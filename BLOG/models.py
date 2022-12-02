from . import db
from flask_login import UserMixin, current_user
from sqlalchemy.dialects.mysql import TEXT

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(50) , unique = True)
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))
    blog = db.relationship('Blog')


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150) )
    data = db.Column(TEXT)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id) )
