"""Blogly application."""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post

# export PATH=/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH
app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)
app.config['SECRET_KEY'] = "anything"

app.config['ENV'] = 'development'
app.config['DEBUG'] = True

db.create_all()

@app.route('/users')
def user():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/users/new')
def add_user_page():
    return render_template('add_user.html')

#note: MUST seperate get and post routes
@app.route('/users/new', methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    
    added_user = User(first_name=first_name, last_name=last_name)
    db.session.add(added_user)
    db.session.commit()
    return redirect(f"/users/{added_user.id}") 

#note-problem: form-action has to go to current url
#note-problem2: the post route only works if its recieving something from the post route - in this case...
#note cont: an id had to be passed into the redirect in above, and i had to receive it from the route below, and use it?
@app.route("/users/<int:id>")
def user_detail(id):
    new_user = User.query.get(id)
    posts = Post.query.filter_by(user_id = new_user.id)
    return render_template("user_detail.html", new_user=new_user, posts=posts)

@app.route("/users/<int:id>/edit")
def user_edit_page(id):
    curr_user = User.query.get(id)
    return render_template("edit_user.html", curr_user=curr_user)

@app.route("/users/<int:id>/edit", methods=["POST"])
def user_edit(id):
    curr_user = User.query.get(id)
    new_fname = request.form["first_name"]
    new_lname = request.form["last_name"]

    curr_user.first_name = new_fname
    curr_user.last_name = new_lname
    db.session.commit()
    return redirect("/users/<int:id>")

@app.route("/users/<int:id>/delete", methods=["POST"])
def user_delete(id):
    curr_user = User.query.filter_by(id = id).delete()
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:id>/posts/new', methods = ["GET", "POST"])
def new_post(id):
    curr_user = User.query.get(id)


    if (request.method == 'POST'):
        title = request.form["title"]
        comment = request.form["comment"]
        user_post = Post(title=title, content=comment, user_id= curr_user.id)
        db.session.add(user_post)
        db.session.commit()
        return redirect(f"/users/{id}")
    else:
        return render_template('new_post.html', curr_user=curr_user)

@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    curr_post = Post.query.get(post_id)
    return render_template('post_detail.html', curr_post=curr_post)

# should i have add this to the initial route?
# remember the form should have this route as the action
@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def post_delete(post_id):
    curr_post_user = Post.query.get(post_id).user.id
    curr_post = Post.query.filter_by(id = post_id).delete()
    db.session.commit()
    return redirect(f"/users/{curr_post_user}")

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def post_edit(post_id):
    curr_post = Post.query.get(post_id)

    if (request.method == 'POST'):
        curr_post.title = request.form['title']
        curr_post.content = request.form['comment']
        db.session.commit()

        return redirect(f'/posts/{post_id}')
    else:
        return render_template('post_edit.html', curr_post=curr_post)



##part 2 further study
### **Make a Homepage**
# Change the homepage to a page that shows the 5 most recent posts.

### **Show Friendly Date**
# When listing the posts (on the post index page, the homepage, and the user detail page), show a friendly-looking version of the date, like “May 1, 2015, 10:30 AM”.

# ### **Using Flash Messages for Notifications**
# Use the Flask “flash message” feature to notify about form errors/successful submissions.

# ### **Add a Custom “404 Error Page”**
# Research how to make a custom page that appears when a 404 error happens in Flask. Make such a page.

# ### **Cascade Deletion of User**
# If you try to delete a user that has posts, you’ll get an ***IntegrityError*** — PostgreSQL raises an error because that would leave posts without a valid ***user_id***.
# When a user is deleted, the related posts should be deleted, too.
# You can find help for this at [Cascades](https://docs.sqlalchemy.org/en/latest/orm/cascades.html)>`_
##