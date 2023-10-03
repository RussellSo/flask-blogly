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


class PostTag(db.Model):
    """Many tags for many posts"""

    __tablename__ = 'posttag'

    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'),  nullable = 'False', primary_key='True')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable='False', primary_key='True')

    def __repr__(self):
        return f"id: {self.tag_id} name: {self.post_id}"

class Tag(db.Model):
    """one tag"""

    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key='True', autoincrement=True)
    name = db.Column(db.Text, unique=True)

    posttags = db.relationship('Post', secondary="posttag", backref='tag')

    def __repr__(self):
        return f"id: {self.id} name: {self.name}"



## testing
# insert into post tag
# try to use relationship to grab back forth information
# how does it work when i'm creating for a user?
# user creates a post > user creates a tag 
# tag can be assigned to post
# tag list > tag create > tag edit > tag show > edit show post for tags > edit post page for tags
# create tag inserts to...tag 
# edit post for tag inserts into posttag