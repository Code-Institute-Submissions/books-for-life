import os
from flask import (
    Flask, render_template, flash,
    redirect, request, url_for, session)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
if os.path.exists("env.py"):
    import env

# Create an instance of flask and assign it to "app"
app = Flask(__name__)

# Configure and pass to os environment
app.config["MONGO_DBNAME"] = 'book_manager'
app.config['MONGO_URI'] = os.environ['MONGO_URI']

# Configure secret key and pass to os environment
app.secret_key = os.environ.get('SECRET_KEY')

# Connection to MongoDB database
mongo = PyMongo(app)


# Landing page
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


# Search book
@app.route('/reviews')
def reviews():
    reviews = mongo.db.reviews.find()
    return render_template("bookgallery.html", reviews=reviews)


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get("query")
    reviews = mongo.db.reviews.find({"$text": {"$search": query}})
    return render_template("bookgallery.html", reviews=reviews)


# Book gallery
@app.route('/gallery')
def gallery():
    return render_template("bookgallery.html", reviews=mongo.db.reviews.find())


# Add book
@app.route('/book')
def book():
    return render_template("addbook.html")


@app.route('/add_book', methods=['POST'])
def add_book():
    reviews = mongo.db.reviews
    reviews.insert_one(
        {
            'title': request.form.get('title').title(),
            'author': request.form.get('author').title(),
            'description': request.form.get('description'),
            'cover_url': request.form.get('cover_url'),
            'amazon_url': request.form.get('amazon_url')
        }
    )
    flash("Added book successful!")
    return redirect(url_for('gallery'))


# Edit book
@app.route('/edit_review/<review_id>')
def edit_review(review_id):
    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    return render_template("editreview.html", review=review)


# Update book
@app.route('/update_review/<review_id>', methods=["POST"])
def update_review(review_id):
    review = mongo.db.reviews
    review.update({'_id': ObjectId(review_id)},
                  {
        'title': request.form.get('title').title(),
        'author': request.form.get('author').title(),
        'description': request.form.get('description'),
        'cover_url': request.form.get('cover_url'),
        'amazon_url': request.form.get('amazon_url')
    })
    flash("Books successfully updated")
    return redirect(url_for('gallery'))


# Delete book
@app.route('/delete_review/<review_id>')
def delete_review(review_id):
    mongo.db.reviews.delete_one({'_id': ObjectId(review_id)})
    flash("Book successfully deleted")
    return redirect(url_for('gallery'))


# Login user
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("You have successfully logged in {}!".format(
                    request.form.get("username")))
                return redirect(url_for(
                    'gallery', username=session["user"]))

            else:
                flash("Incorrect username or password")
                return redirect(url_for('login'))

        else:
            flash("Incorrect username or password")
            return redirect(url_for('login'))

    return render_template("login.html")


# Signup user
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("signup"))

        signup = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(signup)

        session["user"] = request.form.get("username").lower()
        flash("Signup successful!")
        return redirect(url_for('gallery', username=session["user"]))

    return render_template("signup.html")


# Logout user
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
