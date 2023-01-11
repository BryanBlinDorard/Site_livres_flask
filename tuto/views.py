from .app import app
from flask import render_template
from .models import *

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

from flask import url_for, redirect
from .app import db
from .models import Author

from wtforms import PasswordField
from .models import User
from hashlib import sha256

from flask_login import login_user, current_user, logout_user, login_required
from flask import request


@app.route("/")
def home():
    return render_template("home.html", title="My Books!", books=get_sample())

@app.route("/detail/<id>")
def detail(id):
    books = get_sample()
    book = books[int(id)-1]
    author_id = get_author_of_book(id)
    author_name = get_name_author(author_id)
    return render_template("detail.html", book=book, author_id=author_name)

@app.route("/author")
def home2():
    return render_template("author.html", title="Tous les auteurs :", authors=get_all_author())

@app.route("/book_author/<id>")
def book_author(id):
    return render_template("book_author.html", title="My Books!", name=get_name_author(id) , books=get_all_books_for_author(id), nb_book=nb_livres_author(id))

class AuthorForm(FlaskForm):
    id = HiddenField()
    name = StringField('Name', validators=[DataRequired()])

@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id):
    author = get_author(id)
    form = AuthorForm(id=author.id, name=author.name)
    return render_template("edit_author.html", author=author, form=form)

@app.route("/save/author/", methods=("POST",))
@login_required
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        a = get_author(id)
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for("book_author", id=a.id))
    a = get_author(int(f.id.data))
    return render_template("edit_author.html", author=a, form=f)

@app.route("/add/author/", methods=("POST","GET"))
@login_required
def add_author():
    f= AuthorForm()
    return render_template("add_author.html", form=f)


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField()

    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

@app.route("/login/", methods=("POST", "GET"))
def login():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get('next')
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for('home')
            return redirect(next)
    return render_template("login.html", form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/user/bibliotheque/<string:username>")
@login_required
def bibliotheque_user(username):
    return render_template("bibliotheque.html", user=get_user(username))