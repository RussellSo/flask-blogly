from flask_sqlalchemy import SQLAlchemy

"""Models for Blogly."""
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ user created """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key='True', autoincrement=True)
    first_name = db.Column(db.Text, nullable="False")
    last_name = db.Column(db.Text, nullable="False")
    image_url = db.Column(db.Text)


class Post(db.Model):
    """ Many posts for one user"""


    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key="True", autoincrement=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable='False', default='09-24-2023')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable='False')

    user = db.relationship('User', backref='post')

# date time
# Create post class
# make route to save into db