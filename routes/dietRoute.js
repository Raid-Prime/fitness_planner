const express = require('express');
const { dietPlanner } = require('../controllers/dietController'); // Import the controller

const router = express.Router();

// Test GET route
router.get('/test', (req, res) => {
    res.json({ message: 'Test route is working!' });
});

// Re-integrate the dietPlanner function for the POST route
router.post('/', (req, res) => {
    console.log('Request received at /api/diet'); // Log the request
    dietPlanner(req, res); // Pass the request to the controller
});

module.exports = router;



