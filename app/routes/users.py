from flask import Blueprint, render_template, session, redirect, url_for
from app.database.models import User

users_bp = Blueprint("users", __name__, template_folder="../templates")


# -----------------------------------
#    ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
# -----------------------------------
@users_bp.route("/profile")
def profile():
    # Проверка авторизации
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    # Достаём пользователя из БД
    user = User.query.get(user_id)
    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    return render_template("profile.html", user=user)


# -----------------------------------
#     СПИСОК ПОЛЬЗОВАТЕЛЕЙ (АДМИН)
# -----------------------------------
@users_bp.route("/admin/users")
def users_admin():
    # Проверяем роль
    if session.get("role") != "admin":
        return redirect(url_for("main.index"))

    all_users = User.query.all()

    return render_template("admin_users.html", users=all_users)


# -----------------------------------
#     ПРОСМОТР ОДНОГО ЮЗЕРА (АДМИН)
# -----------------------------------
@users_bp.route("/admin/user/<int:user_id>")
def admin_view_user(user_id):
    if session.get("role") != "admin":
        return redirect(url_for("main.index"))

    user = User.query.get(user_id)

    if not user:
        return redirect(url_for("users.users_admin"))

    return render_template("admin_user_item.html", user=user)

# -----------------------------------
#     СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ (АДМИН)
# -----------------------------------
@users_bp.route("/admin/create", methods=["GET", "POST"])
def create_user():
    # Доступ только админу
    if session.get("role") != "admin":
        return redirect(url_for("main.index"))

    if request.method == "POST":
        login_input = request.form.get("login")
        password_input = request.form.get("password")
        role_input = request.form.get("role", "user")

        # Проверка дублирования
        if User.query.filter_by(login=login_input).first():
            return render_template("admin_create.html",
                                   error="Пользователь с таким логином уже существует")

        # Создание пользователя
        new_user = User(login=login_input, role=role_input)
        new_user.set_password(password_input)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("users.users_admin"))

    return render_template("admin_create.html")

