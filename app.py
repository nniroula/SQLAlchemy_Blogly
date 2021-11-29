from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_debugtoolbar import DebugToolbarExtension
# from models import db, connect_db  # import SQLAlchemy instance and a method
from models import User, Post, Tag, PostTag   # import the class from models.py
# from models import User, Post  # import the class from models.py
from models import db, connect_db  # import SQLAlchemy instance and a method
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
    
    get_values_from_db = User.query.all()  # this is a query to get all items in database, it is object you can iterate over
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

        if image_url_from_form != None:
            all_users_list = User(first_name = first_name_from_form, last_name = last_name_from_form , image_url = image_url_from_form)
        else:
            image_url_from_form = User.image_url
            all_users_list = User(first_name = first_name_from_form, last_name = last_name_from_form, image_url = image_url_from_form)

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

# Post Routes

@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])  #add button does not work
def display_form_for_new_post(user_id): 
    # GET /users/[user-id]/posts/new
    # Show form to add a post for that user.
    post_user = User.query.get_or_404(user_id)
    if request.method == "GET":
        return render_template("post_files/new_post.html", post_user = post_user) 
    if request.method == "POST":
        # POST /users/[user-id]/posts/new
        # Handle add form; add post and redirect to the user detail page.
        if request.form["addpost"] == "contentadded":
            title_from_form = request.form['titleinput']
            content_from_form = request.form['cont']
        
        # new_post =  Post( title, conent, user_id)
            new_post_user = Post(title = title_from_form, content = content_from_form)
        
            # flash some messages to show if the form processes successfully to add some content
            db.session.add(new_post_user)
            db.session.commit()
            return redirect (f'/users/{user_id}') # f string b/c user_id is a python variable, not the jinja template variable
        
@app.route("/posts/<int:post_id>")  #It does not render first and last name for BY .............
def show_a_post(post_id):
    # GET /posts/[post-id]
    # Show a post.
    # Show buttons to edit and delete the post.
    get_post = Post.query.get_or_404(post_id)
    return render_template('post_files/show_post.html', get_post = get_post)

@app.route("/post/<int:post_id>/edit", methods = ["GET", "POST"])   # bottons do not work right now
def show_form_to_edit_post(post_id):
    # GET /posts/[post-id]/edit
    # Show form to edit a post, and to cancel (back to user page). 
            # To edit we need to get value from form input value="something"
    user_to_edit = Post.query.get_or_404(post_id)
    if request.method == "GET":
        return render_template("post_files/edit.html", user_to_edit = user_to_edit)
    if request.method == "POSt":
        # POST /posts/[post-id]/edit
        # Handle editing of a post. Redirect back to the post view.
        pass
        # if request.form["editingcontent"] == f"{{user_to_edit.content}}"
        if request.form["editingcontent"] == f"{user_to_edit.content}": # this should be a content for value attribute
            user_to_edit.title = request.form["editing"]
            user_to_edit.content = request.form["editingcontent"]
            db.session.add(user_to_edit)
            db.session.commit()
            return redirect(f'/users/{user_to_edit.user_id}')   # this does not redirect back to post view

@app.route("/posts/<int:post_id>/delete", methods=["POST"])  # this does not work yet
def delete_a_post(post_id):
    # POST /posts/[post-id]/delete
    # Delete the post.
    # Change the User Page
    # Change the user page to show the posts for that user.
    post_to_delete = Post.query.get(post_id)
    post_to_delete.delete(post_to_delete)
    db.session.commit()
    # flash some messgae such as something removed
    return redirect(f"/users/{post_to_delete.user_id}")

# Testing
# Update any broken tests and add more testing

# Part 3    ################################################################################################
# add M2M relationship, especially add tagging feature
