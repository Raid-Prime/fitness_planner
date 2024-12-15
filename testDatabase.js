const db = require('./controllers/hydraDb');

db.serialize(() => {
    db.all("SELECT name FROM sqlite_master WHERE type='table'", [], (err, tables) => {
        if (err) {
            console.error(err.message);
        } else {
            console.log('Tables:', tables);
        }
    });
});

db.close(); // Always close the database connection after testing
