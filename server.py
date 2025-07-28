import json
import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask,render_template,request,redirect,flash,url_for
from utils.utils import (
    find_club_by_name,
    find_club_by_email,
    find_competition_by_name,
    is_valid_places_input,
    exceed_club_points,
    exceed_available_places,
    is_competition_in_past,
    loadClubs,
    loadCompetitions
)


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form["email"]
    matched_club = find_club_by_email(email= email, clubs=clubs)
    if matched_club is None: 
        flash("ERROR : Unknown e-mail")
        return redirect(url_for('index'))
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
    competition_name = request.form['competition']
    competition = find_competition_by_name(name = competition_name)
    club_name = request.form["club"]
    club = find_club_by_name(club_name=club_name)
    competition_date= datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    places_str = request.form['places']
    placesRequired = int(places_str)
    club_available_points = int(club['points'])
    print("club_available_points :::>" , club_available_points)
    competition_available_places = int(competition['numberOfPlaces'])
    if not is_valid_places_input(places_input=places_str): 
        flash('Please enter a valid number of places.')
        return redirect(url_for('book', club=club_name, competition=competition_name))
    if exceed_available_places(required_places=placesRequired, available_places=competition_available_places): 
            flash("ERROR: You can not book more places than available")
            return redirect(url_for('book', club=club_name, competition=competition_name))
    if exceed_club_points(required_places=placesRequired, club_available_points=club_available_points): 
            flash("ERROR: You do not have enough points to book these places.")
            return redirect(url_for('book', club=club_name, competition=competition_name))
    if placesRequired > 12: 
        flash("ERROR: You can not book more than 12 places")
        return redirect(url_for('book', club=club_name, competition=competition_name))
    if is_competition_in_past(competition_date=competition_date): 
        flash("ERROR: This competition is not available anymore... Sorry")
        return redirect(url_for('book', club=club_name, competition=competition_name))
    competition['numberOfPlaces'] = competition_available_places - placesRequired
    print("Updated numberOfPlaces:", competition['numberOfPlaces'])
    competition['numberOfPlaces'] = competition_available_places-placesRequired
    club["points"] = club_available_points - placesRequired
    flash('Great-booking complete!')
    # Mettre à jour la compétition dans la liste globale
    for i, c in enumerate(competitions):
        if c['name'] == competition['name']:
            competitions[i] = competition
            break
    return render_template('welcome.html', club=club, competitions=competitions)



# TODO: Add route for points display
@app.route('/clubs/points', methods=['GET'])
def displayPoints():
    return render_template('points.html', clubs = clubs)
    pass

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)