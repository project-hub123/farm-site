from flask import Blueprint, render_template

articles_bp = Blueprint('articles', __name__, template_folder='../templates')


@articles_bp.route('/articles')
def articles_list():
    return render_template('articles.html')


@articles_bp.route('/articles/<int:article_id>')
def article_item(article_id):
    return render_template('article_item.html', article_id=article_id)
