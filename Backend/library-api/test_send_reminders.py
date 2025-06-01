import pytest
from datetime import date
from flask import Flask
from unittest.mock import patch

from app import create_app, db, User, Book, Loan, send_due_today_reminders

@pytest.fixture
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'MAIL_SUPPRESS_SEND': True,
        'SECRET_KEY': 'test',
        'MAIL_SERVER': 'smtp.test.com',
        'MAIL_PORT': 587,
        'MAIL_USERNAME': 'test@test.com',
        'MAIL_PASSWORD': 'password',
        'MAIL_USE_TLS': True,
        'MAIL_USE_SSL': False,
    }

    app = create_app(test_config)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def setup_due_loan(app):
    with app.app_context():
        user = User(username='janedoe', email='jane@example.com')
        user.set_password('testpass')
        db.session.add(user)

        book = Book(title='Test Book', genre='Test', author='Author', release_year=2020, description='Desc')
        db.session.add(book)
        db.session.commit()

        loan = Loan(
            user_id=user.id,
            book_id=book.id,
            loan_date=date.today(),
            due_date=date.today()
        )
        db.session.add(loan)
        db.session.commit()
        return loan

def test_send_due_today_reminders_sends_email(app, setup_due_loan):
    with app.app_context(), patch('app.send_confirmation_email') as mock_send_email:
        send_due_today_reminders()
        mock_send_email.assert_called_once()
        args = mock_send_email.call_args[0]
        assert args[0] == 'jane@example.com'
        assert 'Dziś mija termin zwrotu' in args[1]
        assert 'Test Book' in args[2]
