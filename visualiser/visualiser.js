const express = require('express')
const app = express()
const server = require('http').Server(app)
const io = require('socket.io')(server)
const path = require('path')
const fs = require('fs')
const dateFormat = require('dateformat')

let fileRaw
let filePosition
let fileDrink
let finishedJourneys = []
app.use('/public', express.static('public'))
app.get('/', function (req, res) {
  res.sendfile(path.join(__dirname, '/public/index.html'))
})

io.on('connection', function (socket) {
  console.log('Visualiser connected')
  socket.on('finishedJourney', function (data) {
    writeToFile(data)
  })
})

function writeToFile (journey) {
  console.log('finishedJourney', journey)
  finishedJourneys.push(journey)
  processRawData(finishedJourneys)
  processDrinkTrainingData(journey)
  processMovementTrainingData(journey)
}
function processRawData (data) {
  fs.appendFileSync(fileRaw, JSON.stringify(data))
}
function processDrinkTrainingData (data) {
  if (data.drink !== '') {
    var cols = []
    cols.push(data.id)
    cols.push(data.drink)
    cols.push(getDrinkId(data.drink))
    var row = cols.join(',') + '\n'
    fs.appendFileSync(fileDrink, row)
  }
}

function processMovementTrainingData (data) {
// TODO - Process this into a format that we can start training on.
// Thoughts in order to aid simple classification:
// x,z becomes a single number representing the position - i = x + width*z; (this is 3000 in our grid)
// location becomes an int to reference the location
// split journeys into 5 elements, eg, if there are 8 positions, there will be will be rows
  var len = data.positions.length
  var width = 3000
  if (len > 5) {
    for (let i = 0; i < len - 4; i++) {
      var cols = []
      cols.push((data.positions[i][0] + (width * data.positions[i][1])))
      cols.push((data.positions[i + 1][0] + (width * data.positions[i + 1][1])))
      cols.push((data.positions[i + 2][0] + (width * data.positions[i + 2][1])))
      cols.push((data.positions[i + 3][0] + (width * data.positions[i + 3][1])))
      cols.push((data.positions[i + 4][0] + (width * data.positions[i + 4][1])))
      cols.push(data.location)
      cols.push(getLocationId(data.location))
      var row = cols.join(',') + '\n'
      fs.appendFileSync(filePosition, row)
    }
  }
}
var drinkMapping = {
  beer: 1,
  whiteWine: 2,
  redWine: 3,
  water: 4,
  coke: 5
}
function getDrinkId (drink) {
  return drinkMapping[drink]
}
var locationMapping = {
  bar: 1,
  toilet: 2,
  smoke: 3
}
function getLocationId (location) {
  return locationMapping[location]
}
function createFiles () {
  var day = dateFormat(new Date(), 'yyyy-mm-dd_hh-MM-ss')
  fileRaw = 'training-data/' + day + '_raw.json'
  filePosition = 'training-data/' + day + '_position.csv'
  fileDrink = 'training-data/' + day + '_drink.csv'
  fs.openSync(fileRaw, 'w')
  fs.openSync(filePosition, 'w')
  fs.openSync(fileDrink, 'w')
}
createFiles()
server.listen(5100, () => console.log('Garcon Visualiser on port 5100!'))
