from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    products = db.relationship('Product', backref='seller', lazy='select', cascade='all, delete-orphan')

    def __repr__(self):
        return f"{self.username}"
    

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"{self.title}, {self.price}"
    
