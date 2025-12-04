from flask import Blueprint, render_template

news_bp = Blueprint('news', __name__, template_folder='../templates')

# Имитация базы данных новостей
news_data = [
    {
        "id": 1,
        "title": "На ферме родился телёнок",
        "text": "Сегодня на ферме появилось новое пополнение. Животное чувствует себя хорошо.",
        "date": "2025-01-15"
    },
    {
        "id": 2,
        "title": "Начался сезон свежего молока",
        "text": "Запасы свежего молока увеличены, доступно больше натуральных продуктов.",
        "date": "2025-02-01"
    },
    {
        "id": 3,
        "title": "Улучшение условий содержания животных",
        "text": "На ферме обновлены помещения и расширены пастбища.",
        "date": "2025-02-10"
    }
]


@news_bp.route('/news')
def news_list():
    return render_template('news.html', news=news_data)


@news_bp.route('/news/<int:news_id>')
def news_item(news_id):
    item = next((n for n in news_data if n["id"] == news_id), None)
    return render_template('news_item.html', item=item)
