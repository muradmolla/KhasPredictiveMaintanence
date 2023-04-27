const dbFactory = require("./db.js");
const fs = require("fs");

const validTables = [
  "vibrationx",
  "vibrationy",
  "vibrationz",
  "temperature",
  "current",
];

const dataInsert = (node, table, data) => {
  // check if table is valid
  if (!validTables.includes(table)) return false;

  var dir = "./db/" + node;

  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir);
  }

  const ts = Date.now();

  const date_ob = new Date(ts);
  const date = ("00" + date_ob.getDate()).slice(-2);
  const month = ("00" + date_ob.getMonth() + 1).slice(-2);
  const year = date_ob.getFullYear();
  const db = dbFactory(dir + "/" + year + "-" + month + "-" + date);

  db.run(
    "CREATE TABLE IF NOT EXISTS " +
      table +
      "(timestamp INTEGER PRIMARY KEY, value REAL)"
  );
  db.serialize(function () {
    db.run("begin transaction");

    for (var i = 0; i < data.length; i++) {
      // TODO: check data values
      db.run(
        "INSERT INTO" + table + "(timestamp, value) values (?, ?)",
        data[i][0],
        data[i][1]
      );
    }

    db.run("commit");
  });
  return true;
};

module.exports = dataInsert;
