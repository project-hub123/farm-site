from flask import Blueprint, render_template, session, redirect, url_for
from app.database.models import User

users_bp = Blueprint("users", __name__, template_folder="../templates")

# --------------------------
# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
# --------------------------
@users_bp.route("/profile")
def profile():
    # Проверяем авторизацию
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # Загружаем пользователя из БД
    user = User.query.get(session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    return render_template("profile.html", user=user)


# --------------------------
# СПИСОК ПОЛЬЗОВАТЕЛЕЙ (ТОЛЬКО АДМИН)
# --------------------------
@users_bp.route("/admin/users")
def users_admin():
    if session.get("role") != "admin":
        return redirect(url_for("main.index"))

    all_users = User.query.all()
    return render_template("admin_users.html", users=all_users)


# --------------------------
# ПРОСМОТР ОТДЕЛЬНОГО ЮЗЕРА (ТОЛЬКО АДМИН)
# --------------------------
@users_bp.route("/admin/user/<int:user_id>")
def admin_view_user(user_id):
    if session.get("role") != "admin":
        return redirect(url_for("main.index"))

    user = User.query.get(user_id)
    return render_template("admin_user_item.html", user=user)
