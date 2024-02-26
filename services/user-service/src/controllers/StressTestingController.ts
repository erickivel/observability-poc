import {Request, Response} from 'express'

export class StressTestingController {
  constructor(){}

  public async longRuntime(req: Request, res: Response) {
    setTimeout(() => {
      res.json({
        ok: true
      })
    }, Number(process.env.LONG_RUNTIME_TIME))
  }

  public async error(req: Request, res: Response) {
    setTimeout(() => {
      res.status(500).json({message: "Error successfully triggered! XD"})
    }, 1000)
  }
}
