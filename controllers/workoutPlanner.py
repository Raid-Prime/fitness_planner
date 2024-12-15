import sqlite3
import heapq
import copy
import sys
from workoutDb import create_database


class AStarWorkoutPlanner:
    def __init__(self, db_name):
        self.workouts = self.load_data(db_name)

    def load_data(self, db_name):
        """Load workouts from the SQLite database."""
        try:
            connection = sqlite3.connect(db_name)
            cursor = connection.cursor()

            cursor.execute("SELECT name, calories_burned, duration, reps, intensity, heuristic_weight FROM workouts")
            workouts = [
                {
                    "name": row[0],
                    "calories_burned": row[1],
                    "duration": row[2],
                    "reps": row[3],
                    "intensity": row[4],
                    "heuristic_weight": row[5]
                }
                for row in cursor.fetchall()
            ]

            connection.close()
            return workouts
        except sqlite3.Error as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            return []

    def heuristic(self, state, goal_calories):
        """Estimate remaining calories to burn."""
        remaining = max(0, goal_calories - state["calories"])
        return remaining

    def find_workout_plan(self, goal_calories, intensity):
        """A* search to find the optimal workout plan."""
        if goal_calories <= 0:
            return None

        start_state = {
            "calories": 0,
            "workouts": []
        }
        frontier = []
        visited = set()
        counter = 0

        # Push the start state onto the priority queue
        heapq.heappush(frontier, (self.heuristic(start_state, goal_calories), counter, start_state))

        while frontier:
            heuristic_value, _, current_state = heapq.heappop(frontier)

            # Check if we've reached or exceeded the goal calories
            if current_state["calories"] >= goal_calories:
                return current_state

            state_key = tuple((workout["name"], workout["sets"]) for workout in current_state["workouts"])
            if state_key in visited:
                continue
            visited.add(state_key)

            for workout in self.workouts:
                # Apply intensity filter
                if intensity == "low" and workout["intensity"] == "high":
                    continue
                if intensity == "high" and workout["intensity"] == "low":
                    continue

                new_state = copy.deepcopy(current_state)
                new_state["calories"] += workout["calories_burned"]
                found = False
                for w in new_state["workouts"]:
                    if w["name"] == workout["name"]:
                        w["sets"] += 1
                        found = True
                        break
                if not found:
                    new_state["workouts"].append({
                        "name": workout["name"],
                        "duration": workout["duration"],
                        "reps": workout["reps"],
                        "sets": 1,
                        "calories_burned": workout["calories_burned"]
                    })

                counter += 1
                # The heuristic includes both the remaining calories and the workout's heuristic weight
                new_heuristic_value = self.heuristic(new_state, goal_calories) + workout["heuristic_weight"]
                heapq.heappush(frontier, (new_heuristic_value, counter, new_state))

        return None


import json

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Usage: python3 workoutPlanner.py <goal_calories> <intensity>"}))
        sys.exit(1)

    goal_calories = int(sys.argv[1])
    intensity = sys.argv[2]

    # Create or re-create the database before running the planner
    create_database("fitness_workouts.db")

    # Instantiate the planner and find the plan
    planner = AStarWorkoutPlanner("fitness_workouts.db")
    workout_plan = planner.find_workout_plan(goal_calories, intensity)

    if workout_plan:
        # Output the result as JSON
        print(json.dumps({
            "workouts": workout_plan["workouts"],
            "total_calories_burned": sum(w["calories_burned"] * w["sets"] for w in workout_plan["workouts"])
        }))
    else:
        # Output an error as JSON
        print(json.dumps({"error": "No valid workout plan found."}))







