from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

# Простая имитация БД (можно заменить на models.py)
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


@auth_bp.route('/login', methods=['GET', 'POST'])
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


@auth_bp.route('/register', methods=['GET', 'POST'])
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

        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
