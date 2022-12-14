import click
from .app import app,db
from .models import get_id_max_biblio

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    """Creates the tables and populates them with data"""

    # création de toutes les tables
    db.create_all()

    # chargement de notre jeu de données
    import yaml
    books = yaml.safe_load(open(filename))

    # import des modèles
    from .models import Author,Book

    # première passe : création de tous les auteurs
    authors = {}
    for b in books :
        a = b["author"]
        if a not in authors :
            o = Author(name=a)
            db.session.add(o)
            authors[a] = o
    db.session.commit()

    # deuxième passe : création de tous les livres
    for b in books :
        a = authors[b["author"]]
        o = Book(title=b["title"],price=b["price"],author=a,url=b["url"],img=b["img"])
        db.session.add(o)
    db.session.commit()

@app.cli.command()
def syncdb():
    """Creates all the missing tables"""
    db.create_all()

@app.cli.command()
@click.argument('username')
@click.argument('password')
def adduser(username,password):
    """Creates a new user"""
    from .models import User, Bibliotheque
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    id_biblio = 0
    try:
        id_biblio = get_id_max_biblio()+1
    except Exception:
        pass
    finally:
        b = Bibliotheque(id=id_biblio,username=username)

    u = User(username=username,password=m.hexdigest(), bibliotheque_id=id_biblio)
    db.session.add(u)
    db.session.add(b)
    db.session.commit()


@app.cli.command()
@click.argument('username')
@click.argument('password')
def updatepassword(username,password):
    """Updates the password of all users"""
    from .models import User
    from hashlib import sha256
    m = sha256()
    for u in User.query.all():
        if u.username == username:
            m.update(password.encode())
            u.password = m.hexdigest()
            db.session.commit()
            return

@app.cli.command()
@click.argument('username')
@click.argument('id_livre')
def ajouter_livre(username, id_livre):
    """Pour ajouter un livre dans la bibliothèque d'un utilisateur"""
    from .models import Bibliotheque, AjouterLivre
    id_biblio = Bibliotheque.query.filter_by(username=username).first().id
    ab = AjouterLivre(id_livre=int(id_livre), id_bibliotheque=id_biblio)
    db.session.add(ab)
    db.session.commit()
