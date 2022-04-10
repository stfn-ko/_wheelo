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
    title = db.Column(db.String(50), nullable=False)
    caption = db.Column(db.Text)
    picture = db.Column(db.String(30))
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
        return f'{self.make_name}'


class Model(db.Model):
    model_id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.Text, nullable=False)
    make_id = db.Column(db.Integer, db.ForeignKey('make.make_id'))
    children = db.relationship("Vehicles")

    def __repr__(self):
        return f'{self.model_name}'


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

    # def __repr__(self):
    #   return f'<Vehicles {self.name}>'

class History(db.Model):
    history_id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    stolen = db.Column(db.Integer, default="false")
    scrapped = db.Column(db.Integer, default="false")
    write_off = db.Column(db.Integer, default="false")
    mileage_disc = db.Column(db.Integer, default="false")
    color_change = db.Column(db.Integer, default="false")
    finance = db.Column(db.Integer, default="false")

    def __repr__(self):
        return f'<History {self.name}>'





class Trade(db.Model):
    trade_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    trade_amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Trade {self.name}>'


class CarReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    caption = db.Column(db.Text)
    image = db.Column(db.Text)
    category = db.Column(db.Text)
    preview_text = db.Column(db.Text)

    def __repr__(self):
        return f'<CarReview {self.name}>'


class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.Text, nullable=False)
    lname = db.Column(db.Text, nullable=False)
    bdate = db.Column(db.DateTime, nullable=False)
    ref_by = db.Column(db.Text)
    property_status = db.Column(db.Text, nullable=False)
    street_address = db.Column(db.Text, nullable=False)
    street_address_l2 = db.Column(db.Text)
    city = db.Column(db.Text)
    state_prov = db.Column(db.Text)
    postal = db.Column(db.Text)
    country = db.Column(db.Text)
    email = db.Column(db.Text, nullable=False)
    ph_num = db.Column(db.Integer, nullable=False)
    hh_ld_amt = db.Column(db.Integer)
    hh_info = db.Column(db.Text)
    health_insurance = db.Column(db.Integer, nullable=False)
    health_insurance_cov = db.Column(db.Integer, nullable=False)
    health_insurance_carr = db.Column(db.Text, nullable=False)
    vehicle_info = db.Column(db.Text, nullable=False)
    vehicle_full_cov = db.Column(db.Integer, nullable=False)
    vehicle_additional = db.Column(db.Text)
    additional_info = db.Column(db.Text)
    insurance_img = db.Column(db.Text)

    def __repr__(self):
        return f'<CarReview {self.name}>'
