import {Request, Response} from 'express'
import { logger } from '../server'

export class StressTestingController {
  constructor(){}

  public async longRuntime(req: Request, res: Response) {
    logger.log('info', 'Starting long runtime test')
    setTimeout(() => {
      logger.log('info', 'Long runtime test finished successfully!')
      res.json({
        message: "Long runtime test finished successfully!"
      })
    }, Number(process.env.LONG_RUNTIME_TIME))
  }

  public async error(req: Request, res: Response) {
    logger.log('info', 'Starting error test')
    setTimeout(() => {
      logger.log('error', 'Error test finished successfully!')
      res.status(500).json({
        message: "Error test successfully triggered! XD"
      })
    }, 1000)
  }

  public async loop(req: Request, res: Response) {
    console.log("Starting loop test")
    logger.log('info', 'Starting loop test')
    
    let n = 1;
    while(true) {
      n *= 2
    }

    logger.log('info', 'Loop test finished successfully!')
    console.log("Ending loop test")
    res.json({"message": "Loop test finished successfully!"})
  }
}
