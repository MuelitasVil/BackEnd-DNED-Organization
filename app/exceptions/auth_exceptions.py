from app.exceptions.base_exceptions import AppError


class InvalidEmailException(AppError):
    """Excepción para email inválido o no verificable."""

    def __init__(self, message: str = "Invalid email"):
        super().__init__(
            message=message,
            code="INVALID_EMAIL",
            status_code=400
        )


class EmailAlreadyRegisteredException(AppError):
    """Excepción para email ya registrado."""

    def __init__(self, email: str):
        super().__init__(
            message=f"Email {email} is already registered",
            code="EMAIL_ALREADY_REGISTERED",
            status_code=409
        )
