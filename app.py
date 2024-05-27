from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)

API_KEY = 'your_spoonacular_api_key'

# Define choices
meats = [
    {"name": "Beef", "image": "beef.jpg"},
    {"name": "Chicken", "image": "chicken.jpg"},
    {"name": "Egg", "image": "egg.jpg"},
    {"name": "Lentil", "image": "lentil.jpg"},
    {"name": "Salmon", "image": "salmon.jpg"},
    {"name": "Tofu", "image": "tofu.jpg"},
    {"name": "Tuna", "image": "tuna.jpg"},
]
veggies = [
    {"name": "Avocado", "image": "avocado.jpg"},
    {"name": "Bell Pepper", "image": "bell_pepper.jpg"},
    {"name": "Bok Choy", "image": "bok_choy.jpg"},
    {"name": "Broccoli", "image": "broccoli.jpg"},
    {"name": "Cabbage", "image": "cabbage.jpg"},
    {"name": "Carrot", "image": "carrot.jpg"},
    {"name": "Cauliflower", "image": "cauliflower.jpg"},
    {"name": "Corn", "image": "corn.jpg"},
    {"name": "Cucumber", "image": "cucumber.jpg"},
    {"name": "Garlic", "image": "garlic.jpg"},
    {"name": "Green Onion", "image": "green_onion.jpg"},
    {"name": "Mushroom", "image": "mushroom.jpg"},
    {"name": "Okra", "image": "okra.jpg"},
    {"name": "Onion", "image": "onion.jpg"},
    {"name": "Spinach", "image": "spinach.jpg"},
    {"name": "Tomato", "image": "tomato.jpg"},
]
carbohydrates = [
    {"name": "Chickpea", "image": "chickpea.jpg"},
    {"name": "Oat", "image": "oat.jpg"},
    {"name": "Pasta", "image": "pasta.jpg"},    
    {"name": "Potato", "image": "rice.jpg"},
    {"name": "Quinoa", "image": "quinoa.jpg"},    
    {"name": "Rice", "image": "rice.jpg"},
    {"name": "Sweet Potato", "image": "sweet_potato.jpg"},    
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
