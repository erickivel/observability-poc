import {Request, Response} from 'express'

export class StressTestingController {
  constructor(){}

  public async longRuntime(req: Request, res: Response) {
    setTimeout(() => {
      res.json({
        message: "Long runtime test finished successfully!"
      })
    }, Number(process.env.LONG_RUNTIME_TIME))
  }

  public async error(req: Request, res: Response) {
    setTimeout(() => {
      res.status(500).json({
        message: "Error test successfully triggered! XD"
      })
    }, 1000)
  }

  public async loop(req: Request, res: Response) {
    console.log("Starting loop test")
    
    let n = 1;
    while(true) {
      n *= 2
    }

    console.log("Ending loop test")
    res.json({"message": "Loop test finished successfully!"})
  }
}
