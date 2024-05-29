from flask import Flask, request, render_template, redirect, url_for
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

API_KEY = os.getenv("API_KEY")

# Define choices
meats = [
    {"id": 1, "name": "Beef", "image": "beef.jpg"},
    {"id": 2, "name": "Chicken", "image": "chicken.jpg"},
    {"id": 3, "name": "Egg", "image": "egg.jpg"},
    {"id": 4, "name": "Lentil", "image": "lentil.jpg"},
    {"id": 5, "name": "Salmon", "image": "salmon.jpg"},
    {"id": 6, "name": "Tofu", "image": "tofu.jpg"},
    {"id": 7, "name": "Tuna", "image": "tuna.jpg"},
]
veggies = [
    {"id": 1, "name": "Avocado", "image": "avocado.jpg"},
    {"id": 2, "name": "Bell Pepper", "image": "bell_pepper.jpg"},
    {"id": 3, "name": "Bok Choy", "image": "bok_choy.jpg"},
    {"id": 4, "name": "Broccoli", "image": "broccoli.jpg"},
    {"id": 5, "name": "Cabbage", "image": "cabbage.jpg"},
    {"id": 6, "name": "Carrot", "image": "carrot.jpg"},
    {"id": 7, "name": "Cauliflower", "image": "cauliflower.jpg"},
    {"id": 8, "name": "Corn", "image": "corn.jpg"},
    {"id": 9, "name": "Cucumber", "image": "cucumber.jpg"},
    {"id": 10, "name": "Garlic", "image": "garlic.jpg"},
    {"id": 11, "name": "Green Onion", "image": "green_onion.jpg"},
    {"id": 12, "name": "Mushroom", "image": "mushroom.jpg"},
    {"id": 13, "name": "Okra", "image": "okra.jpg"},
    {"id": 14, "name": "Onion", "image": "onion.jpg"},
    {"id": 15, "name": "Spinach", "image": "spinach.jpg"},
    {"id": 16, "name": "Tomato", "image": "tomato.jpg"},
]
carbohydrates = [
    {"id": 1, "name": "Chickpea", "image": "chickpea.jpg"},
    {"id": 2, "name": "Oat", "image": "oat.jpg"},
    {"id": 3, "name": "Pasta", "image": "pasta.jpg"},    
    {"id": 4, "name": "Potato", "image": "rice.jpg"},
    {"id": 5, "name": "Quinoa", "image": "quinoa.jpg"},    
    {"id": 6, "name": "Rice", "image": "rice.jpg"},
    {"id": 7, "name": "Sweet Potato", "image": "sweet_potato.jpg"},    
]

user_choices = {
    "meat": None,
    "veggies": [],
    "carb": None
}

def get_next_id(items):
    if not items:
        return 1
    return max(item["id"] for item in items) + 1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/choose_meat', methods=['GET', 'POST'])
def choose_meat():
    if request.method == 'POST':
        selected_meat = request.form['choice']
        user_choices['meat'] = selected_meat
        return redirect(url_for('choose_veggies'))
    sorted_meats = sorted(meats, key=lambda x: x['name'])
    return render_template('choose_meat.html', items=sorted_meats, item_type='Meat')

@app.route('/choose_veggies', methods=['GET', 'POST'])
def choose_veggies():
    if request.method == 'POST':
        selected_veggies = request.form.getlist('choice')
        user_choices['veggies'] = selected_veggies
        return redirect(url_for('choose_carb'))
    sorted_veggies = sorted(veggies, key=lambda x: x['name'])
    return render_template('choose_veggie.html', items=sorted_veggies, item_type='Veggie')

@app.route('/choose_carb', methods=['GET', 'POST'])
def choose_carb():
    if request.method == 'POST':
        selected_carb = request.form['choice']
        user_choices['carb'] = selected_carb
        return redirect(url_for('show_recipes'))
    sorted_carbohydrates = sorted(carbohydrates, key=lambda x: x['name'])
    return render_template('choose_carb.html', items=sorted_carbohydrates, item_type='Carbohydrate')

@app.route('/show_recipes')
def show_recipes():
    meat = user_choices['meat']
    veggies = user_choices['veggies']
    carb = user_choices['carb']
    
    # Form the query
    ingredients = [meat] + veggies + [carb]
    ingredients_str = ','.join(ingredients)
    
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients_str}&number=10&apiKey={API_KEY}"
    
    response = requests.get(url)
    recipes = response.json()
    
    return render_template('recipes.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)