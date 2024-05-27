from flask import Flask, request, render_template
import requests

app = Flask(__name__)

API_KEY = 'INSERT_API_KEY'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recipes', methods=['GET'])
def find_recipes():
    ingredient = request.args.get('ingredient')
    if not ingredient:
        return render_template('index.html', error='No ingredient provided')
    
    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredient}&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code != 200:
        return render_template('index.html', error='Failed to fetch recipes')
    
    recipes = response.json()
    return render_template('index.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)