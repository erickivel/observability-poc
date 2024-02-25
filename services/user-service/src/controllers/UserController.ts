import {Request, Response} from 'express'
import { dbConnection } from '../db';

export class UserController {
  constructor(){}

  public async createUser(req: Request, res: Response) {
    const { name, email, phone } = req.body;
    console.log(`Creating user: "${name}"`);

    const insertQuery = `
      INSERT INTO users(name, email, phone)
      VALUES($1, $2, $3)
      RETURNING *;
    `

    dbConnection.query(insertQuery, [name, email, phone], (err, result) => {
      if (err) {
        console.error('Error creating user:', err);
        return res.status(500).json({ message: 'Error when creating user' });
      } else {
        console.log(`User "${result.rows[0].name}" created successfully!`);
        res.json(result.rows[0])
      }
    });
  }

  public async listUsers(req: Request, res: Response) {
    console.log("Fetching users");

    const selectQuery = `
      SELECT * FROM users
      ORDER BY id DESC
      LIMIT 100;
    `

    dbConnection.query(selectQuery, (err, result) => {
      if (err) {
        console.error('Error fetching users:', err);
        return res.status(500).json({ message: 'Error fetching users:' });
      } else {
      console.log("Users fetched successfully!");
        res.json(result.rows)
      }
    });
  }
}
