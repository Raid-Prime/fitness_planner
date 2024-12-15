import sqlite3
import os
import sys

def create_database(db_name="fitness_workouts.db"):
    """Creates the SQLite database and populates it with workouts."""
    if os.path.exists(db_name):
        # Skip creating the database if it already exists
        return

    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # Create table for workouts
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            name TEXT PRIMARY KEY,
            calories_burned INTEGER,
            duration INTEGER,
            reps INTEGER,
            intensity TEXT,
            heuristic_weight INTEGER
        );
        """)

        # Insert workout data
        workouts_data = [
            ("Running", 500, 30, 0, "high", 1),
            ("Weightlifting", 300, 45, 10, "high", 2),
            ("Yoga", 200, 60, 0, "low", 3),
            ("HIIT", 600, 20, 15, "high", 1),
            ("Cycling", 400, 45, 0, "high", 2),
            ("Swimming", 600, 30, 0, "high", 1),
            ("Pilates", 250, 40, 0, "low", 3),
            ("Rock Climbing", 500, 60, 5, "high", 2),
            ("Dance Class", 300, 60, 0, "low", 3),
            ("Boxing", 450, 30, 15, "high", 1),
            ("Walking", 150, 60, 0, "low", 3)
        ]

        # Insert data into the table
        cursor.executemany("INSERT OR IGNORE INTO workouts VALUES (?, ?, ?, ?, ?, ?);", workouts_data)

        # Commit changes and close connection
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}", file=sys.stderr)

