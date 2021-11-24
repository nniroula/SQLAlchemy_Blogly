from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# models go underneath here

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
    image_url = db.Column(db.String,
                            nullable = False,
                            unique = False)   # put default image url

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