from flask import Blueprint, render_template

animals_bp = Blueprint('animals', __name__, template_folder='../templates')


@animals_bp.route('/animals')
def animals_list():
    return render_template('animals.html')
