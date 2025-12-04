from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime

messages_bp = Blueprint('messages', __name__, template_folder='../templates')

# Имитация базы сообщений
messages_data = []


@messages_bp.route('/messages')
def messages_list():
    return render_template('messages.html', messages=messages_data)


@messages_bp.route('/messages/send', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        name = session.get('user', 'Гость')
        text = request.form.get('text')

        if text.strip():
            messages_data.append({
                "name": name,
                "text": text,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        return redirect(url_for('messages.messages_list'))

    return render_template('message_send.html')
