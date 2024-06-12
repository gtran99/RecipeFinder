from flask import Flask, request, render_template, redirect, url_for
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

SPOONACULAR_API_KEY = os.getenv("API_KEY")

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
    return render_template('choose_veggies.html', items=sorted_veggies, item_type='Veggie')

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
    ingredients_str = ', '.join(ingredients)
    
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients_str}&number=10&apiKey={SPOONACULAR_API_KEY}"
    
    response = requests.get(url)
    recipes = response.json()
    
    return render_template('recipes.html', recipes=recipes, ingredients_str=ingredients_str)

@app.route('/meats')
def list_meats():
    sorted_meats = sorted(meats, key=lambda x: x['name'])
    return render_template('list.html', items=sorted_meats, item_type='Meat')

@app.route('/meats/add', methods=['GET', 'POST'])
def add_meat():
    if request.method == 'POST':
        new_meat = {
            "id": get_next_id(meats),
            "name": request.form['name'],
            "image": request.form['image']
        }
        meats.append(new_meat)
        return redirect(url_for('list_meats'))
    return render_template('add.html', item_type='Meat')

@app.route('/meats/edit/<int:id>', methods=['GET', 'POST'])
def edit_meat(id):
    meat = next((m for m in meats if m['id'] == id), None)
    if request.method == 'POST' and meat:
        meat['name'] = request.form['name']
        meat['image'] = request.form['image']
        return redirect(url_for('list_meats'))
    return render_template('edit.html', item=meat, item_type='Meat')

@app.route('/meats/delete/<int:id>', methods=['POST'])
def delete_meat(id):
    global meats
    meats = [m for m in meats if m['id'] != id]
    return redirect(url_for('list_meats'))

# Repeat similar CRUD routes for veggies and carbohydrates

@app.route('/veggies')
def list_veggies():
    sorted_veggies = sorted(veggies, key=lambda x: x['name'])
    return render_template('list.html', items=sorted_veggies, item_type='Veggie')

@app.route('/veggies/add', methods=['GET', 'POST'])
def add_veggie():
    if request.method == 'POST':
        new_veggie = {
            "id": get_next_id(veggies),
            "name": request.form['name'],
            "image": request.form['image']
        }
        veggies.append(new_veggie)
        return redirect(url_for('list_veggies'))
    return render_template('add.html', item_type='Veggie')

@app.route('/veggies/edit/<int:id>', methods=['GET', 'POST'])
def edit_veggie(id):
    veggie = next((v for v in veggies if v['id'] == id), None)
    if request.method == 'POST' and veggie:
        veggie['name'] = request.form['name']
        veggie['image'] = request.form['image']
        return redirect(url_for('list_veggies'))
    return render_template('edit.html', item=veggie, item_type='Veggie')

@app.route('/veggies/delete/<int:id>', methods=['POST'])
def delete_veggie(id):
    global veggies
    veggies = [v for v in veggies if v['id'] != id]
    return redirect(url_for('list_veggies'))

@app.route('/carbohydrates')
def list_carbohydrates():
    sorted_carbohydrates = sorted(carbohydrates, key=lambda x: x['name'])
    return render_template('list.html', items=sorted_carbohydrates, item_type='Carbohydrate')

@app.route('/carbohydrates/add', methods=['GET', 'POST'])
def add_carbohydrate():
    if request.method == 'POST':
        new_carb = {
            "id": get_next_id(carbohydrates),
            "name": request.form['name'],
            "image": request.form['image']
        }
        carbohydrates.append(new_carb)
        return redirect(url_for('list_carbohydrates'))
    return render_template('add.html', item_type='Carbohydrate')

@app.route('/carbohydrates/edit/<int:id>', methods=['GET', 'POST'])
def edit_carbohydrate(id):
    carbohydrate = next((c for c in carbohydrates if c['id'] == id), None)
    if request.method == 'POST' and carbohydrate:
        carbohydrate['name'] = request.form['name']
        carbohydrate['image'] = request.form['image']
        return redirect(url_for('list_carbohydrates'))
    return render_template('edit.html', item=carbohydrate, item_type='Carbohydrate')

@app.route('/carbohydrates/delete/<int:id>', methods=['POST'])
def delete_carbohydrate(id):
    global carbohydrates
    carbohydrates = [c for c in carbohydrates if c['id'] != id]
    return redirect(url_for('list_carbohydrates'))

if __name__ == '__main__':
    app.run(debug=True)