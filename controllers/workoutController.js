const { spawn } = require('child_process');

const getWorkoutPlan = (req, res) => {
    const { goalCalories, intensity } = req.body;

    // Spawn the Python process
    const python = spawn('python3', [
        './controllers/workoutPlanner.py',
        goalCalories,
        intensity,
    ]);

    let output = '';
    let error = '';

    // Capture the Python script's stdout
    python.stdout.on('data', (data) => {
        output += data.toString();
    });

    // Capture errors from the Python script
    python.stderr.on('data', (data) => {
        error += data.toString();
    });

    // Handle the process close
    python.on('close', (code) => {
        if (code === 0) {
            try {
                // Parse the Python dictionary output as JSON
                const result = JSON.parse(output);
                res.json(result); // Send the result as JSON response
            } catch (err) {
                console.error('Error parsing Python output:', err);
                console.error('Raw output received:', output);
                res.status(500).json({ error: 'Error parsing Python output' });
            }
        } else {
            console.error('Python Error:', error);
            res.status(500).json({ error: 'Error running Python script', details: error });
        }
    });
};

module.exports = { getWorkoutPlan };



