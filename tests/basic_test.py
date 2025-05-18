import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server import loadClubs, loadCompetitions, find_club_by_email, find_competition_by_name, is_valid_places_input, exceed_available_places, exceed_club_points, is_competition_in_past

clubs = loadClubs()
competitions = loadCompetitions()

def test_club_loading(): 
    clubs = loadClubs()
    assert isinstance(clubs, list) , 'list'
    assert len(clubs) > 0 , 'longueur'
    assert 'email' in clubs[0] , 'email'

def test_competitions_loading(): 
    competitions = loadCompetitions()
    assert isinstance(competitions, list), "Competitions n'est pas une liste"
    assert len(competitions) > 0 , 'Competitions à une longueur de 0'
    assert 'name' in competitions[0] , 'competitions[0] na pas de name'


def test_find_club_by_email_valid() : 
    email = "john@simplylift.co"
    result = find_club_by_email(email=email, clubs=clubs)
    assert result is not None


def test_find_club_by_email_invalid() : 
    email = "invalid@gmail.com"
    result = find_club_by_email(email=email, clubs=clubs)
    assert result is None

def test_find_competition_by_name_valid() :
    competition_name = 'Fall Classic'
    result = find_competition_by_name(competition_name)
    assert result is not None 

def test_find_competition_by_name_invalid() :
    competition_name = 'False Classic'
    result = find_competition_by_name(competition_name)
    assert result is None 


def test_is_valid_place_input():
    assert is_valid_places_input("3")
    assert is_valid_places_input(2)
    assert not is_valid_places_input("0")
    assert not is_valid_places_input("-5")
    assert not is_valid_places_input("")
    assert not is_valid_places_input(None)
    assert not is_valid_places_input("abc")

def test_exceeds_available_places():
    assert exceed_available_places(10, 5)
    assert not exceed_available_places(3, 10)

def test_exceeds_club_points():
    assert exceed_club_points(5, 3)
    assert not exceed_club_points(2, 10)


def test_is_competition_in_past():
    past = datetime.now() - timedelta(days=1)
    future = datetime.now() + timedelta(days=1)
    assert is_competition_in_past(past) is True
    assert is_competition_in_past(future) is False