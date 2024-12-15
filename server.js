const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors'); // Import CORS
const dietRoute = require('./routes/dietRoute'); // Import the diet route
const workoutRoute = require('./routes/workoutRoute'); // Import workout route
const hydrationRoute = require('./routes/hydrationRoute'); 

const app = express();

// Enable CORS for all routes
app.use(cors());

// Middleware for logging all incoming requests
app.use((req, res, next) => {
    console.log(`Incoming Request: ${req.method} ${req.url}`);
    next();
});

// Middleware for parsing JSON bodies
app.use(bodyParser.json());

app.use(express.static('public'));

// Define routes after logging middleware
app.use('/api/diet', dietRoute); // API path for diet
app.use('/api/workout', workoutRoute); // API path for workout
app.use('/api/hydration', hydrationRoute); // API path for hydration


// Start the server
app.listen(5000, () => console.log('Server running on port 5000'));


