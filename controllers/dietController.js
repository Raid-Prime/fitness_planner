const { spawn } = require('child_process');

const dietPlanner = (req, res) => {
    console.log('dietPlanner function triggered'); // Add log here
    const { weight, height, age, gender, activityLevel, goal, dietPreference } = req.body;

    console.log('Request Body:', req.body); // Add log here
    console.log('Attempting to run Python script at:', '/workspaces/codespaces-blank/fitness_planner/controllers/dietController.py');

    const python = spawn('python3', [
        '/workspaces/codespaces-blank/fitness_planner/controllers/dietController.py',
        weight,
        height,
        age,
        gender,
        activityLevel,
        goal,
        dietPreference,
    ]);

    let output = '';
    python.stdout.on('data', (data) => {
        console.log('Python Output:', data.toString()); // Add log here
        output += data.toString();
    });

    python.stderr.on('data', (data) => {
        console.error('Python Error:', data.toString()); // Add log here
    });

    python.on('close', (code) => {
        console.log(`Python script exited with code ${code}`); // Add log here
        if (code === 0) {
            try {
                res.json(JSON.parse(output)); // Send Python response
            } catch (err) {
                console.error('Error Parsing Python Output:', err);
                res.status(500).send('Error parsing Python output');
            }
        } else {
            res.status(500).send('Error running Python script');
        }
    });
};

module.exports = { dietPlanner };



