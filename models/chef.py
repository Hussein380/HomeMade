from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from . import db

class Chef(db.Model):
    __tablename__ = 'chefs'

    chef_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(40))
    bio = db.Column(db.String(100))
    profile_picture = db.Column(db.String(255))
    rating = db.Column(db.Float)
    whatsapp = db.Column(db.String(20))
    cuisine_types = db.Column(db.String(255))  # Store as comma-separated values
    location_enabled = db.Column(db.Boolean, default=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    user = db.relationship('User', back_populates='chef')
    dishes = db.relationship('Dishes', back_populates='chef', lazy=True)
    media = db.relationship('Media', back_populates='chef')
    order = db.relationship('Order', back_populates='chef', lazy=True)
    reviews = db.relationship('Review', back_populates='chef', lazy=True)

    def __repr__(self):
        return f"<Chef(chef_id={self.chef_id}, username={self.username})>"
