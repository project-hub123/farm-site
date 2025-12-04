from flask import Flask
from flask_login import LoginManager
from app.database.models import db
from config import DevelopmentConfig

# Blueprints
from app.routes.main import main_bp
from app.routes.animals import animals_bp
from app.routes.products import products_bp
from app.routes.articles import articles_bp
from app.routes.users import users_bp
from app.routes.errors import errors_bp
from app.routes.news import news_bp               
from app.components.auth import auth_bp
from app.components.search_engine import search_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from app.database.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register routes
    app.register_blueprint(main_bp)
    app.register_blueprint(animals_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(articles_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(news_bp)              
    app.register_blueprint(auth_bp)
    app.register_blueprint(search_bp)

    return app
