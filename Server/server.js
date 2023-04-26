const express = require("express");
const app = express();
const dbFactory = require('./db.js');
const db = dbFactory("test");
// Server port
const HTTP_PORT = 8000;
// Start server
app.listen(HTTP_PORT, () => {
  console.log("Server running on port %PORT%".replace("%PORT%", HTTP_PORT));
});

// Root endpoint
app.get("/", (req, res, next) => {
  res.json({ message: "Ok" });
});

app.get("/incoming", (req, res, next) => {
  // Auth check
  // Db creation/check
  const db = dbFactory("test");
  // table creation ? maybe with db
  // data duplication check / timestamp as index?
  // data insertion
  // status response
});


app.use(function (req, res) {
  res.status(404);
});
