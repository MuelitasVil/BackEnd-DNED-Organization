from openpyxl.cell.cell import Cell
from typing import Any, Dict, List, Tuple, Type
import unicodedata

from enum import Enum

from app.service.excel_processor.utils.error_utils import (
    add_blank_cell_error,
    add_blank_row_error
)


def is_blank(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def get_file_text(v: Any) -> str:
    if v is None:
        return ""
    text = str(v).strip()
    text = text.replace('(', '').replace(')', '')
    return text


def get_value_from_row(row: Tuple[Cell, ...], col_idx: int) -> str:
    # La columna es 1-indexada
    return get_file_text(row[col_idx - 1].value)


def normalize_string(s: str) -> str:
    """Normaliza una cadena eliminando tildes y convirtiéndola a minúsculas."""
    if s is None:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', s)
    return (
        ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
        .lower()
    )


def is_header_row(row: int) -> bool:
    return row == 1


def validate_row_blank_or_incomplete(
    row: Tuple[Cell, ...],
    row_idx: int,
    file_enum: Type[Enum],
) -> List[Dict[str, Any]]:
    """
    Devuelve una lista de errores:
    - Si la fila está completamente vacía: un solo error de fila vacía.
    - Si la fila está incompleta: errores por celda vacía.
    - Si está OK: lista vacía.
    """
    if file_enum is None:
        raise ValueError("El parámetro 'file_enum' no puede ser None")

    missing: List[Dict[str, Any]] = []
    enum_cols = list(file_enum)

    for col in enum_cols:
        col_idx = col.value
        col_name = col.name

        # Evita IndexError si la fila viene más corta que el enum
        value = row[col_idx - 1].value if (col_idx - 1) < len(row) else None
        if is_blank(value):
            add_blank_cell_error(missing, row_idx, col_idx, col_name)

    if len(missing) == len(enum_cols):
        # solo error de fila vacía (sin spam de celdas)
        missing = []
        add_blank_row_error(missing, row_idx)

    return missing
