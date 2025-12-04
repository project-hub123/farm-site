from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__, template_folder='../templates')


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/contacts')
def contacts():
    return render_template('contacts.html')


@main_bp.route('/sitemap')
def sitemap():
    return render_template('sitemap.html')
