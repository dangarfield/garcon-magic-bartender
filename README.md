# Garcon! Magic Bartender
> Magic Bartenders who predict the future and make the right drinks for the right customer so they are ready when they get to the bar

The experience of having a drink ready for you when you get to the bar, and the bartending remembering you and your habits is great for our customers. We want to try and assist our bartenders in this manner by creating some unobtrusive but modern technology.

We can do this programmatically, eg, User X has bought 1 beer last time, we can assume he'll buy another one now. However, we want to be able to create some machine learning models to aid with this task. For this hackathon project we will make some assumptions, limit the data to synthetically created and not use any metadata about our customers to aid in the modelling (eg, age, gender, location, activity preference, favourite newspaper, colour of swimshorts etc)

TUI Maker Fair Project 2018 from Dan Garfield


### Assumptions
- 1 person buys 1 drink - No 'rounds'
- Whilst people generally gather together, we will not profile groups or group activity
- User data will be synthetically generated
- User location data is expected to be streamed (id, x_pos, y_pos) as per cruise ships
- 1 bartender
- 1 queue position, users will queue on top of each other (no collision detecting within bar area)
- No one leaves, no one enters the bar, no one changes seat or position

### Base logic (tbc)
`Logic Stub`
- Seeded random
- Create 10-ish profiles for behaviour (walking speed, frequency of drinking, frequency of going to toilet, likeliness of drink choice)
- Init visualiser with data

`Visualiser`
- Init with logic stubbed data
- Create static map of restaurant with tables, bar, positions for all (50?) users (origins) and toilet
- Paths and origins are set for each user / can be group based on position, different paths can go in different directions to the bar / toilet
- Queue required for bartender service, bartender requires 10 seconds to make a drink
- (For simplicity, although against decoupling) Syndicate travel event data, rather than doing this in the movement listener
- Animate loop
-- User at table, no movement required > Stay
-- User at table, go to toilet > Create / select path(s) and follow
-- User at table, go to bar > Create / select path(s) and follow
-- User moving to toilet / bar > Follow path, point in direction, avoid collisions, add x_pos, y_pos to array for tracking
-- User arrives at toilet > Wait for x time. Syndicate travel event data
-- User returning from toilet > Return to origin, face table centre
-- User arrives at bar > Select drink, wait for bartender service
-- User been served at bar > Syndicate travel event data to movement listener and dashboard
-- User returning from bar > Return to origin, face table centre


`Movement Listener`
- Based on movement data sent / polled from the visualised
- If the movement is a finished journey we can prepare training data for the movement classifier or predict movement based on the classifier
- If number of steps is longer than 5 and movement is towards toilet or bar > Get prediction from movement classifier
- If the movement prediction is to the bar, attempt a 'Drink Classifier' > Send the result to the bartender in the visualiser and dashboard
- After X time / an amount of training data is generated > train model in movement classifier

`Movement Classifier`
- Training data comes from [toilet/bar,['x_pos_1','y_pos_1]...['x_pos_n','y_pos_n]]
- May need to transform [x_pos,y_pos] to a single number
- May need to separate samples so that there are always a fixed number of samples (5?) in each. Therefore an array of 8 positions, will result in 4 ranges of 5 positions, each with the same destination label, representing different parts on the journey.
- This would make it easier, eg, we could try Random Forest Classifiers or Naive Bayesian Classifiers straight away

`Drink Classifier`
- tbc

`Dashboard`
- Plot waiting customers (eg, bartender activity list)
- Plot bartender current activity
- Plot incoming prediction list
- Plot percentage and total orders correctly predicted

### Technology Usage (tbc)
`Visualiser`
- Three.js
- ThreeSteer for three.js

`Classifiers`
- As simple as possible, skikit-learn or something similar with an api layer
- Start with Random Forest and Naive Bayesian Classifiers based on fixed column
- We can move on to

### Still to do
- General
-- Update this readme technology usage, installation, base logic and assumptions

- Visualiser
-- Better UI for lists on dashboard, eg highlight the bar queue, movement list and prediction results better
-- Add icons for actual and predicted destinations that hover over the moving individuals
-- Add / adapt the bar queue for a 'bartender display' which contains a combination of the incoming movements to the bar and the existing bar list
-- Add rotating effect for screen, eg, keep orbit controls, but when dragged mouse movement, keep rotating slowly, zoom in slightly for default
-- Syndicate data for bartender display to a queue (pubnub or something), that the other projects can think about using
-- Add proper human names to the users
-- Maybe add some more 3d models for the bar, tables, walls, maybe some other furniture such as piano, pictures, plants etc
-- Get users to point the right way when they are at the origin
-- I think there are some dud journeys that still go through the walls, maybe add something back into the dat.gui that allows us to test all movements again, this is probably because I adjusted the threshold radius to 50 from 10
-- Potentially reinstate the avoid for the journeys, although we have to deal with the bottleneck locations (typically around the origins of others and at the bar, toilet and smoke destinations)
-- Test with different seeded values and find a good example seed that highlights a failed movement (eg, in the top left room going to the toilet, but incorrectly predicted as the bar)
-- Try moving the bar to the top right hand corner to make movements even more accurate, probably more pain than its worth

- Predictor
-- Walk through with models with Bijeesh and Abhiram, it seems to be fairly solid
-- The drinks predictor is very basic, purely based on that users' location. As these profile attributes are random assigned, it is difficult at this stage to group typical drinkers together (eg, girls night out table -> wine, stag do table -> beer). Think about how we could / should plant this data
-- Potentially add additional metadata to the users, such as age, income, etc, but again, faking this data is messy. Could we maybe find som real world drinkers profile information to replace our randomly assigned one?