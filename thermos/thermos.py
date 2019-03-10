import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

from logging import DEBUG
from flask_sqlalchemy import SQLAlchemy

from forms import BookmarkForm



# app config
app = Flask(__name__)
app.logger.setLevel(DEBUG)
#-- app.config is a dict object that holds stuff
app.config['SECRET_KEY'] = '\xa5\xceug\xb2\xb2t\x02\x7f\xa5\x9bD\xc3e\xc1\xbcm\xf2!\x1e\xbaEN\x19'
# 3rd slash if part of filesystem path to db
# basedir = directory from where our app runs
# thermos.db = file where SQL stores data
# __file__ = current file
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#init sqldb (constructor that returns db objects)
#db = db connection & access to functionality of flask_sqlalchemy
db = SQLAlchemy(app)


# Variables
bookmarks = []

# Functions
def store_bookmark(url, description):
    bookmarks.append(dict(
        url = url,
        description = description,
        user = "Jack",
        date = datetime.utcnow()
    ))

def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]



# Inner Classes
class User:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def initials(self):
        return '{}. {}.'.format(self.firstname[0], self.lastname[0])


# Routes & View Functions (controller functions...)
# View Functions have access to request & session objects
@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        title='How to be a Thug',
        text=[
            '1. Eat a lot of bananas', '2. Don\'t play with matches',
            '3. Adopt a kitten'
        ],
        users=[User('Ice', 'Cube'),
               User('Dr', 'Dre'),
               User('Snoop', 'Dogg')
        ],
        new_bookmarks=new_bookmarks(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
    # FlaskWTF extension checks current request contains user input 
    # from the client-side form and adds them to the fields of BookmarkForm()
    # if no user inputs available then fields are blank?
    form = BookmarkForm(request.form)

    # validate_on_submit() checks the HTTP method and validates incoming form
    # false if method = GET or ERROR
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        store_bookmark(url, description)
        flash("Stored '{}'".format(description))
        return redirect(url_for('index'))

    if request.method == "IMPOSSIBLE":
        url = request.form['url']
        store_bookmark(url, 'dummy description')
        flash("stored bookmark: '{}'".format(url))
        app.logger.debug('stored url: ' + url)
        return redirect(url_for('index'))

    app.logger.debug('request.method = ' + request.method)
    #GET or ERROR will render add.html with form variable (which is blank)
    return render_template('add.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)