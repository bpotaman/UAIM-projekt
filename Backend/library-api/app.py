import os
import io
from flask import Flask, jsonify, request, send_file, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from dotenv import load_dotenv
import errno


print(generate_password_hash("testpass"))

# Database config %------------------------------------------------------------------------------------------------------------------------------

db = SQLAlchemy()
mail = Mail()

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:UETuCwPapitksT9qmu3Y@localhost:5432/biblioteka'
    )

    if os.path.exists(".env"):
        load_dotenv()
    else:
        raise FileNotFoundError(
        errno.ENOENT, os.strerror(errno.ENOENT), ".env")

    SECRET_KEY = os.getenv("SECRET_KEY")

    app.config['COMMIT_ON_TEARDOWN'] = True
    app.config['MAIL_SERVER'] = 'smtp.example.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'your@email.com'
    app.config['MAIL_PASSWORD'] = 'yourpassword'
    app.config['MAIL_USE_TLS'] = True
    app.config["JWT_SECRET_KEY"] = SECRET_KEY
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    jwt = JWTManager(app)

    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    mail.init_app(app)
    # Routes %---------------------------------------------------------------------------------------------------------------------------------------

    # TODO: Dodaj stronę główną api, nic ambitnego

    @app.route('/')
    def index():
        return jsonify({'message': 'Welcome to the BookNest public library API!'})

    # App context %----------------------------------------------------------------------------------------------------------------------------------

    # TODO: zmień tutaj maina na coś co będzie lepiej działało w dockerze

    # @app.shell_context_processor
    # def make_shell_context():
    #     return {'db': db, 'User': User, 'Book': Book, 'Loan': Loan}
    
    # API Functions %--------------------------------------------------------------------------------------------------------------------------------

    @app.route('/api/books', methods=['GET'])
    def get_books():
        """
        Endpoint zwracający listę książek.
        """
        author = request.args.get('author')
        title = request.args.get('title')
        year = request.args.get('year')
        query = Book.query
        if author:
            query = query.filter(Book.author.ilike(f'%{author}%'))
        if title:
            query = query.filter(Book.title.ilike(f'%{title}%'))
        if year:
            query = query.filter_by(release_year=year)
        books = Book.query.all()
        return jsonify([{'id': book.id,
                        'title': book.title,
                        'author': book.author,
                        'release_year': book.release_year,
                        'image': book.image
                        } for book in books])
    
    @app.route('/api/books/<int:book_id>/cover')
    def get_book_cover(book_id):
        book = Book.query.get_or_404(book_id)
        if book.cover_blob:
            return send_file(
                io.BytesIO(book.cover_blob),
                mimetype='image/jpeg',  # lub image/png, jeśli taki format trzymasz
                as_attachment=False,
                download_name=f"cover_{book_id}.jpg"
            )
        return jsonify({'error': 'No cover'}), 404


    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.get_json()
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        response = jsonify({'message': 'User registered'})
        return response, 201

    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            additional_claims = {"username": user.username}
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            response = jsonify(access_token=access_token)
            return response, 200
        return jsonify({'message': 'Invalid credentials'}), 401
        
    
    @app.route("/api/auth/check")
    def auth_check():
        if "username" in session:
            return jsonify({'authenticated': True, 'username': session['username']})
        return jsonify({'authenticated': False}), 401

    @app.route('/api/loans', methods=['POST'])
    def borrow_book():
        data = request.get_json()
        loan = Loan(
            user_id=data['user_id'],
            book_id=data['book_id'],
            loan_date=date.today(),
            due_date=data['due_date']
        )
        db.session.add(loan)
        db.session.commit()
        user = User.query.get(data['user_id'])
        book = Book.query.get(data['book_id'])
        if user and book:
            send_confirmation_email(
                user.email,
                'Book Succesfully Borrowed',
                f'You have borrowed "{book.title}" by {book.author}. Due date: {loan.due_date}. Do not forget to return it on time!'
            )
        return jsonify({'message': 'Book borrowed'}), 201

    @app.route('/api/loans/<int:loan_id>/return', methods=['PUT'])
    def return_book(loan_id):
        loan = Loan.query.get(loan_id)
        if loan:
            loan.return_date = date.today()
            db.session.commit()
            user = User.query.get(loan.user_id)
            book = Book.query.get(loan.book_id)
            if user and book:
                send_confirmation_email(
                    user.email,
                    'Book Successfully Returned',
                    f'You have returned "{book.title}" by {book.author}. Thank you for visiting BookNest public library! Please leave a review!'
                )
            return jsonify({'message': 'Book returned'})
        return jsonify({'message': 'Loan not found'}), 404
    
    return app

