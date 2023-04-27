const sqlite3 = require('sqlite3').verbose();
const md5 = require('md5');


let db = (path) => {
    return new sqlite3.Database(path + '.sqlite', (err) => {
        if (err) {
            console.error(err.message);
            throw err;
        } else {
            console.log('Connectd to SQLite DB');
        }
    })
}

module.exports = db;