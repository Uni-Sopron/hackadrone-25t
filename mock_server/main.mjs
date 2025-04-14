import express from 'express'
import cors from 'cors'
import fs from 'fs'

const app = express()

app.use(cors())

app.get('/', (req, res) => {
  const file = fs.readFileSync('./mock.json', 'utf-8')
  const mock = JSON.parse(file)
  res.json(mock)
})

app.listen(8000, () => console.log('listening on port 8000'))
