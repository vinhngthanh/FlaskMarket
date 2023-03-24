from flask_login import UserMixin
from . import db
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    products = db.relationship('Product', backref='seller', lazy='select', cascade='all, delete-orphan')

    def __repr__(self):
        return f"{self.username}"
    
    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"{self.title}, {self.price}"
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))