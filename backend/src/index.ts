import express, { NextFunction } from "express";
import mongoose from "mongoose";

require("dotenv").config();
const port: number = Number(process.env.PORT) || 8000;

const app: express.Express = express();

app.use(express.json());
app.use((req: express.Request, res: express.Response, next: NextFunction) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
  res.setHeader("Access-Control-Allow-Headers", [
    "Content-Type",
    "Authorization",
  ]);
  next();
});

mongoose
  .connect(process.env.DB_HOST as string)
  .then(() => console.log("Connected to database"))
  .catch((err: Error) =>
    console.error("Error connecting to database:", err.message)
  );

app.listen(port, async () => {
  console.log(`Questscape backend is now listening on port ${port}`);
});
