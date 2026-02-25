from enum import Enum
from typing import List

from app.domain.enums.files.files_enum_utils import (
    normalize_header
)


class FuncionariosActivos(Enum):
    SEDE = 1
    NOMBRES_Y_APELLIDOS = 2
    EMAIL = 3
    NOMBRE_CARGO = 4
    UNIDAD = 5
    NOMBRE_VINCULACION = 6
    FACULTAD_NOMBRE_ZONA = 7

    @classmethod
    def validate_headers(cls, headers: List[str]) -> bool:
        """
        Verifica si todos los encabezados en `headers` están en el Enum.
        No requiere que estén en orden, pero sí que estén todos presentes.
        """

        normalized_headers = {normalize_header(h) for h in headers if h}
        enum_headers = {e.name for e in cls}

        return enum_headers.issubset(normalized_headers)
