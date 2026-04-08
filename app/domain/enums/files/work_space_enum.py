from enum import Enum
from typing import List

from app.utils.string_utils import (
    normalize_header
)


NEVER_LOG_IN = "Never logged in"
ACTIVE = "Active"
SUSPENDED = "Suspended"


class WorkSpace(Enum):
    FIRST_NAME = 1
    LAST_NAME = 2
    EMAIL = 3
    STATUS = 4
    LAST_SING_IN = 5
    EMAIL_USAGE = 6
    STORAGE_USED = 7
    STORAGE_LIMIT = 8

    @classmethod
    def validate_headers(self, headers: List[str]) -> bool:
        """
        Verifica si todos los encabezados en `headers` están en el Enum.
        No requiere que estén en orden, pero sí que estén todos presentes.
        """

        normalized_headers = {normalize_header(h) for h in headers if h}
        enum_headers = {normalize_header(e.name) for e in self}

        print(f"Normalized Headers: {normalized_headers}")
        print(f"Enum Headers: {enum_headers}")

        return enum_headers.issubset(normalized_headers)

    def is_never_logged_in(value) -> bool:
        return value == NEVER_LOG_IN

    def is_active(value) -> bool:
        return value == ACTIVE

    def is_suspended(value) -> bool:
        return value == SUSPENDED

    def get_status_value(value) -> bool:
        if WorkSpace.is_active(value):
            return True
        else:
            return False

