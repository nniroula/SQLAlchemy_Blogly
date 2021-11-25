from flask import Flask, redirect, render_template, request, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db  # import SQLAlchemy instance and a method
from models import User   # import the class form models.py
# from flask_cors import CORS

app = Flask(__name__) 
# CORS(app)

app.config['SECRET_KEY'] = "nabinbro"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app) 
app.config['SQLALCHEMY_ECHO'] = True  # this helps to display sql tables in ipython terminal with db.create_all()
app.config['SQLALCHEMY_TRACK_MODIFIACTIONS'] = False    # To supress sqlAlchemy message in terminal

# locate your database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///SQLAlchemy_Blogly_db'

# configuration should go before this
connect_db(app)
db.create_all()  # to create all tables

# To test that flask app is up and running correctly
@app.route("/user_list")
def user_list():
    return render_template("user_listing.html")

@app.route('/')      # OK
def home_page():
    # GET /
    # Redirect to list of users. (We’ll fix this in a later step).
    # return redirect("users.html")
    return redirect('/user_list')

@app.route("/users")        # Ok, Incomplete
def list_all_users_in_db():
    # GET /users
    # Show all users.
    # Make these links to view the detail page for the user.   # this means when you click on the user's name, it has to take you to details page
    # Have a link here to the add-user form.  # this is to add user button, DONE in user_lising.html file
    
    get_values_from_db = User.query.all()  # this is a query to get all items in database
    return render_template("user_listing.html", get_values_from_db = get_values_from_db)  

@app.route("/users/new", methods=["GET", "POST"])   # Ok
def get_new_user():
    """add a new user """
    # GET /users/new 
    # Show an add form for users
    if request.method == 'GET':
        return render_template("new_user.html")  # or do redirect('/user_list)

    # POST /users/new
    # Process the add form, adding a new user and going back to /users
    if request.method == 'POST':
        #@app.route("/users/new", methods=["GET", "POST"])
        first_name_from_form = request.form["new-user-first-name"]
        last_name_from_form = request.form["new-user-last-name"]
        image_url_from_form = request.form["image-url"]
        all_users_list = User(first_name = first_name_from_form, last_name = last_name_from_form , image_url = image_url_from_form)
        db.session.add(all_users_list) 
        db.session.commit()

        return redirect("/users")
    
    #3 this is not working
@app.route("/users/<int:user_id>")   # Ok, edit and delete does not work, when you go to the edit page it does not show the information
def show_details_about_user(user_id):
    # GET /users/[user-id]
    # Show information about the given user.
    # Have a button to get to their edit page, and to delete the user.
    singleuser = User.query.get_or_404(user_id)    # becuase User.query.get(user_id) can return None

    # may be redirect to ("/users/{{user_id}}") in html form
    return render_template("user_detail_page.html", singleuser = singleuser) 

@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])   # Stuck here, buttons do not work
def show_edit_page_for_a_user(user_id):
    # GET /users/[user-id]/edit
    # Show the edit page for a user.
    #Have a cancel button that returns to the detail page for a user, and a save button that updates the user.

    if request.method == "GET":
        user = User.query.get_or_404(user_id)
        return render_template("user_edit_page.html", user = user) 

    # POST /users/[user-id]/edit
    # Process the edit form, returning the user to the /users page.
    if request.method == "POST":
        if request.form["cancelling_input"] == 'cancelling':  # info come from name and value attribute
            # Or if value of name attribute in request.form ( here, if 'cancelling_inpt' in request.form)
            return redirect("/user/user_id") 

        if request.form["saving_input"] == 'saving':  # if a button is save, update information
            first_name_update = request.form["update-first"]
            last_name_update = request.form["update-last"]
            image_url_update = request.form["update-url"]
            update_list = User(first_name = first_name_update, last_name = last_name_update , image_url = image_url_update)
            db.seesion.add(update_list) 
            db.session.commit()
            return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    # Delete the user.
    id = User.query.get(user_id) 
    User.query.filter_by(id = user_id).delete()
    db.session.commit()
    
    return redirect("/users") 

