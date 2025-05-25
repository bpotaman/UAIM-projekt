import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:UETuCwPapitksT9qmu3Y@localhost:5432/biblioteka')
app.config['COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

# Models %-------------------------------------------------------------------------------------------------------------------------------------

class User(db.Model):
    """
    Model użytkownika biblioteki.
    Przechowuje dane logowania i kontaktowe.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) # Unikalna nazwa użytkownika
    email = db.Column(db.String(120), unique=True, nullable=False) # Unikalny email użytkownika
    password_hash = db.Column(db.String(128), nullable=False) # Hasz hasła

    loans = db.relationship('Loan', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Book(db.Model):
    """
    Model książki w bibliotece.
    Przechowuje podstawowe informacje o książce.
    """
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False) # Tytuł książki
    author = db.Column(db.String(80), nullable=False) # Autor książki
    release_year = db.Column(db.Integer, nullable=False) # Rok wydania

    loans = db.relationship('Loan', back_populates='book')

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

class Loan(db.Model):
    """
    Model wypożyczenia książki.
    Przechowuje informacje o tym, kto i kiedy wypożyczył oraz zwrócił książkę.
    """
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    loan_date = db.Column(db.Date, default=date.today, nullable=False) # Data wypożyczenia
    due_date = db.Column(db.Date, nullable=False) # Termin zwrotu
    return_date = db.Column(db.Date, nullable=True) # Data faktycznego zwrotu

    user = db.relationship('User', back_populates='loans')
    book = db.relationship('Book', back_populates='loans')

    def __repr__(self):
        return f'<Loan {self.id}: User {self.user_id} Book {self.book_id}>'


# Database Populate %--------------------------------------------------------------------------------------------------------------------------

def populate_db():
    db.drop_all()
    db.create_all()

# API Functions %------------------------------------------------------------------------------------------------------------------------------

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    Endpoint zwracający listę użytkowników.
    """
    users = User.query.all()
    return jsonify([{'id': user.id,
                     'username': user.username,
                     'email': user.email
                     } for user in users])

@app.route('/api/books', methods=['GET'])
def get_books():
    """
    Endpoint zwracający listę książek.
    """
    books = Book.query.all()
    return jsonify([{'id': book.id,
                     'title': book.title,
                     'author': book.author,
                     'release_year': book.release_year
                     } for book in books])

# Testy %--------------------------------------------------------------------------------------------------------------------------------------

# Routes %-------------------------------------------------------------------------------------------------------------------------------------

# App context and main %-----------------------------------------------------------------------------------------------------------------------

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User, 'Book': Book, 'Loan': Loan}

if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        # db.create_all()
        populate_db()
    app.run(debug=True)