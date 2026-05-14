from datetime import datetime, timezone

import jwt
import pytest

from app.domain.models.system_user import SystemUser
from app.service.crud import auth_service
from app.exceptions.auth_exceptions import (
    InvalidEmailException,
    EmailAlreadyRegisteredException
)


class FakeAuthRepository:
    def __init__(self, user=None):
        self.user = user
        self.created_user = None
        self.created_token = None

    def create_user(self, user):
        self.created_user = user
        return user

    def get_user_by_email(self, email):
        if self.user and self.user.email == email:
            return self.user
        return None

    def create_token(self, token):
        self.created_token = token


def test_register_rejects_non_unal_email(monkeypatch):
    repo = FakeAuthRepository()
    monkeypatch.setattr(auth_service, "AuthRepository", lambda session: repo)

    with pytest.raises(InvalidEmailException):
        auth_service.AuthService.register(
            "user@gmail.com",
            "super-secret",
            session=object()
        )


def test_register_rejects_duplicate_email(monkeypatch):
    existing_user = SystemUser(
        email="student@unal.edu.co",
        hashed_password="hash",
        salt="salt",
        state=False
    )
    repo = FakeAuthRepository(user=existing_user)
    monkeypatch.setattr(auth_service, "AuthRepository", lambda session: repo)

    with pytest.raises(EmailAlreadyRegisteredException):
        auth_service.AuthService.register(
            "student@unal.edu.co",
            "super-secret",
            session=object()
        )


def test_register_hashes_password_and_creates_user(monkeypatch):
    repo = FakeAuthRepository()
    monkeypatch.setattr(auth_service, "AuthRepository", lambda session: repo)

    user = auth_service.AuthService.register(
        "student@unal.edu.co",
        "super-secret",
        session=object()
    )

    assert user.email == "student@unal.edu.co"
    assert user.state is False
    assert user.salt
    assert user.hashed_password != "super-secret"
    assert auth_service.pwd_context.verify(
        "super-secret" + user.salt,
        user.hashed_password
    )
    assert repo.created_user is user


def test_login_returns_none_when_user_does_not_exist(monkeypatch):
    repo = FakeAuthRepository(user=None)
    monkeypatch.setattr(auth_service, "AuthRepository", lambda session: repo)

    token = auth_service.AuthService.login(
        "missing@example.com",
        "password",
        session=object()
    )

    assert token is None
    assert repo.created_token is None


def test_login_returns_none_when_user_is_inactive(monkeypatch):
    user = SystemUser(
        email="inactive@example.com",
        hashed_password="hash",
        salt="salt",
        state=False
    )
    repo = FakeAuthRepository(user=user)
    monkeypatch.setattr(auth_service, "AuthRepository", lambda session: repo)

    token = auth_service.AuthService.login(
        "inactive@example.com",
        "password",
        session=object()
    )

    assert token is None
    assert repo.created_token is None


def test_login_returns_none_with_wrong_password(monkeypatch):
    salt = "abc123"
    hashed_password = auth_service.pwd_context.hash("correct-password" + salt)
    user = SystemUser(
        email="active@example.com",
        hashed_password=hashed_password,
        salt=salt,
        state=True
    )
    repo = FakeAuthRepository(user=user)
    monkeypatch.setattr(auth_service, "AuthRepository", lambda session: repo)

    token = auth_service.AuthService.login(
        "active@example.com",
        "wrong-password",
        session=object()
    )

    assert token is None
    assert repo.created_token is None


def test_login_returns_jwt_and_persists_token(monkeypatch):
    salt = "xyz789"
    hashed_password = auth_service.pwd_context.hash("correct-password" + salt)
    user = SystemUser(
        email="active@example.com",
        hashed_password=hashed_password,
        salt=salt,
        state=True
    )
    repo = FakeAuthRepository(user=user)
    monkeypatch.setattr(auth_service, "AuthRepository", lambda session: repo)

    token = auth_service.AuthService.login(
        "active@example.com",
        "correct-password",
        session=object()
    )

    assert token is not None
    payload = jwt.decode(
        token,
        auth_service.SECRET_KEY,
        algorithms=[auth_service.ALGORITHM]
    )
    assert payload["sub"] == "active@example.com"
    assert payload["exp"] >= int(datetime.now(timezone.utc).timestamp())

    assert repo.created_token is not None
    assert repo.created_token.email == "active@example.com"
