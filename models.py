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

    # we need to display first and last name. So, have a function for it
    # @classmethod   # becuase we won't be creating an instance of this class
    # def display_image(self):
    #     return f'{self.image_url}'

    def display_image(self):
        return f'{self.image_url}'

    # @classmethod 
    # def display_first_last_names(cls):
    #     return f"{cls.first_name} {cls.last_name}"

    def display_first_last_names(self):
        return f"{self.first_name} {self.last_name}"

# part 2, add model for Post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime)
    