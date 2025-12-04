from flask import Blueprint, render_template, redirect, url_for, request, session, abort
from app.database.models import db, User

users_bp = Blueprint("users", __name__, template_folder="../templates")

# ------------------------------
# ПРОВЕРКА, ЧТО ПОЛЬЗОВАТЕЛЬ — АДМИН
# ------------------------------
def admin_required():
    if "role" not in session or session["role"] != "admin":
        abort(403)

# ------------------------------
# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
# ------------------------------
@users_bp.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(login=session["user"]).first()
    return render_template("profile.html", user=user)

# ------------------------------
# АДМИН-ПАНЕЛЬ: СПИСОК ПОЛЬЗОВАТЕЛЕЙ
# ------------------------------
@users_bp.route("/admin")
def admin_home():
    admin_required()
    users = User.query.all()
    return render_template("admin_home.html", users=users)

# ------------------------------
# СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ
# ------------------------------
@users_bp.route("/admin/create", methods=["GET", "POST"])
def admin_create():
    admin_required()

    if request.method == "POST":
        login_input = request.form.get("login")
        password_input = request.form.get("password")
        role_input = request.form.get("role", "user")

        if User.query.filter_by(login=login_input).first():
            return render_template("admin_create.html", error="Пользователь уже существует")

        new_user = User(login=login_input, role=role_input)
        new_user.set_password(password_input)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("users.admin_home"))

    return render_template("admin_create.html")

# ------------------------------
# УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
# ------------------------------
@users_bp.route("/admin/delete/<int:user_id>")
def admin_delete(user_id):
    admin_required()
    user = User.query.get_or_404(user_id)

    if user.role == "admin":
        return "Нельзя удалить администратора."

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("users.admin_home"))
