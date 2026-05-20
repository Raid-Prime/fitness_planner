# Fitness Planner

A comprehensive health and wellness application designed to provide personalized diet recommendations, workout plans, and hydration tracking. The system utilizes a Node.js backend to integrate web-based user interfaces with Python-driven analytical scripts.

## Features

- **Diet Recommendation Engine**: Generates personalized meal plans based on user metrics including weight, height, age, gender, activity level, and specific fitness goals.
- **Workout Planner**: Provides structured exercise routines tailored to user requirements.
- **Hydration Tracker**: Allows users to log and monitor daily water intake via a dedicated SQLite database.
- **Report Exporting**: Integration with `jspdf` and `html2canvas` enables users to export their fitness and diet plans as PDF documents.

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Node.js, Express
- **Processing**: Python 3 (via `child_process` spawning)
- **Database**: SQLite3
- **Key Libraries**:
    - `cors` & `body-parser`: Request handling and cross-origin resource sharing.
    - `jspdf` & `html2canvas`: Client-side PDF generation.
    - `sqlite3`: Persistent storage for workouts and hydration data.

## Project Structure

```text
├── controllers/            # Logic for diet, workouts, and hydration
│   ├── dietController.py   # Python-based diet recommendation logic
│   ├── dietController.js   # Node.js bridge to Python scripts
│   └── ...                 # Additional JS/Python controllers
├── public/                 # Static frontend assets (HTML/CSS/JS)
├── routes/                 # API endpoint definitions
├── server.js               # Primary Express server entry point
├── *.db                    # SQLite database files
└── package.json            # Node.js dependencies and metadata
```

## Getting Started

### Prerequisites

- **Node.js**: Version 14.x or higher recommended.
- **Python**: Version 3.x required for recommendation engines.
- **NPM**: Package manager for dependency installation.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Raid-Prime/fitness_planner.git
   cd fitness_planner
   ```

2. Install backend dependencies:
   ```bash
   npm install
   ```

3. Ensure Python dependencies (if any) are installed for the scripts in the `controllers/` directory.

### Running the Application

1. Start the Express server:
   ```bash
   node server.js
   ```
2. The server will launch on `http://localhost:5000`.
3. Open `public/index.html` (or the relevant entry page) in your browser to access the interface.

## API Endpoints

- `POST /api/diet`: Submits user metrics to retrieve a diet plan.
- `POST /api/workout`: Retrieves tailored workout routines.
- `GET/POST /api/hydration`: Manages and retrieves water intake logs.

## License

This project is licensed under the ISC License.
