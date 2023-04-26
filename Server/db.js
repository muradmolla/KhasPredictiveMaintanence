const sqlite3 = require('sqlite3').verbose();
const md5 = require('md5');


let db = (name) => {
    name = name.replace(/([^a-z0-9]+)/gi, "-");
    return new sqlite3.Database('db/' + name + '.sqlite', (err) => {
        if (err) {
            console.error(err.message);
            throw err;
        } else {
            console.log('Connectd to SQLite DB');
        }
    })
}

module.exports = db