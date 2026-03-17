from app.exceptions.base_exceptions import AppError


class PeriodNotFoundError(AppError):
    def __init__(self, cod_period: str):
        super().__init__(
            message=f"El periodo con código {cod_period} no existe",
            code="PERIOD_NOT_FOUND",
            status_code=404,
            extra={"cod_period": cod_period}
        )
