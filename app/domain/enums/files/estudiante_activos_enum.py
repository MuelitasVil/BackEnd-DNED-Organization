from enum import Enum
from typing import List

from app.utils.string_utils import (
    normalize_header
)

from app.domain.enums.global_sedes_enum import (
    SPECIAL_SEDES
)


class EstActSedeEnum(Enum):
    SEDE_BOGOTA = (1, "SEDE BOGOTÁ")
    SEDE_MANIZALES = (2, "SEDE MANIZALES")
    SEDE_MEDELLÍN = (3, "SEDE MEDELLÍN")
    SEDE_PALMIRA = (4, "SEDE PALMIRA")
    SEDE_AMAZONIA = (5, "SEDE AMAZONÍA")
    SEDE_CARIBE = (6, "SEDE CARIBE")
    SEDE_ORINOQUÍA = (7, "SEDE ORINOQUÍA")
    SEDE_TUMACO = (8, "SEDE TUMACO")
    SEDE_DE_LA_PAZ = (9, "SEDE DE LA PAZ")

    def __init__(self, number, _name):
        self.number = number
        self._name = _name

    @classmethod
    def is_valid_sede(cls, sede_value: str) -> bool:
        """
        Valida si el valor de la sede proporcionado existe en el Enum
        EstActSedeEnum.
        :param sede_value: El valor de la sede (con tildes, mayúsculas, etc.).
        :return: True si la sede existe, False en caso contrario.
        """
        # Comparar directamente el string con los nombres de los miembros
        # del Enum
        name_members = [member._name for member in cls]
        if sede_value in name_members:
            return True
        return False

    @classmethod
    def is_special_sede(self, sede: str) -> bool:
        return sede in SPECIAL_SEDES

    @classmethod
    def get_by_name(self, name: str):
        """
        Obtiene un miembro del Enum a partir del nombre de la sede.
        :param name: El nombre de la sede (como cadena, e.g., "SEDE BOGOTÁ").
        :return: El miembro correspondiente del Enum.
        """
        sede_value = name.strip().upper()
        for member in self:
            if member._name == sede_value:
                return member
        return None


class EstudianteActivos(Enum):
    NOMBRES_APELLIDOS = 1
    EMAIL = 2
    SEDE = 3
    FACULTAD = 4
    COD_PLAN = 5
    PLAN = 6
    TIPO_NIVEL = 7

    @classmethod
    def validate_headers(self, headers: List[str]) -> bool:
        """
        Verifica si todos los encabezados en `headers` están en el Enum.
        No requiere que estén en orden, pero sí que estén todos presentes.
        """
        # Normalizamos las cadenas para evitar errores por
        # mayúsculas/minúsculas/espacios

        normalized_headers = {normalize_header(h) for h in headers if h}
        enum_headers = {e.name for e in self}
        return enum_headers.issubset(normalized_headers)
