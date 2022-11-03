from . import db #from the current folder/package, I am importing the database (package is website folder)
from flask_login import UserMixin
from sqlalchemy.sql import func #make sql add dates to the notes, func.now will add a now timestamp

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #User as in the class below is python convention, sql will have it as user for foreignkeys

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #this is our primary key, uses integer values
    email = db.Column(db.String(150), unique=True) #string w max length 150 and must be unique
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    notes = db.relationship('Note') # every time we madke a note, add that note id to the user
                                    # foreign keys (user above in Note class) is always lower case, but when you reference the relationship its uppercase
