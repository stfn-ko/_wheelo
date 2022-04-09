import jwt
from time import time
from app import db, login
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from flask_login import LoginManager  # new code entry
from werkzeug.security import generate_password_hash, check_password_hash

# timestamp to be inherited by other class models


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


@login.user_loader  # new code entry
def load_user(id):  # new code entry
    # new code entry --- # slightly modified such that the user is loaded based on the id in the db
    return User.query.get(int(id))

# user class


class User(db.Model, TimestampMixin, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    admin = db.Column(db.Integer, default=0)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    #vehicles = db.relationship('Vehicle', backref='user', lazy='dynamic')

    # print to console username created
    def __repr__(self):
        return f'<User {self.username}>'
    # generate user password i.e. hashing

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    # check user password is correct

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # for reseting a user password

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')
    # verify token generated for resetting password

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Post(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Post {self.name}>'


class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    display = db.Column(db.Integer, default=0)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)

    def __repr__(self):
        return f'<FAQ {self.title}>'



class Make(db.Model):
    make_id = db.Column(db.Integer, primary_key=True)
    make_name = db.Column(db.Text, nullable=False)
    children = db.relationship("Vehicles")

    def __repr__(self):
        return f'<Make {self.name}>'


class Model(db.Model):
    model_id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.Text, nullable=False)
    make_id = db.Column(db.Integer, db.ForeignKey('make.make_id'))
    children = db.relationship("Vehicles")


    def __repr__(self):
        return f'<Model {self.name}>'


class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make_id = db.Column(db.Integer, db.ForeignKey('make.make_id'))
    model_id = db.Column(db.Integer, db.ForeignKey('model.model_id'))
    price = db.Column(db.Integer)
    year = db.Column(db.Integer)
    color = db.Column(db.Text)
    description = db.Column(db.Text)
    pictures = db.Column(db.Text)
    popular = db.Column(db.Text)
    mileage = db.Column(db.Integer)
    fuel_type = db.Column(db.Text)
    gear_type = db.Column(db.Text)

    def __repr__(self):
        return f'<Vehicles {self.name}>'
