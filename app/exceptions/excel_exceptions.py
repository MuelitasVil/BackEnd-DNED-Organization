from app.exceptions.base_exceptions import AppError


class InvalidExcelStructureError(AppError):
    def __init__(self, sheet_name: str, headers: list[str]):
        super().__init__(
            message=f"La hoja {sheet_name} no tiene una estructura válida",
            code="INVALID_EXCEL_STRUCTURE",
            status_code=400,
            extra={
                "sheet_name": sheet_name,
                "headers": headers,
                "hint": (
                    "El programa siempre toma la primera hoja, "
                    "verifique si la primera hoja contiene la información"
                )
            }
        )
