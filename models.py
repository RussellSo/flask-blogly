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


