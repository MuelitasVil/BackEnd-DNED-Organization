from fastapi import HTTPException
from typing import Dict, Any, List

MAX_ERRORS_IN_RESPONSE = 25


def add_blank_row_error(
        errors: List[Dict[str, Any]],
        row_idx: int,
) -> None:
    errors.append({
      "row": row_idx,
      "message": "Fila completamente vacía"
    })


def add_blank_cell_error(
        errors: List[Dict[str, Any]],
        row_idx: int,
        col_idx: int,
        col_name: str
) -> None:
    errors.append({
        "row": row_idx,
        "column": col_idx,
        "message": f"Celda vacía en columna '{col_name}'"
    })


def add_invalid_headquarters_error(
        errors: List[Dict[str, Any]],
        row_idx: int,
        col_idx: int,
        invalid_value: str
) -> None:
    errors.append({
        "row": row_idx,
        "column": col_idx,
        "message": f"Sede no válida: {invalid_value}"
    })


def raise_if_errors(errors: List[Dict[str, Any]]):
    """Lanza HTTPException si hay errores en la lista."""
    if not errors or len(errors) == 0:
        return

    raise HTTPException(status_code=400, detail={
        "status": False,
        "errors": errors[:MAX_ERRORS_IN_RESPONSE],
        "total_errors": len(errors)
    })
