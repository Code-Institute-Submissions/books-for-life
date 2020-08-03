import os
from flask import Flask, render_template, flash, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
"""
from forms import LoginForm, RegistrationForm
from flask_login import (
    LoginManager, current_user, login_user,
    logout_user, login_required)
from werkzeug.security import generate_password_hash, check_password_hash
"""
from os import path
if os.path.exists("env.py"):
    import env 


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('You have been logged in!', 'success')
        return redirect(url_for('gallery'))
    else:
        flash('Login unsuccessful. Please try again', 'danger')
        return render_template("login.html", title='Sign In', form=form)

@app.route('/reviews')
def reviews():
    reviews = mongo.db.reviews.find()
    return render_template("reviews.html", reviews=reviews)


@app.route('/gallery')
def gallery():
    return render_template("bookgallery.html")


@app.route('/users')
def users():
    users = mongo.db.users.find()
    return render_template("users.html", users=users)


@app.route('/book')
def book():
    return render_template("addbook.html")

@app.route('/book/add')
def add_book():
    return render_template("bookgallery.html")

@app.route('/book/edit/<book_id>')
def edit_book(book_id):
    return render_template("addbook.html", book=book_id)

@app.route('/book/delete/<book_id>')
def delete_book(book_id):
    mongo.db.books.remove({'_id': ObjectId(book_id)})
    flash(('The book has been successfully deleted').format(book_id), 'success')
    return render_template("bookgallery.html")

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been successfully logged out!', 'success')
    return redirect(url_for('landing_page'))

@app.route('/signup') #, methods=['GET', 'POST'])
def signup():
    #form = RegisterForm()
    #if form.validate_on_submit():
        return render_template("signup.html") #, form=form)
        # return redirect(url_for('book_gallery'))


@app.route('/account')
def account():
    return render_template("personalaccount.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)

