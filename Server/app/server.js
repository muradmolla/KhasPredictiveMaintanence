const express = require("express");
const app = express();
const dbFactory = require("./db.js");
require("dotenv").config();

const inserter = require("./dataInsert.js");
// Server port
const HTTP_PORT = process.env.PORT;

// Start server
app.listen(HTTP_PORT, () => {
  console.log("Server running on port %PORT%".replace("%PORT%", HTTP_PORT));
});

// Root endpoint
app.get("/", (req, res, next) => {
  res.json({ message: "Ok" });
});

// Data insertion
app.get("/incoming", (req, res, next) => {
  // TODO: Auth check

  //let name = name.replace(/([^a-z0-9]+)/gi, "-");

  if (
    inserter("trabzon", "vibrationx", [
      [34524, 63.3],
      [34535, 22.9],
      [34926, 27.3],
      [38527, 82.3],
    ])
  )
    //const db = dbFactory("test");

    // table creation ? maybe with db
    // data duplication check / timestamp as index?
    // data insertion
    res.json({ message: "OK" });
});

app.get("/token", (req, res, next) => {});

app.use(function (req, res) {
  res.status(404);
});
