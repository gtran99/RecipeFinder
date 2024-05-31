# Recipe Finder

A web application which outputs 10 recipes based on your desired ingredients using the Spoonacular API.

## Setup

1. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

2. Install the dependencies:
   pip install -r requirements.txt

3. Generate your unique API key:
   Go to "https://spoonacular.com/food-api" and grab your API key. Create a .env file and create an API_KEY variable with the value of your API key. (Ex. API_KEY = 'abcdefg').

4. Run the application:
    python app.py
