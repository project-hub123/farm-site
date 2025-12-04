from flask import Blueprint, render_template, redirect, url_for, request, session
from werkzeug.security import check_password_hash, generate_password_hash

users_bp = Blueprint('users', __name__, template_folder='../templates')

# Простейшая имитация БД пользователей (можешь заменить на базу)
users_db = {
    "admin": {
        "password": generate_password_hash("admin123"),
        "role": "admin"
    },
    "user": {
        "password": generate_password_hash("user123"),
        "role": "user"
    }
}


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('login')
        password_input = request.form.get('password')

        user = users_db.get(login_input)

        if user and check_password_hash(user["password"], password_input):
            session['user'] = login_input
            session['role'] = user["role"]
            return redirect(url_for('main.index'))

        return render_template('login.html', error="Неверный логин или пароль")

    return render_template('login.html')


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login_input = request.form.get('login')
        password_input = request.form.get('password')

        if login_input in users_db:
            return render_template('register.html', error="Пользователь уже существует")

        users_db[login_input] = {
            "password": generate_password_hash(password_input),
            "role": "user"
        }

        return redirect(url_for('users.login'))

    return render_template('register.html')


@users_bp.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('users.login'))

    return render_template('profile.html', user=session.get('user'), role=session.get('role'))


@users_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
