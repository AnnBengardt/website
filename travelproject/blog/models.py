from blog import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), nullable=False, default='default2.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('Post', backref='author', lazy=True)
    tickets = db.relationship('Ticket', backref='consumer', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User: {self.username}"

class Post(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f'Post ID: {self.id}, User ID: {self.user_id}, Date: {self.date}'


class Flight(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    departure = db.Column(db.String(128), nullable=False)
    arrival = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Integer)

    def __init__(self, date, departure, arrival, price):
        self.date = date
        self.departure = departure
        self.arrival = arrival
        self.price = price

    def __repr__(self):
        return f'Flight ID: {self.id}, Date: {self.date}, Departure-Arrival: {self.departure} - {self.arrival}'


class Ticket(db.Model):

    users = db.relationship(User)
    flight = db.relationship(Flight)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))
    date = db.Column(db.DateTime, nullable=False)
    departure = db.Column(db.String(128), nullable=False)
    arrival = db.Column(db.String(128), nullable=False)

    def __init__(self, date, departure, arrival, user_id, flight_id):
        self.date = date
        self.departure = departure
        self.arrival = arrival
        self.user_id = user_id
        self.flight_id = flight_id

    def __repr__(self):
        return f'Ticket ID: {self.id}, User ID: {self.user_id}, Date: {self.date}, Departure-Arrival: {self.departure} - {self.arrival}'