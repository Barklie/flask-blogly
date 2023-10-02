"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.config['SECRET_KEY'] = "SECRET!"

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    first_name = db.Column(db.String(20),
                           nullable = False
                           )
    
    last_name = db.Column(db.String(20),
                           nullable = False
                           )
    
    profile_picture = db.Column(db.String(200))

    def update_user(self, new_first_name, new_last_name, new_profile_picture):
        self.first_name = new_first_name
        self.last_name = new_last_name
        self.profile_picture = new_profile_picture