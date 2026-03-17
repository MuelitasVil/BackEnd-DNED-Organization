class AppError(Exception):
    """Excepción base de la aplicación."""

    def __init__(
        self,
        message: str,
        code: str = "APP_ERROR",
        status_code: int = 400,
        extra: dict | None = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.extra = extra or {}
        super().__init__(message)
