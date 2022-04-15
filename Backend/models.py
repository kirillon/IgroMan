from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(300), nullable=False)
    genre = db.Column("genre", db.String(300), nullable=False)
    steam_id = db.Column("steam_id", db.Integer, nullable=False)
    url = db.Column("url", db.String(150), nullable=False)
    price = db.Column("price", db.String(150), nullable=False)
