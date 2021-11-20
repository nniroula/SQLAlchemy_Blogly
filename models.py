from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# models go underneath here

class User(db.Model):
    """ User class """

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
                            unique = False)