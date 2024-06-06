from datetime import datetime
from corkboard import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    boards = db.relationship('Board', backref='author', passive_deletes=True)
    comments = db.relationship('Comment', backref='author', passive_deletes=True)
    
    
    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
            print(user_id)
        except:
            return None
        return User.query.get(user_id)



    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

 



class Starred(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'board.id', ondelete="CASCADE"), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('board.id', ondelete="CASCADE"), nullable=False)

class Board(db.Model):
    __tablename__ = 'board'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255), nullable=True)  # Adjust the length as needed
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='board', passive_deletes=True)
    likes = db.relationship('Starred', backref='board', passive_deletes=True)