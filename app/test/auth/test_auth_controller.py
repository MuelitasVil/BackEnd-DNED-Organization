from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.configuration.database import get_session
from app.controllers import auth_controller
from app.exceptions.auth_exceptions import (
    InvalidEmailException,
    EmailAlreadyRegisteredException
)


app = FastAPI()
app.include_router(auth_controller.router)
app.dependency_overrides[get_session] = lambda: object()

client = TestClient(app)


def test_register_returns_user_email(monkeypatch):
    def fake_register(email, password, session):
        class User:
            def __init__(self, user_email):
                self.email = user_email

        return User(email)

    monkeypatch.setattr(auth_controller.AuthService, "register", fake_register)

    response = client.post(
        "/auth/register",
        json={"email": "student@unal.edu.co", "password": "secret"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "User registered",
        "email": "student@unal.edu.co"
    }


def test_register_rejects_non_unal_email(monkeypatch):
    def fake_register(email, password, session):
        raise InvalidEmailException(
            "Email must be from @unal.edu.co domain"
        )

    monkeypatch.setattr(auth_controller.AuthService, "register", fake_register)

    response = client.post(
        "/auth/register",
        json={"email": "user@gmail.com", "password": "secret"}
    )

    assert response.status_code == 400
    assert "must be from @unal.edu.co" in response.json()["detail"]


def test_register_rejects_duplicate_email(monkeypatch):
    def fake_register(email, password, session):
        raise EmailAlreadyRegisteredException(email)

    monkeypatch.setattr(auth_controller.AuthService, "register", fake_register)

    response = client.post(
        "/auth/register",
        json={"email": "student@unal.edu.co", "password": "secret"}
    )

    assert response.status_code == 409
    assert "already registered" in response.json()["detail"]


def test_login_returns_access_token(monkeypatch):
    monkeypatch.setattr(
        auth_controller.AuthService,
        "login",
        lambda email, password, session: "jwt-token"
    )

    response = client.post(
        "/auth/login",
        json={"email": "active@example.com", "password": "secret"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "jwt-token",
        "token_type": "bearer"
    }


def test_login_returns_401_when_credentials_are_invalid(monkeypatch):
    monkeypatch.setattr(
        auth_controller.AuthService,
        "login",
        lambda email, password, session: None
    )

    response = client.post(
        "/auth/login",
        json={"email": "inactive@example.com", "password": "secret"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
