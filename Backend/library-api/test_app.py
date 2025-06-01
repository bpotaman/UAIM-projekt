import pytest
from app import create_app, db

# TODO: Dodaj więcej testów

@pytest.fixture
def client():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200

def test_register(client):
    response = client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass'
    })
    assert response.status_code == 201
    assert b'User registered' in response.data

def test_login(client):
    client.post('/api/register', json={
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': 'testpass'
    })
    response = client.post('/api/login', json={
        'username': 'testuser2',
        'password': 'testpass'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
