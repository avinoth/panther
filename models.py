from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(60), index = True)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    comments = db.relationship('Comment', backref = 'commenter', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


    def __repr__(self):
        return '<User %r>' % (self.name)
    
    def __init__(self , name ,email , password):
        self.name = name
        self.email = email
        self.password = password


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(1400))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref = 'parentpost', lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % (self.title)
        
#     def __init__(self , title ,body, timestamp):
#         self.title = title
#         self.body = body
#         self.timestamp = timestamp
        
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    commenter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(140))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    
#     def __init__(self , content):
#         self.content = content
        
    def __repr__(self):
        return '<Post %r>' % (self.content)
    
