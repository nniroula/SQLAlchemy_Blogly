from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db  # import SQLAlchemy instance and a method

app = Flask(__name__)

connect_db(app)
db.create_all()  # to create all tables


app.config['SECRET_KEY'] = "nabinbro"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app) 
 
app.config['SQLALCHEMY_ECHO'] = True  # this helps to display sql tables in ipython terminal with db.create_all()
app.config['SQLALCHEMY_TRACK_MODIFIACTIONS'] = False    # To supress sqlAlchemy message in terminal

# locate your database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///SQLAlchemy_Blogly'

# To test that flask app is up and running correctly
@app.route("/user_list")
def user_list():
    return render_template("user_listing.html")

@app.route('/')
def home_page():
    # return redirect("users.html")
    return redirect('/user_list')

@app.route("/users")
def users():
    # GET /users
    # Show all users.

    # Make these links to view the detail page for the user.   # this means when you click on the user's name, it has to take you details page

    # Have a link here to the add-user form.  # this is add user button
    
    return render_template("user_listing.html")  # now this one, we need links here



########################
"""
Make routes for the following:

GET /
Redirect to list of users. (We’ll fix this in a later step).

GET /users
Show all users.

Make these links to view the detail page for the user.

Have a link here to the add-user form.

GET /users/new
Show an add form for users
POST /users/new
Process the add form, adding a new user and going back to /users
GET /users/[user-id]
Show information about the given user.

Have a button to get to their edit page, and to delete the user.

GET /users/[user-id]/edit
Show the edit page for a user.

Have a cancel button that returns to the detail page for a user, and a save button that updates the user.

POST /users/[user-id]/edit
Process the edit form, returning the user to the /users page.
POST /users/[user-id]/delete
Delete the user.
Add Testing
Add python tests to at least 4 of your routes.

"""