import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server import loadClubs, loadCompetitions, find_club_by_email

clubs = loadClubs()

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

