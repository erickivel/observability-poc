import { Router } from "express";
import { UserController } from "../controllers/UserController";

const router = Router()

const userController = new UserController()

router.get("/ping", (req, res) => {
  res.json({
    "ok": true
  })
})

router.post("/users", userController.createUser);
router.get("/users", userController.listUsers);
router.post("/users/order", userController.placeOrder);

export { router }
