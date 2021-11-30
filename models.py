from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# models go underneath here
default_url = "https://cs.cheggcdn.com/covers2/64370000/64371514_1534275794_Width288.jpg"

class User(db.Model):
    """ User class. Model defines virtual sql tables """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.String(50),
                            nullable = False,
                            unique = False)      # note on unique = True
    last_name = db.Column(db.String(50),
                            nullable = False,
                            unique = False)
    image_url = db.Column(db.Text,
                            nullable = False,
                            default = default_url)   # put default image url
    # reference Post model class
    reference_post = db.relationship('Post')  # with backref you can reference in only one class, and SQLAlchemy references for both via used vairable
                                                # ref = db.relationships('Post', backref = 'references')
    # we need to display first and last name. So, have a function for it

    def display_image(self):
        return f'{self.image_url}'

    def display_first_last_names(self):
        return f"{self.first_name} {self.last_name}"

# part 2, add model for Post
class Post(db.Model):
    __tablename__ = "post_table"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime)    # nullable = False,   default = datetime.datetime.now)
    # need to reference model class User
    reference_to_user = db.relationship('User') # with backref you can reference in only one class, and SQLAlchemy references for both via used vairable

# Part, M2M relationsips and composite primary key

class PostTag(db.Model):
    __tablename__ = "postTagsTable"

    post_id = db.Column(db.Integer,  db.ForeignKey('post_table.id'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tagsTable.id'), primary_key = True)

class Tag(db.Model):
    __tablename__ = "tagsTable"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable = False, unique = True) 
    # through_relationship = db.relationship('Post', secondary = "postTagRelation", backref = "postAndTag")
    through_relationship = db.relationship('Post', secondary = "postTagsTable", backref = "postAndTag")