from flask import Blueprint, render_template, session, redirect, url_for, request
from app.database.models import User, db

users_bp = Blueprint("users", __name__, template_folder="../templates")


# -----------------------------------
#    ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
# -----------------------------------
@users_bp.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    return render_template("profile.html", user=user)


# -----------------------------------
#   СПИСОК ПОЛЬЗОВАТЕЛЕЙ  (АДМИН)
# -----------------------------------
@users_bp.route("/admin/users")
def admin_users():
    if session.get("role") != "admin":
        return redirect(url_for("main.index"))

    users = User.query.all()
    return render_template("admin_users.html", users=users)


# -----------------------------------
#   СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ (АДМИН)
# -----------------------------------
@users_bp.route("/admin/create", methods=["GET", "POST"])
def create_user():
    if session.get("role") != "admin":
        return redirect(url_for("main.index"))

    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        role = request.form.get("role")

        if User.query.filter_by(login=login).first():
            return render_template("admin_create.html", error="Такой пользователь уже существует!")

        new_user = User(login=login, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("users.admin_users"))

    return render_template("admin_create.html")


# -----------------------------------
#   ПРОСМОТР ОТДЕЛЬНОГО ЮЗЕРА (АДМИН)
# -----------------------------------
@users_bp.route("/admin/user/<int:user_id>")
def admin_view_user(user_id):
    if session.get("role") != "admin":
        return redirect(url_for("main.index"))

    user = User.query.get(user_id)
    if not user:
        return redirect(url_for("users.admin_users"))

    return render_template("admin_user_item.html", user=user)
