const express = require('express');
const { getWorkoutPlan } = require('../controllers/workoutController');

const router = express.Router();

router.post('/', getWorkoutPlan);

module.exports = router;
