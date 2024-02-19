from datetime import timedelta
from flask import render_template, request, session, url_for, redirect
import requests
from app import app
from .forms import LoginForm, SignUpForm

app.permanent_session_lifetime = timedelta(minutes=15) 
# ...
# this code sets the duration of session data for 15 minutes, 
# which otherwise is by default 30 days.
# ...
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
            if len(pokemon_catchlist)<6:
                if pokemon_catch_id not in pokemon_catchlist:
                    pokemon_catchlist.append(pokemon_catch_id)
            elif(len(session['pokemon_catchlist'])==6):
                print("Pokemon Catch Limit Already Reached! Try releasing the ones you do not want anymore")
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


@app.route('/pokemonteam')
def pokemonteam():
    pokemon_infolist=[]

    if 'pokemon_catchlist' in session:
        for pokemon in session['pokemon_catchlist']:
            pokemon_in = pokemon_info(pokemon)
            pokemon_infolist.append(pokemon_in)
            # print(pokemon_infolist)
    return render_template('pokemonteam.html', pokemon_infolist=pokemon_infolist)
    
    # elif request.method == 'POST':
        
    #     pokemon_release_id = session.get('pokemon_name_id')
    #     pokemon_list = session['pokemon_catchlist']
    #     if pokemon_list:
    #         pokemon_list.remove(pokemon_release_id)
    #     print(pokemon_list)
    # return render_template('pokemonteam.html', pokemon_list=pokemon_list)

@app.route('/pokemonteam/release/<int:pokemon_id>')
def release_pokemon(pokemon_id):
    print(type(pokemon_id))
    pokemon_list = session['pokemon_catchlist']
    if pokemon_list:
        if pokemon_id in pokemon_list:
            pokemon_list.remove(pokemon_id)
    print(pokemon_list)
    return redirect(url_for('pokemonteam'))

# @app.route('/pokemonteam/release/<int:pokemon_id>')
# def release_pokemon(pokemon_id):
#     print(type(pokemon_id))
    
#     # Convert pokemon_id to integer directly, no need for a separate variable
#     # Ensure that 'pokemon_catchlist' exists in the session
#     if 'pokemon_catchlist' in session:
#         pokemon_list = session['pokemon_catchlist']
        
#         # Check if the Pokemon ID is in the list before attempting to remove
#         if pokemon_id in pokemon_list:
#             pokemon_list.remove(pokemon_id)

#     print(pokemon_list)
#     return redirect(url_for('pokemonteam'))
