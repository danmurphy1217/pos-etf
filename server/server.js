//! use "npm run server" to start

import express from "express";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";

import authRoutes from "./routes/auth.js";

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(helmet());
app.use(morgan("common"));

app.use("/auth", authRoutes);

var PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`server started on PORT ${PORT}`);
});
