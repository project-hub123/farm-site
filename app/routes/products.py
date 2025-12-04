from flask import Blueprint, render_template

products_bp = Blueprint('products', __name__, template_folder='../templates')


@products_bp.route('/products')
def products_list():
    return render_template('products.html')
