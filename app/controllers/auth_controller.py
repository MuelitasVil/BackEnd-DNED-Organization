from app.domain.dtos.auth.register_input import RegisterInput
from app.domain.dtos.auth.login_input import LoginInput
from app.service.use_cases.auth import AuthService
from app.exceptions.auth_exceptions import (
    InvalidEmailException,
    EmailAlreadyRegisteredException
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configuration.database import get_session

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(data: RegisterInput, session: Session = Depends(get_session)):
    try:
        user = AuthService.register(data.email, data.password, session)
        return {"message": "User registered", "email": user.email}
    except InvalidEmailException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except EmailAlreadyRegisteredException as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.post("/login")
def login(data: LoginInput, session: Session = Depends(get_session)):
    token = AuthService.login(data.email, data.password, session)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
