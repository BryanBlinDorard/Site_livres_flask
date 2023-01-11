from .app import db, login_manager
from flask_login import UserMixin

class Author(db.Model):
    __tablename__ = "Author"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return "Author (%d, %s)" % (self.id, self.name)

relationUserBook = db.Table("relationUserBook", 
    db.Column("username", db.String(100), db.ForeignKey("User.username"), primary_key=True),
    db.Column("id_livre", db.Integer, db.ForeignKey("Book.id"), primary_key=True)
)

class Book(db.Model):
    __tablename__ = "Book"

    id = db.Column(db.Integer,primary_key=True)
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    img = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('Author.id'))
    author = db.relationship('Author', backref=db.backref('books', lazy='dynamic'))

    def __repr__(self):
        return "Book (%d, %s)" % (self.id, self.title)

class User(db.Model, UserMixin):
    __tablename__ = "User"

    username = db.Column(db.String(100),primary_key=True)
    password = db.Column(db.String(100))
    livres = db.relationship("Book", secondary=relationUserBook, lazy="subquery", backref=db.backref("users", lazy=True))

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password


    def __repr__(self):
        return "User (%s, %s)" % (self.username, self.password)

    def get_id(self):
        return self.username

    def get_password(self):
        return self.password

def get_sample():
    return Book.query.all()

def get_livre(id):
    return Book.query.get(id)

## INFO AUTHOR 
def get_all_author():
    return Author.query.all()

def get_all_books_for_author(id):
    return Book.query.filter_by(author_id=id).all()

def get_author(id):
    return Author.query.get(id)

def get_name_author(id):
    return Author.query.get(id).name

def get_last_id():
    return Author.query.order_by(Author.id.desc()).first().id

def nb_livres_author(author_id):
    return Book.query.filter_by(author_id=author_id).count()

def get_author_of_book(id):
    return Book.query.get(id).author_id

# ## INFO BOOK
# def get_price_book(id):
#     return Book.query.get(id).price

# def get_title_book(id):
#     return Book.query.get(id).title

# def get_url_book(id):
#     return Book.query.get(id).url

# def get_img_book(id):
#     return Book.query.get(id).img

# def get_author_book(id):
#     return Book.query.get(id).author_id


## USER 
@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

def get_user(username):
    return User.query.get(username)
