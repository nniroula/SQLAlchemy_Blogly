from flask import Flask

app = Flask(__name__)

# To test that flask app is up and running correctly
@app.route('/')
def home_page():
    return "<h1>Hello SQLALCHEMY Blogly."