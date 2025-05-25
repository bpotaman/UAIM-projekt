import pytest
from app import app, db, User

# TODO: Dodaj więcej testów

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register(client):
    response = client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass'
    })
    assert response.status_code == 201
    assert b'User registered' in response.data

def test_login(client):
    # Najpierw zarejestruj użytkownika
    client.post('/api/register', json={
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': 'testpass'
    })
    # Teraz zaloguj
    response = client.post('/api/login', json={
        'username': 'testuser2',
        'password': 'testpass'
    })
    assert response.status_code == 200
    assert b'Login successful' in response.data