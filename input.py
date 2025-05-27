from fastapi import FastAPI,Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
app = FastAPI()

templates = Jinja2Templates(directory=".")

#靜態資料夾
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("input_form.html", {"request": request})

@app.post("/submit")
async def handle_form(
    request: Request,
    age: int = Form(...),
    gender: str = Form(...),
    height: float = Form(...),
    weight: float = Form(...),
    activity_level: str = Form(...),
    health_goals: str = Form(...),
    dish_type: str = Form(...),
    budget: float = Form(...),
    servings_per_meal: int = Form(...),
    dietary_preferences: str = Form(""),
    restrictions: str = Form("")
):
    def calculate_calories_and_meals(height, weight, age, gender, activity_level, health_goals):
        # Step 1: BMR
        if gender == "Male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # Step 2: Activity Multiplier
        activity_map = {"low": 1.2, "moderate": 1.55, "high": 1.725}
        tdee = bmr * activity_map[activity_level]
        
        # Step 3: Goal adjustment
        if health_goals == "weight_loss":
            target_cal = tdee - 400
        elif health_goals == "muscle_gain":
            target_cal = tdee + 300
        else:
            target_cal = tdee

        # Step 4: Recommend number of meals
        if health_goals == "weight_loss":
            meals = 2 if activity_level == "low" else 3
        elif health_goals == "muscle_gain":
            meals = 4 if activity_level == "high" else 3
        else:
            meals = 3
        return round(target_cal), meals

    print(
        "\nage:",age,
        "\ngender:",gender,
        "\nheight:",height,
        "\nweight:",weight,
        "\nactivity_level:",activity_level,
        "\nhealth_goals:",health_goals,
        "\ndish_type:",dish_type,
        "\nbudget:",budget,
        "\nservings_per_meal:",servings_per_meal,
        "\ndietary_preferences:",dietary_preferences,
        "\nrestrictions:",restrictions
    )
    print("Calculating calories and meals...")
    # Call the calculation function
    print(calculate_calories_and_meals(height, weight, age, gender, activity_level, health_goals))
    return templates.TemplateResponse("input_form.html", {"request": request})