from .app import db, login_manager
from flask_login import UserMixin

class Author(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return "Author (%d, %s)" % (self.id, self.name)



class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    img = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('books', 
    lazy='dynamic'))

    def __repr__(self):
        return "Book (%d, %s)" % (self.id, self.title)

class User(db.Model, UserMixin):
    username = db.Column(db.String(100),primary_key=True)
    password = db.Column(db.String(100))
    bibliotheque_id = db.Column(db.Integer, db.ForeignKey('bibliotheque.id'))

    def __repr__(self):
        return "User (%s, %s)" % (self.username, self.password)

    def get_id(self):
        return self.username

    def get_password(self):
        return self.password

def get_sample():
    return Book.query.all()


class Bibliotheque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer, db.ForeignKey('user.username'))

    def __repr__(self):
        return "Bibliotheque (%d)" % (self.id)

class AjouterLivre(db.Model):
    id_livre = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    id_bibliotheque = db.Column(db.Integer, db.ForeignKey('bibliotheque.id'), primary_key=True)

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


def get_id_max_biblio():
    if Bibliotheque.query.all() == []:
        raise Exception("Pas de bibliothèques dans la base de donnée.")
    return Bibliotheque.query.order_by(Bibliotheque.id.desc()).first().id

def nb_livres_author(author_id):
    return Book.query.filter_by(author_id=author_id).count()

def get_author_of_book(id):
    return Book.query.get(id).author_id

def get_livre_bibliotheque(username):
    return AjouterLivre.query.filter_by(id_bibliotheque=Bibliotheque.query.filter_by(username=username).id)



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