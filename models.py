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

    posts = db.relationship('Post', backref='User')



    def update_user(self, new_first_name, new_last_name, new_profile_picture):
        self.first_name = new_first_name
        self.last_name = new_last_name
        self.profile_picture = new_profile_picture

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,  
                   primary_key=True,
                   autoincrement=True)
    
    post_title = db.Column(db.String(25),
                           nullable=False,
                           )
    post_content = db.Column(db.String(250),
                           nullable=False,
                           )
    posters_id = db.Column(db.Integer,
                           db.ForeignKey('users.id'))
    
    def update_post(self, new_title, new_content):
        self.post_title = new_title
        self.post_content = new_content