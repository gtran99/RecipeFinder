from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)

API_KEY = '9fef2bcf72ac484b9d215f06f971bc0c'

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
# Utility function to find next id
def get_next_id(items):
    if not items:
        return 1
    return max(item["id"] for item in items) + 1

@app.route('/')
def home():
    return render_template('index.html')

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
        new_carbohydrate = {
            "id": get_next_id(carbohydrates),
            "name": request.form['name'],
            "image": request.form['image']
        }
        carbohydrates.append(new_carbohydrate)
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

# Existing routes for recipe finding
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
    veggie_choices = request.args.get('choices', '')
    previous_choices = f"{meat_choice},{veggie_choices}"
    return render_template('choice.html', choice_type='Carbohydrate', items=carbohydrates, next_choice_type='result', previous_choice=previous_choices)

@app.route('/result', methods=['GET'])
def result():
    previous_choices = request.args.get('previous_choice').split(',')
    meat_choice = previous_choices[0]
    veggie_choices = previous_choices[1:-1]  # Collect all middle elements as veggies
    carbohydrate_choice = previous_choices[-1]

    # Join veggie choices into a single string for the API request
    veggie_choices_str = ','.join(veggie_choices)
    ingredients = f"{meat_choice},{veggie_choices_str},{carbohydrate_choice}"

    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code != 200:
        return render_template('result.html', error='Failed to fetch recipes', recipes=[])

    recipes = response.json()
    return render_template('result.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)