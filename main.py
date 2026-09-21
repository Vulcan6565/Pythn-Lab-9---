from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(300), nullable=False)

START_BOOKS = [
    ("Rifujin na Magonote", "Mushoku Tensei: Jobless Reincarnation — Volumes 1–15 of 26"),
    ("Tappei Nagatsuki", "Re:Zero − Starting Life in Another World"),
    ("Guiltythree", "Shadow Slave"),
    ("singNsong", "Omniscient Reader's Viewpoint"),
    ("Cuttlefish That Loves Diving", "Lord of Mysteries"),
    ("Q10", "Star-Embracing Swordmaster"),
    ("SOULPUNG", "Eternally Regressing Knight"),
    ("Pierce Brown", "Red Rising"),
    ("Dan Abnett", "Horus Rising — The Horus Heresy"),
    ("Graham McNeill", "False Gods — The Horus Heresy"),
    ("Ben Counter", "Galaxy in Flames — The Horus Heresy"),
]

def seed_books():
    if Book.query.count() == 0:
        for author, name in START_BOOKS:
            db.session.add(Book(author=author, name=name))
        db.session.commit()

@app.route("/")
def index():
    books = Book.query.order_by(Book.id).all()
    return render_template("index.html", books=books)

@app.route("/add", methods=["POST"])
def add_book():
    author = request.form.get("author", "").strip()
    name = request.form.get("name", "").strip()
    if author and name:
        db.session.add(Book(author=author, name=name))
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/clear", methods=["POST"])
def clear_books():
    db.session.query(Book).delete()
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/restore", methods=["POST"])
def restore_books():
    db.session.query(Book).delete()
    for author, name in START_BOOKS:
        db.session.add(Book(author=author, name=name))
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_books()
    app.run(debug=True)
