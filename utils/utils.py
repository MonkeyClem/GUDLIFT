import json 
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

competitions = loadCompetitions()
clubs = loadClubs()


def find_club_by_name(club_name : str):
    return next((club for club in clubs if club["name"] == club_name))

def find_club_by_email(email, clubs):
    return next((club for club in clubs if club["email"] == email), None)

def find_competition_by_name(name):
    for c in competitions:
        if c["name"] == name:
            return c
    return None

# def find_competition_by_name(name) : 
#     return next((competition for competition in competitions if competition["name"] == name), None)

def is_valid_places_input(places_input):
    try :
        return int(places_input) > 0
    except(ValueError, TypeError): 
        return False

def exceed_available_places(required_places , available_places):
    return required_places > available_places

def exceed_club_points(required_places ,club_available_points, ): 
    return required_places > club_available_points


def is_competition_in_past(competition_date): 
    return competition_date < datetime.now()