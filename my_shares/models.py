from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from datetime import datetime
from my_shares import login_manager, db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    password_hash = Column(String(128))
    cash = Column(Float(16), default=10000)
    portfolio = relationship('Portfolio', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    symbol = Column(String(16))
    name = Column(String(64))
    shares = Column(Integer)
    transaction_time = Column(DateTime(64), default=datetime.now())
    transaction_type = Column(String(16), default=None)
    price = Column(Float(32))
    total = Column(Float(16))

    def __init__(self, user_id, symbol, name, shares, transaction_type, price, total):
        self.user_id = user_id
        self.symbol = symbol
        self.name = name
        self.shares = shares
        self.transaction_type = transaction_type
        self.price = price
        self.total = total

    def __repr__(self):
        return f"{self.symbol} - {self.shares} - {self.transaction_type} - {self.price} {self.total}"
