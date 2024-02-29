import express from 'express'
import cors from 'cors'
import 'dotenv/config'
import winston from 'winston'

import { router } from "./routes"

const app = express();

app.use(express.json())
app.use(cors())

export const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  defaultMeta: { service: 'user-service' },
  transports: [
    new winston.transports.Console(),
  //   //
  //   // - Write all logs with importance level of `error` or less to `error.log`
  //   // - Write all logs with importance level of `info` or less to `combined.log`
  //   //
  //
  //   new winston.transports.File({ filename: 'error.log', level: 'error' }),
  //   new winston.transports.File({ filename: 'combined.log' }),
  ],
});

logger.log("info", "Server started on port 3000")

app.use(router)

app.listen(3000, () => {
  console.log("User Service is running on port 3000 🚀")
})

