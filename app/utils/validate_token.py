# app/utils/auth.py
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import jwt

from app.configuration.settings import settings
from app.configuration.database import get_session
from app.repository.auth_repository import AuthRepository

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

token_scheme = HTTPBearer()


def get_current_user(
    token_data: str = Depends(token_scheme),
    session: Session = Depends(get_session)
) -> str:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido"
    )

    token = token_data.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise credentials_exception

    repo = AuthRepository(session)
    if not repo.token_exists(token):
        raise credentials_exception

    return payload.get("sub")
