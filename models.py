from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# models go underneath here
default_url = "https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2Fc%2Fc3%2FPython-logo-notext.svg%2F1200px-Python-logo-notext.svg.png&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FPython_(programming_language)&tbnid=aNKixiwLiDxvIM&vet=12ahUKEwj8o9bhmrL0AhVWZM0KHZ8zDFQQMygAegUIARDSAQ..i&docid=3wRBXLyvECcz0M&w=1200&h=1200&itg=1&q=python%20programming%20language%20images&client=safari&ved=2ahUKEwj8o9bhmrL0AhVWZM0KHZ8zDFQQMygAegUIARDSAQ"

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