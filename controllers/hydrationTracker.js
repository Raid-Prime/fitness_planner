const db = require('./hydraDb'); // Import SQLite database setup

// 1. Calculate daily water goal based on weight and activity level
const calculateDailyWater = (name, weight, activityLevel) => {
    if (!name || !weight || !activityLevel) {
        throw new Error('Missing required fields');
    }

    // Calculate daily water goal (ml)
    let multiplier = 35; // Default for sedentary
    if (activityLevel === 'Lightly Active') multiplier = 40;
    else if (activityLevel === 'Moderately Active') multiplier = 45;
    else if (activityLevel === 'Very Active') multiplier = 50;

    const dailyGoal = weight * multiplier;

    return new Promise((resolve, reject) => {
        // Save user to the database
        db.run(
            'INSERT INTO users (name, weight, daily_goal) VALUES (?, ?, ?)',
            [name, weight, dailyGoal],
            function (err) {
                if (err) reject(err);
                else resolve({ userId: this.lastID, dailyGoal });
            }
        );
    });
};

// 2. Log water intake
const logWaterIntake = (userId, intake) => {
    if (!userId || !intake) {
        throw new Error('Missing userId or intake');
    }

    return new Promise((resolve, reject) => {
        db.run(
            'INSERT INTO water_logs (user_id, intake) VALUES (?, ?)',
            [userId, intake],
            function (err) {
                if (err) reject(err);
                else resolve({ logId: this.lastID, message: 'Water intake logged successfully' });
            }
        );
    });
};

// 3. Get today's progress
const getHydrationProgress = (userId) => {
    return new Promise((resolve, reject) => {
        db.get(
            `
            SELECT SUM(intake) AS totalIntake, u.daily_goal AS dailyGoal
            FROM water_logs wl
            JOIN users u ON wl.user_id = u.id
            WHERE wl.user_id = ? AND date = CURRENT_DATE
            GROUP BY u.daily_goal
            `,
            [userId],
            (err, row) => {
                if (err) reject(err);
                else resolve(row || { totalIntake: 0, dailyGoal: null });
            }
        );
    });
};

module.exports = {
    calculateDailyWater,
    logWaterIntake,
    getHydrationProgress,
};
