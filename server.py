import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask,render_template,request,redirect,flash,url_for


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
    print("\n \n On est dans le showSummary : \n")
    email = request.form["email"]
    matched_club = find_club_by_email(email= email, clubs=clubs)
    if matched_club is None: 
        flash("ERROR : Unknown e-mail")
        return redirect(url_for('index'))
    print("matched_club : ", matched_club)
    return render_template('welcome.html', club=matched_club ,competitions=competitions)


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



def find_club_by_email(email, clubs):
    return next((club for club in clubs if club["email"] == email), None)
    # return matched_club

