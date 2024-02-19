from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def hello():
   return "<p>Hello! Welcome to my bSite</p>"

# @app.route('/user')
# def user():
#     return "<h1> Hello there! User </h1>"


# @app.route('/user/<name>')
# def user(name):
#     return f'Hello! {name}'

# @app.route('/login', methods = ['GET','POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         return f'{email} {password}'
#     return render_template('index.html')

def pokemon_info(my_pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{my_pokemon}'

    response = requests.get(url)

    if response.ok:
        data = response.json()
        poke_dict = {
        'name' :  data['name'],
        'id' : data['id'], 
        'ability' : data['abilities'][0]['ability']['name'],
        'sprite': data['sprites']['front_default']
        }
    print(poke_dict)
    return poke_dict
       
print(pokemon_info(66))

@app.route('/pokemon', methods = ['GET','POST'])
def pokemon():
    if request.method == 'POST':
        pokemon_name_id = request.form.get('pokemon_name_id')
        #print(pokemon_info(pokemon_name_id))
        return pokemon_info(pokemon_name_id) #f'Searched for {pokemon_name_id}'
    return render_template('pokemon copy.html')






