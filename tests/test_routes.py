from server import app
from datetime import datetime


def test_valid_email():
    with app.test_client() as client:
        response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
        assert response.status_code == 200

def test_invalid_email_redirect():
    with app.test_client() as client:
        response = client.post('/showSummary', data={'email': 'invalid@email.com'}, follow_redirects=True)
        assert b"ERROR : Unknown e-mail" in response.data
        assert response.status_code == 200


def test_display_points_pages() :
    with app.test_client() as client :
        response = client.get('/clubs/points')
        assert response.status_code == 200 
        assert b"Clubs and Points" in response.data
        assert b'Simply Lift' in response.data