"""Blogly application."""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

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
    return render_template("user_detail.html", new_user=new_user)

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
