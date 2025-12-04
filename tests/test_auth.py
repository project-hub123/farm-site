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


def test_register(client):
    response = client.post("/register", data={
        "login": "testuser",
        "password": "12345"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Вход" in response.data


def test_login(client):
    # создаём пользователя
    client.post("/register", data={
        "login": "testuser",
        "password": "12345"
    })

    response = client.post("/login", data={
        "login": "testuser",
        "password": "12345"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Главная" in response.data


def test_profile_access(client):
    # сначала регистрируем и логиним
    client.post("/register", data={
        "login": "testuser",
        "password": "12345"
    })
    client.post("/login", data={
        "login": "testuser",
        "password": "12345"
    })

    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Профиль" in response.data


def test_logout(client):
    # регистрация + вход
    client.post("/register", data={
        "login": "testuser",
        "password": "12345"
    })
    client.post("/login", data={
        "login": "testuser",
        "password": "12345"
    })

    response = client.get("/logout", follow_redirects=True)

    assert response.status_code == 200
    assert b"Главная" in response.data
