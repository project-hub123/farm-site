from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.database.models import db, User

auth_bp = Blueprint("auth", __name__, template_folder="../templates")

# ------------------------------
# АВТО-СОЗДАНИЕ АДМИНА
# ------------------------------
def create_admin():
    admin = User.query.filter_by(role="admin").first()
    if not admin:
        admin = User(login="admin", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()


# ------------------------------
# ВХОД
# ------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")   # из формы
        password = request.form.get("password")

        user = User.query.filter_by(login=username).first()

        if user and user.check_password(password):
            login_user(user)     # <-- правильный вход
            return redirect(url_for("main.index"))

        return render_template("login.html", error="Неверный логин или пароль")

    return render_template("login.html")


# ------------------------------
# РЕГИСТРАЦИЯ
# ------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if User.query.filter_by(login=username).first():
            return render_template("register.html", error="Пользователь уже существует")

        new_user = User(login=username, role="user")
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ------------------------------
# ВЫХОД
# ------------------------------
@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
