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


def show_html(_top3):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)),
                            url("/static/background_image.jpg") no-repeat center center fixed;
                background-size: cover;
                margin: 0;
                padding: 20px;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: rgba(255, 255, 255, 0.95);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            }
            h2 {
                text-align: center;
                color: #2c3e50;
                margin-bottom: 30px;
                font-size: 28px;
            }
            .recipe-card {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            }
            h3 {
                color: #e74c3c;
                text-align: center;
                margin-bottom: 20px;
                font-size: 24px;
            }
            p {
                text-align: center;
                margin: 10px 0;
                color: #34495e;
            }
            ul {
                list-style-type: none;
                padding: 0;
                margin: 20px 0;
            }
            li {
                text-align: center;
                padding: 8px 0;
                color: #7f8c8d;
                border-bottom: 1px solid #eee;
            }
            li:last-child {
                border-bottom: none;
            }
            .carbon-info {
                color: #27ae60;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>推薦的菜單</h2>
    """
    
    for i, item in enumerate(_top3, 1):
        html += f"""
            <div class="recipe-card">
                <h3>第 {i} 推薦</h3>
                <p><strong>料理：</strong>{item['title']}</p>
                <p><strong>份量：</strong>{item['servings']} | <strong>類型：</strong>{item['dish_type']}</p>
                <p><strong>碳足跡總量：</strong><span class="carbon-info">約 {item['total_carbon']:.2f} kg CO₂e</span></p>
                <p><strong>食材清單：</strong></p>
                <ul>
        """
        for ing in item['ingredients']:
            html += f"<li>{ing['name']}: {ing['amount']} {ing['unit']} (碳足跡: {ing['carbon']} kg)</li>"
        html += """
                </ul>
            </div>
        """
    
    html += """
        </div>
    </body>
    </html>
    """
    
    return html