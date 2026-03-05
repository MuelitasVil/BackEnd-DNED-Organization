from enum import Enum
from typing import List

from app.utils.string_utils import (
    normalize_header
)


NEVER_LOG_IN = "Never logged in"
ACTIVE = "Active"
SUSPENDED = "Suspended"


class WorkSpace(Enum):
    FIRST_NAME = "First Name [Required]"
    LAST_NAME = "Last Name [Required]V"
    EMAIL = "Email Address [Required]"
    STATUS = "Status [READ ONLY]"
    LAST_SING_IN = "Last Sign In [READ ONLY]"
    EMAIL_USAGE = "Email Usage [READ ONLY]"
    STORAGE_USED = "Storage Used [READ ONLY]"
    STORAGE_LIMIT = "Storage limit [READ ONLY]"

    @classmethod
    def validate_headers(self, headers: List[str]) -> bool:
        """
        Verifica si todos los encabezados en `headers` están en el Enum.
        No requiere que estén en orden, pero sí que estén todos presentes.
        """

        normalized_headers = {normalize_header(h) for h in headers if h}
        enum_headers = {e.name for e in self}

        return enum_headers.issubset(normalized_headers)

    def is_never_logged_in(self) -> bool:
        return self.STATUS.value == NEVER_LOG_IN

    def is_active(self) -> bool:
        return self.STATUS.value == ACTIVE

    def is_suspended(self) -> bool:
        return self.STATUS.value == SUSPENDED
