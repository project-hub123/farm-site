from flask import Blueprint, render_template, request, redirect, url_for, session
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
        login_input = request.form.get("username")
        password_input = request.form.get("password")

        # 🔥 главная ошибка была ТУТ
        user = User.query.filter_by(login=login_input).first()

        if user and user.check_password(password_input):
            session["user"] = user.login
            session["role"] = user.role
            session["user_id"] = user.id
            return redirect(url_for("main.index"))

        return render_template("login.html", error="Неверный логин или пароль")

    return render_template("login.html")


# ------------------------------
# РЕГИСТРАЦИЯ
# ------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login_input = request.form.get("username")
        password_input = request.form.get("password")

        if User.query.filter_by(login=login_input).first():
            return render_template("register.html", error="Пользователь уже существует")

        new_user = User(login=login_input, role="user")
        new_user.set_password(password_input)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ------------------------------
# ВЫХОД
# ------------------------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))
