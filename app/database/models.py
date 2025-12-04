from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# -----------------------------------
# МОДЕЛЬ ПОЛЬЗОВАТЕЛЯ
# -----------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")

    def __repr__(self):
        return f"<User {self.login}>"


# -----------------------------------
# МОДЕЛЬ СТАТЬИ
# -----------------------------------
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Article {self.title}>"


# -----------------------------------
# МОДЕЛЬ НОВОСТИ
# -----------------------------------
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), default=datetime.now().strftime("%Y-%m-%d"))

    def __repr__(self):
        return f"<News {self.title}>"


# -----------------------------------
# МОДЕЛЬ СООБЩЕНИЯ
# -----------------------------------
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="Гость")
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), default=datetime.now().strftime("%Y-%m-%d %H:%M"))

    def __repr__(self):
        return f"<Message {self.id}>"
