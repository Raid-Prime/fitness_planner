const express = require('express');
const {
    calculateDailyWater,
    logWaterIntake,
    getHydrationProgress,
} = require('../controllers/hydrationTracker'); // Import hydration functions

const router = express.Router();

// Endpoint to calculate daily water needs
router.post('/calculate', async (req, res) => {
    try {
        const { name, weight, activityLevel } = req.body;
        const result = await calculateDailyWater(name, weight, activityLevel);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Endpoint to log water intake
router.post('/log', async (req, res) => {
    try {
        const { userId, intake } = req.body;
        const result = await logWaterIntake(userId, intake);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Endpoint to get hydration progress
router.get('/progress/:userId', async (req, res) => {
    try {
        const { userId } = req.params;
        const result = await getHydrationProgress(userId);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;

