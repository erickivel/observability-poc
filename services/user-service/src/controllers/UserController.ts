import {Request, Response} from 'express'
import { dbConnection } from '../db';
import axios from 'axios';
import { logger } from '../server';

export class UserController {
  constructor(){}

  public async createUser(req: Request, res: Response) {
    const { name, email, phone } = req.body;
    console.log(`Creating user: "${name}"`);
    logger.log('info', `Creating user: "${name}"`)

    const insertQuery = `
      INSERT INTO users(name, email, phone)
      VALUES($1, $2, $3)
      RETURNING *;
    `

    dbConnection.query(insertQuery, [name, email, phone], (err, result) => {
      if (err) {
        console.error('Error creating user:', err);
        logger.log('error', `Error creating user: ${err}`)
        return res.status(500).json({ message: 'Error when creating user' });
      } else {
        logger.log('info', `User "${result.rows[0].name}" created successfully!`)
        console.log(`User "${result.rows[0].name}" created successfully!`);
        res.json(result.rows[0])
      }
    });
  }

  public async listUsers(req: Request, res: Response) {
    console.log("Fetching users");
    logger.log('info', "Fetching users")

    const selectQuery = `
      SELECT * FROM users
      ORDER BY id DESC
      LIMIT 100;
    `

    dbConnection.query(selectQuery, (err, result) => {
      if (err) {
        console.error('Error fetching users:', err);
        logger.log('error', `Error fetching users: ${err}`)
        return res.status(500).json({ message: 'Error fetching users:' });
      } else {
        console.log("Users fetched successfully!");
        logger.log('info', 'Users fetched successfully!')
        res.json(result.rows)
      }
    });
  }

  public async placeOrder(req: Request, res: Response) {
    const { user_id, product_ids, quantities } = req.body;
    console.log(`Placing order user_id: "${user_id}", with products: [${product_ids.join(", ")}]`);
    logger.log('info', `Placing order user_id: "${user_id}", with products: [${product_ids.join(", ")}]`)

    try {
      const {data : orderData} = await axios.post("http://localhost:3001/orders", {
        user_id: user_id
      })

      const postProductOrdersPromises = product_ids.map((product_id: string, idx: number) => {
        return axios.post("http://localhost:3002/product_orders", {
          order_id: orderData.id,
          product_id: product_id,
          quantity: quantities[idx]
        })
      })

      await Promise.all(postProductOrdersPromises)
        .then(async () => {
          const {data : getOrder} = await axios.get(`http://localhost:3001/orders/${orderData.id}`)

          res.json(getOrder);
        })
        .catch(err => {
          logger.log('error', `Error placing order: ${err}`)
        })

    } catch (error) {
      console.error('Error placing order:', error);
      logger.log('error', `Error placing order: ${error}`)
      return res.status(500).json({ message: 'Error placing order:' });
    }
  }
}
