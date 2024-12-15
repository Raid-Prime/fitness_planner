import sys
import json
import sqlite3

def calculate_bmr(weight, height, age, gender):
    if gender == 'Male':
        return round(10 * weight + 6.25 * height - 5 * age + 5, 2)
    return round(10 * weight + 6.25 * height - 5 * age - 161, 2)

def calculate_tdee(bmr, activity_level):
    activity_factors = {
        "Sedentary": 1.2,
        "LightlyActive": 1.375,
        "ModeratelyActive": 1.55,
        "VeryActive": 1.725
    }
    # Ensure input matches dictionary keys
    activity_level = activity_level.replace(" ", "")
    return round(bmr * activity_factors[activity_level], 2)


def calculate_macronutrients(tdee):
    protein_percentage = 0.25
    carb_percentage = 0.50
    fat_percentage = 0.25

    protein_calories = tdee * protein_percentage
    carbs_calories = tdee * carb_percentage
    fats_calories = tdee * fat_percentage

    protein_grams = protein_calories / 4
    carbs_grams = carbs_calories / 4
    fats_grams = fats_calories / 9

    return round(protein_grams,2), round(carbs_grams, 2), round(fats_grams, 2)

def recommend_meals_greedy(db_name, target_calories, target_protein, target_carbs, diet_preference, optimization_goal):
    connection = sqlite3.connect('/workspaces/codespaces-blank/fitness_planner/controllers/Diet_Recom.db')
    cursor = connection.cursor()

    # Fetch meals based on diet preference
    if diet_preference and diet_preference != "None":
        cursor.execute("SELECT name, calories, protein, carbs, fats, meal_type FROM meals WHERE type = ?", (diet_preference,))
    else:
        cursor.execute("SELECT name, calories, protein, carbs, fats, meal_type FROM meals")

    meals = cursor.fetchall()
    connection.close()

    # Debugging: Validate fetched meals
    if not meals:
        return {"Breakfast": [], "Lunch": [], "Dinner": []}, 0, 0, 0, 0

    # Initialize variables
    meal_plan = {"Breakfast": [], "Lunch": [], "Dinner": []}
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0
    added_meals = set()

    # Select meals using greedy heuristic
    for meal_type in meal_plan:
        available_meals = [meal for meal in meals if meal[5] == meal_type]
        partial_calories = 0

        if available_meals:
            if optimization_goal == "minimize_fat":
                meals_sorted = sorted(available_meals, key=lambda meal: meal[4])
            elif optimization_goal == "maximize_protein":
                meals_sorted = sorted(available_meals, key=lambda meal: -meal[2])
            else:
                raise ValueError("Unknown optimization goal")

            for meal in meals_sorted:
                name, calories, protein, carbs, fats, m_type = meal
                if name not in added_meals and partial_calories + calories <= target_calories * 0.36:
                    meal_plan[meal_type].append(name)
                    total_calories += calories
                    partial_calories += calories
                    total_protein += protein
                    total_carbs += carbs
                    total_fats += fats
                    added_meals.add(name)

    return meal_plan, total_calories, total_protein, total_carbs, total_fats

if __name__ == "__main__":
    # Parse input arguments
    weight = float(sys.argv[1])
    height = float(sys.argv[2])
    age = int(sys.argv[3])
    gender = sys.argv[4]
    activity_level = sys.argv[5]
    goal = sys.argv[6]
    diet_preference = sys.argv[7]

    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)

    if goal == "Weight Loss":
        tdee -= 500
    elif goal == "Muscle Gain":
        tdee += 500

    macronutrients = calculate_macronutrients(tdee)
    meal_plan, total_calories, total_protein, total_carbs, total_fats = recommend_meals_greedy(
        "Diet_Recom.db", tdee, macronutrients[0], macronutrients[1], diet_preference, "minimize_fat"
    )

    output = {
        "tdee": tdee,
        "macronutrients": macronutrients,
        "meal_plan": meal_plan,
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fats": total_fats
    }

    print(json.dumps(output))
