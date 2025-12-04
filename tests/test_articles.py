import pytest
from app import create_app
from models import db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

    client = app.test_client()
    yield client


def test_articles_page(client):
    """Страница со списком статей должна открываться."""
    response = client.get("/articles")
    assert response.status_code == 200
    assert b"Статьи" in response.data


def test_article_items(client):
    """Каждая статья по ID должна открываться корректно."""

    for article_id in range(1, 6):
        response = client.get(f"/articles/{article_id}")
        assert response.status_code == 200
        assert b"Статья" in response.data


def test_article_not_found(client):
    """Несуществующая статья должна показывать заглушку."""
    response = client.get("/articles/999")
    assert response.status_code == 200
    assert b"не найдена" in response.data
