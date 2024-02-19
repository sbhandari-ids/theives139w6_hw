from flask import render_template, request, session
import requests
from app import app
from .forms import LoginForm, SignUpForm

@app.route('/')
def hello():
   return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return f'Hello! {name}'

@app.route('/login', methods = ['GET','POST'])
def login():
    #loginForm = LoginForm()
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        return f'{email} {password}'
    return render_template('login.html', form=form)

@app.route('/signup', methods = ['GET','POST'])
def signup():
    #signUpForm = signUpForm()
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data 
        return f'{username} {email} {password}'
    return render_template('signup.html', form=form)



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
    #print(poke_dict)
    return poke_dict
       
# def pokemon_catch():
#     pokemon_catch_id = session.get['pokemon_name_id']
#     poke_catchlist

# @app.route('/pokemon', methods = ['GET','POST'])
# def pokemon():
#     if request.method == 'POST':
#         pokemon_name_id = request.form.get('pokemon_name_id')
#         #print(pokemon_info(pokemon_name_id))
#         #return pokemon_info(pokemon_name_id) #f'Searched for {pokemon_name_id}'
#         pokemon_deets = pokemon_info(pokemon_name_id)
#         return render_template('pokemon.html', pokemon_deets=pokemon_deets)
#     return render_template('pokemon.html')
 
@app.route('/pokemon', methods = ['GET','POST'])
def pokemon():
    if request.method == 'POST':
        if 'search-btn' in request.form:
            pokemon_name_id = request.form.get('pokemon_name_id')
            session['pokemon_name_id'] = pokemon_name_id
            #print(pokemon_info(pokemon_name_id))
            #return pokemon_info(pokemon_name_id) #f'Searched for {pokemon_name_id}'
            pokemon_deets = pokemon_info(pokemon_name_id)
            
            if pokemon_deets:
                return render_template('pokemon.html', pokemon_deets=pokemon_deets)
            else: 
                return render_template('pokemon.html')
            
            return render_template('pokemon.html')
        elif 'catch-btn' in request.form:
            pokemon_catch_id = session.get('pokemon_name_id')
            #if 'pokemon_catchlist' not in session:
            pokemon_catchlist = session.get('pokemon_catchlist',[])
            pokemon_catchlist.append(pokemon_catch_id)
            session['pokemon_catchlist'] = pokemon_catchlist
                # while(len(session['pokemon_catchlist'])<6):
                #     session['pokemon_catchlist'].append(pokemon_catch_id)
                # if(len(session['pokemon_catchlist'])==6):
                #     print("Pokemon Catch Limit Already Reached! Try releasing the ones you do not need anymore")
                
           # print(pokemon_catch_id, pokemon_catchlist, session['pokemon_catchlist'])
            return render_template('pokemon.html', catch_message = f'Pokemon {pokemon_catch_id} caught!')
        else: return render_template('pokemon.html')
    else:
        return render_template('pokemon.html')


@app.route('/pokemonteam', methods = ['GET','POST'])
def pokemonteam():
    if request.method == 'GET':
        for item in session['pokemon_catchlist']:
            pokemon_deet = pokemon_info(item)
            print(pokemon_deet)
        return render_template('pokemonteam.html', pokemon_deet=pokemon_deet)
    
    elif request.method == 'POST':
        
        pokemon_release_id = session.get('pokemon_name_id')
        session['pokemon_catchlist'].remove(pokemon_release_id)
        print(session['pokemon_catchlist'])
    return render_template('pokemonteam.html')



