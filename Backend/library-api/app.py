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
from apscheduler.schedulers.background import BackgroundScheduler


print(generate_password_hash("testpass"))

# Database config %------------------------------------------------------------------------------------------------------------------------------

db = SQLAlchemy()
mail = Mail()

def send_due_today_reminders():
    today = date.today()
    due_today_loans = Loan.query.filter(
        Loan.due_date == today,
        Loan.return_date == None
    ).all()

    for loan in due_today_loans:
        user = User.query.get(loan.user_id)
        book = Book.query.get(loan.book_id)
        if user and book:
            send_confirmation_email(
                user.email,
                "Dziś mija termin zwrotu książki",
                f"To przypomnienie, że dziś upływa termin zwrotu książki '{book.title}'. Prosimy o jej zwrot w terminie."
                )

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins="http://localhost:3000")
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
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.getenv("SENDER")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PSWD")
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
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
                        'genre': book.genre,
                        'description': book.description,
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
                mimetype='image/jpeg',
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
        send_confirmation_email(
                    data['email'],
                    'Registration successful',
                    f'You have successfuly registered :)'
                )
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
        return jsonify({'message': f'{book} has been successfuly borrowed'}), 201

    @app.route('/api/loans/<int:user_id>', methods=['GET'])
    def get_my_books(user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            return jsonify({'loans': [loan.to_dict() for loan in user.loans]})
        else:
            return jsonify({'error': 'User not found'}), 404

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
    
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=send_due_today_reminders, trigger="cron", hour=8)  # Codziennie o 8:00
    scheduler.start()
    
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
    genre = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200)) # Opis książki
    author = db.Column(db.String(80), nullable=False) # Autor książki
    release_year = db.Column(db.Integer, nullable=False) # Rok wydania
    image = db.Column(db.String(255), nullable=True)
    cover_blob = db.Column(db.LargeBinary, nullable=True)

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

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'loan_date': self.loan_date.isoformat(),
            'due_date': self.due_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'book': {
                'id': self.book.id,
                'title': self.book.title,
                'author': self.book.author,
            }
        }


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

    book1 = Book(
        title="Wiedźmin",
        genre="Fantasy",
        description="The story of Geralt of Rivia, a legendary monster hunter, who travels a magical world full of intrigue, danger, and moral ambiguity.",
        author="Andrzej Sapkowski",
        release_year=1993,
        image="http://localhost:5000/static/covers/cover_wiedzmin.jpg",
        cover_blob=cover_wiedzmin
    )

    with open("static/covers/cover_lalka.jpg", "rb") as f:
        cover_lalka = f.read()

    book2 = Book(
        title="Lalka",
        genre="Novel",
        description="A classic Polish novel by Bolesław Prus, following the tragic love of merchant Stanisław Wokulski for the aristocratic Izabela Łęcka, set against the backdrop of 19th-century Warsaw.",
        author="Bolesław Prus",
        release_year=1890,
        image="http://localhost:5000/static/covers/cover_lalka.jpg",
        cover_blob=cover_lalka
    )
    with open("static/covers/cover_pan_tadeusz.jpg", "rb") as f:
        cover_pan_tadeusz = f.read()

    book3 = Book(
        title="Pan Tadeusz",
        genre="Epic poem",
        description="Adam Mickiewicz’s national epic, depicting the lives and customs of Polish nobility in Lithuania, filled with nostalgia, humor, and the hope for national freedom.",
        author="Adam Mickiewicz",
        release_year=1834,
        image="http://localhost:5000/static/covers/cover_pan_tadeusz.jpg",
        cover_blob=cover_pan_tadeusz
    )

    with open("static/covers/cover_maly_ksiaze.jpg", "rb") as f:
        cover_maly_ksiaze = f.read()

    book4 = Book(
        title="Le Petit Prince",
        genre="Science fantasy",
        description="A poetic tale by Antoine de Saint-Exupéry about a young prince who travels from planet to planet, discovering the wonders and absurdities of the adult world.",
        author="Antoine de Saint-Exupéry",
        release_year=1943,
        image="http://localhost:5000/static/covers/cover_maly_ksiaze",
        cover_blob=cover_maly_ksiaze
    )

    with open("static/covers/cover_1984.jpg", "rb") as f:
        cover_1984 = f.read()

    book5 = Book(
        title="1984",
        genre="Dystopian",
        description="George Orwell’s dystopian masterpiece about a totalitarian regime that uses surveillance, censorship, and propaganda to control every aspect of life.",
        author="George Orwell",
        release_year=1949,
        image="http://localhost:5000/static/covers/cover_1984",
        cover_blob=cover_1984
    )

    with open("static/covers/cover_hanba.jpg", "rb") as f:
        cover_hanba = f.read()

    book6 = Book(
        title="Disgrace",
        genre="Novel",
        description="J.M. Coetzee’s novel about a disgraced professor in post-apartheid South Africa, exploring themes of power, redemption, and societal change.",
        author="John Maxwell Coetzee",
        release_year=1999,
        image="http://localhost:5000/static/covers/cover_hanba",
        cover_blob=cover_hanba
    )

    with open("static/covers/cover_okruchy_dnia.jpg", "rb") as f:
        cover_okruchy_dnia = f.read()

    book7 = Book(
        title="The Remains of the Day",
        genre="Historical novel",
        description="Kazuo Ishiguro’s moving story of an English butler reflecting on his life, loyalty, and missed opportunities in the years before and after World War II.",
        author="Kazuo Ishiguro",
        release_year=1989,
        image="http://localhost:5000/static/covers/cover_okruchy_dnia",
        cover_blob=cover_okruchy_dnia
    )

    with open("static/covers/cover_druzyna_pierscienia.jpg", "rb") as f:
        cover_druzyna_pierscienia = f.read()

    book8 = Book(
        title="The fellowship of the ring",
        genre="Fantasy",
        description="The first part of J.R.R. Tolkien’s epic trilogy, where Frodo Baggins and his companions set out on a perilous quest to destroy the One Ring.",
        author="John Ronald Reuel Tolkien",
        release_year=1954,
        image="http://localhost:5000/static/covers/covercover_druzyna_pierscienia_",
        cover_blob=cover_druzyna_pierscienia
    )

    with open("static/covers/cover_dwie_wieze.jpg", "rb") as f:
        cover_dwie_wieze = f.read()

    book9 = Book(
        title="The Two Towers",
        genre="Fantasy",
        description="The second volume of Tolkien’s The Lord of the Rings, following the divided fellowship as they face new dangers and the growing power of Sauron.",
        author="John Ronald Reuel Tolkien",
        release_year=1954,
        image="http://localhost:5000/static/covers/cover_dwie_wieze",
        cover_blob=cover_dwie_wieze
    )

    with open("static/covers/cover_powrot_krola.jpg", "rb") as f:
        cover_powrot_krola = f.read()

    book10 = Book(
        title="The Return of the King",
        genre="Fantasy",
        description="The final part of The Lord of the Rings trilogy, where the forces of good make their last stand against evil and the fate of Middle-earth is decided.",
        author="John Ronald Reuel Tolkien",
        release_year=1955,
        image="http://localhost:5000/static/covers/cover_powrot_krola",
        cover_blob=cover_powrot_krola
    )

    with open("static/covers/cover_hobbit.jpg", "rb") as f:
        cover_hobbit = f.read()

    book11 = Book(
        title="The Hobbit",
        genre="Fantasy",
        description="The enchanting prelude to The Lord of the Rings, telling the adventure of Bilbo Baggins as he joins a group of dwarves on a quest to reclaim their homeland from a dragon.",
        author="John Ronald Reuel Tolkien",
        release_year=1937,
        image="http://localhost:5000/static/covers/cover_hobbit",
        cover_blob=cover_hobbit
    )

    db.session.add_all([book1, book2, book3, book4, book5, book6, book7, book8, book9, book10, book11])
    db.session.commit()

# Mail Functions %-----------------------------------------------------------------------------------------------------------------------------------

def send_confirmation_email(user_email, subject, body):
    msg = Message(subject, sender=os.getenv("SENDER"),recipients=[user_email], body=body)
    mail.send(msg)




# TODO: dorób wysyłanie przypomnień o terminie zwrotu książki

# Main %---------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # db.drop_all()
        # db.create_all()
        populate_db()
    app.run(host="0.0.0.0", debug=True)