# Models %-------------------------------------------------------------------------------------------------------------------------------------------

# TODO: 3 modele wydaje się mało, trzeba zdecydować czy to ok

class User(db.Model):
    """
    Model użytkownika biblioteki.
    Przechowuje dane logowania i kontaktowe.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) # Unikalna nazwa użytkownika
    email = db.Column(db.String(120), unique=True, nullable=False) # Unikalny email użytkownika
    password_hash = db.Column(db.Text, nullable=False) # Hasz hasła - hashowany za pomocą scrypt hash algorithm

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
    image = db.Column(db.String(255), nullable=True)
    cover_blob = db.Column(db.LargeBinary, nullable=True)
    # TODO: dodaj pole do przechowywania okładki książki, np. URL do okładki

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


# Database Populate %--------------------------------------------------------------------------------------------------------------------------------

# TODO: Czy w ogóle potrzebujemy tej funkcji? Jak dodamy dane wejściowe?

def populate_db():
    db.drop_all()
    db.create_all()
    

    # Dodaj przykładowych użytkowników
    user1 = User(username="alice", email="alice@example.com")
    user1.set_password("alicepass")
    user2 = User(username="bob", email="bob@example.com")
    user2.set_password("bobpass")
    db.session.add_all([user1, user2])

    # Dodaj przykładowe książki
    with open("static/covers/cover_wiedzmin.jpg", "rb") as f:
        cover_wiedzmin = f.read()
    with open("static/covers/cover_lalka.jpg", "rb") as f:
        cover_lalka = f.read()
    with open("static/covers/cover_pan_tadeusz.jpg", "rb") as f:
        cover_pan_tadeusz = f.read()

    book1 = Book(
        title="Wiedźmin",
        author="Andrzej Sapkowski",
        release_year=1993,
        image="http://localhost:5000/static/covers/cover_wiedzmin.jpg",
        cover_blob=cover_wiedzmin
    )
    book2 = Book(
        title="Lalka",
        author="Bolesław Prus",
        release_year=1890,
        image="http://localhost:5000/static/covers/cover_lalka.jpg",
        cover_blob=cover_lalka
    )
    book3 = Book(
        title="Pan Tadeusz",
        author="Adam Mickiewicz",
        release_year=1834,
        image="http://localhost:5000/static/covers/cover_pan_tadeusz.jpg",
        cover_blob=cover_pan_tadeusz
    )
    db.session.add_all([book1, book2, book3])
    db.session.commit()

# Mail Functions %-----------------------------------------------------------------------------------------------------------------------------------

def send_confirmation_email(user_email, subject, body):
    msg = Message(subject, recipients=[user_email], body=body)
    mail.send(msg)

def send_due_reminders():
    today = date.today()
    overdue_loans = Loan.query.filter(
        Loan.due_date < today,
        Loan.return_date == None
    ).all()
    for loan in overdue_loans:
        user = User.query.get(loan.user_id)
        book = Book.query.get(loan.book_id)
        if user and book:
            send_confirmation_email(
                user.email,
                "Przypomnienie o terminie zwrotu książki",
                f"Przekroczyłeś termin zwrotu książki '{book.title}'. Prosimy o jej zwrot!"
            )

# TODO: dorób wysyłanie przypomnień o terminie zwrotu książki

# Main %---------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # db.drop_all()
        # db.create_all()
        populate_db()
    app.run(host="0.0.0.0", debug=True)