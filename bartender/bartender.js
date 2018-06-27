const express = require('express')
const app = express()
app.use('/', express.static('public'))
app.listen(5102, () => console.log('Garcon Bartender Dashboard on port 5102!'))
