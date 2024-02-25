import 'dotenv/config'
import {Pool} from "pg"

const DB_USER = process.env.DB_USER
const DB_PASSWORD = process.env.DB_PASSWORD
const DB_HOST = process.env.DB_HOST
const DB_PORT = process.env.DB_PORT
const DB_NAME = process.env.DB_NAME

export const dbConnection = new Pool({
  user: DB_USER,
  host: DB_HOST,
  database: DB_NAME,
  password: DB_PASSWORD,
  port: Number(DB_PORT),
});

dbConnection.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('Error connecting to the database:', err);
  } else {
    console.log('Connected to the database');
  }
});

// Close the pool when the process is terminated
process.on('SIGINT', () => {
  console.log('Closing database connection pool');
  dbConnection.end(() => {
    console.log('Database connection pool closed');
    process.exit(0);
  });
});

// Handle other termination signals as well
process.on('SIGTERM', () => {
  console.log('Closing database connection pool');
  dbConnection.end(() => {
    console.log('Database connection pool closed');
    process.exit(0);
  });
});
