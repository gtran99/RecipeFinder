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
    return render_template('choice.html', choice_type='Meat', items=meats, next_choice_type='choose_veggie')

@app.route('/choose_veggie', methods=['GET'])
def choose_veggie():
    meat_choice = request.args.get('choice')
    return render_template('choice.html', choice_type='Veggie', items=veggies, next_choice_type='choose_carbohydrate', previous_choice=meat_choice)

@app.route('/choose_carbohydrate', methods=['GET'])
def choose_carbohydrate():
    meat_choice = request.args.get('previous_choice')
    veggie_choice = request.args.get('choice')
    previous_choices = f"{meat_choice},{veggie_choice}"
    return render_template('choice.html', choice_type='Carbohydrate', items=carbohydrates, next_choice_type='result', previous_choice=previous_choices)

@app.route('/result', methods=['GET'])
def result():
    previous_choices = request.args.get('previous_choice').split(',')
    meat_choice = previous_choices[0]
    veggie_choice = previous_choices[1]
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
