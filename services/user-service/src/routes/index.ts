import { Router } from "express";
import { UserController } from "../controllers/UserController";
import { StressTestingController } from "../controllers/StressTestingController";
import { logger } from "../server";

const router = Router()

const userController = new UserController()
const stressTestingController = new StressTestingController()

router.get("/ping", (req, res) => {
  logger.log('info', 'Running ping route!')
  res.json({
    "ok": true
  })
})

router.post("/users", userController.createUser);
router.get("/users", userController.listUsers);
router.post("/users/order", userController.placeOrder);

router.get("/stress-testing/long-runtime", stressTestingController.longRuntime);
router.get("/stress-testing/error", stressTestingController.error);
router.get("/stress-testing/loop", stressTestingController.loop);

export { router }
