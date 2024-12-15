const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('hydration_tracker.db');

// Create tables
db.serialize(() => {
    db.run(`
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight INTEGER NOT NULL,
            daily_goal INTEGER NOT NULL
        )
    `);

    db.run(`
        CREATE TABLE IF NOT EXISTS water_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE DEFAULT CURRENT_DATE,
            intake INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    `);
});

module.exports = db;
