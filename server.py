import json
from flask import Flask,render_template,request,redirect,flash,url_for


# On commence par importer les éléments nécessaire depuis flask (Flask, la méthode servent au rendu du template, la méthode request, la méthode redirect pour les redirections, etc.)
# On définit ensuite loadClubs et loadCompetitions, qui nous serviront à charger les competitions et les clubs dans les constantes du même noms
# On a ensuite toute les routes de l'app. Je n'ai jamais utilisé Flask, mais j'ai l'impression que c'est un petit peu similaire à Django dans la méthode de rendu.
# On indique un endpoint et une méthode HTTP, et dans la fonction render_template, on indique le nom du fichier html, ainsi que les éléments dynamique qui serviront à être display dynamiquement dans le HTML avec une syntaxe Jinja 2

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))