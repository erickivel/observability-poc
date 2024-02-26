import express from 'express'
import cors from 'cors'
import 'dotenv/config'

import { router } from "./routes"

const app = express();

app.use(express.json())
app.use(cors())

app.use(router)

app.listen(3000, () => {
  console.log("User Service is running on port 3000 🚀")
})

