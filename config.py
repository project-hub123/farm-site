import os

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = "super-secret-key"

    # Папка /app
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "app"))

    # Путь к SQLite внутри /app/db.sqlite3
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
