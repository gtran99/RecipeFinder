from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)

API_KEY = 'your_spoonacular_api_key'

# Define choices
meats = [
    {"name": "Chicken", "image": "chicken.jpg"},
    {"name": "Beef", "image": "beef.jpg"},
]
veggies = [
    {"name": "Broccoli", "image": "broccoli.jpg"},
    {"name": "Carrot", "image": "carrot.jpg"},
]
carbohydrates = [
    {"name": "Rice", "image": "rice.jpg"},
    {"name": "Pasta", "image": "pasta.jpg"},
]

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/choose_meat')
def choose_meat():
    return render_template('choice.html', choice_type='Meat', items=meats, next_choice_type='Veggie')

@app.route('/choose_veggie')
def choose_veggie():
    meat_choice = request.args.get('choice')
    return render_template('choice.html', choice_type='Veggie', items=veggies, next_choice_type='Carbohydrate', previous_choice=meat_choice)

@app.route('/choose_carbohydrate')
def choose_carbohydrate():
    meat_choice = request.args.get('choice')
    veggie_choice = request.args.get('previous_choice')
    return render_template('choice.html', choice_type='Carbohydrate', items=carbohydrates, next_choice_type='result', previous_choice=f"{meat_choice},{veggie_choice}")

@app.route('/result')
def result():
    meat_choice, veggie_choice = request.args.get('previous_choice').split(',')
    carbohydrate_choice = request.args.get('choice')
    ingredients = f"{meat_choice},{veggie_choice},{carbohydrate_choice}"

    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code != 200:
        return render_template('result.html', error='Failed to fetch recipes', recipes=[])

    recipes = response.json()
    return render_template('result.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
