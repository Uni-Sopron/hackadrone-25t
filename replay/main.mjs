import fs from 'fs'
import express from 'express'
import cors from 'cors'

let files = fs
  .readdirSync('logs')
  .sort((a, b) => a.localeCompare(b))
  .filter((file) => file.startsWith('data_') && file.endsWith('.json'))

const app = express()

app.use(cors())

let counter = 0

const formatDateString = (dateString) => {
  const year = dateString.substring(0, 4)
  const month = dateString.substring(4, 6)
  const day = dateString.substring(6, 8)
  const hour = dateString.substring(9, 11)
  const minute = dateString.substring(11, 13)
  const second = dateString.substring(13, 15)

  return `${year}-${month}-${day}T${hour}:${minute}:${second}`
}

app.get('/', (req, res) => {
  console.log('Current index:', counter)
  if (counter >= files.length) {
    counter = 0
    files = fs
      .readdirSync('logs')
      .sort((a, b) => a.localeCompare(b))
      .filter((file) => file.startsWith('data_') && file.endsWith('.json'))
  }
  const fileName = files[counter % files.length]
  const timeString = fileName.replace('data_', '').replace('.json', '')
  const formattedDate = formatDateString(timeString)
  const date = new Date(formattedDate)

  const file = fs.readFileSync(`./logs/${fileName}`, 'utf-8')
  const mock = JSON.parse(file)
  counter++
  res.json({ ...mock, time: date.toISOString() })
})

app.listen(8000, () => console.log('listening'))
