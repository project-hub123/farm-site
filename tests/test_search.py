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


def test_search_page_load(client):
    """Страница поиска загружается."""
    response = client.get("/search")
    assert response.status_code == 200
    assert b"Поиск" in response.data or b"query" in response.data


def test_search_query_existing(client):
    """Поиск по существующему слову должен выдавать результаты."""
    response = client.post("/search", data={"query": "молоко"})
    assert response.status_code == 200
    assert b"молоко".lower() in response.data.lower()


def test_search_query_no_results(client):
    """Поиск по слову, которого нет."""
    response = client.post("/search", data={"query": "неттакоготекста"})
    assert response.status_code == 200
    assert b"Ничего не найдено" in response.data or b"0" in response.data


def test_search_minimum_length(client):
    """Короткий запрос должен корректно обработаться."""
    response = client.post("/search", data={"query": "a"})
    assert response.status_code == 200
