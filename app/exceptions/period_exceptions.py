from app.exceptions.base_exceptions import AppError


class PeriodNotFoundError(AppError):
    def __init__(self, cod_period: str):
        super().__init__(
            message=f"El periodo con código {cod_period} no existe",
            code="PERIOD_NOT_FOUND",
            status_code=404,
            extra={"cod_period": cod_period}
        )


class InvalidPeriodDateError(AppError):
    def __init__(self, initial_date: str, final_date: str):
        super().__init__(
            message="La fecha inicial no puede ser mayor que la fecha final",
            code="INVALID_PERIOD_DATES",
            status_code=400,
            extra={"initial_date": initial_date, "final_date": final_date}
        )
