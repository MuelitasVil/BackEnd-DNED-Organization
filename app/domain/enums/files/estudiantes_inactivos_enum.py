from enum import Enum
from typing import List

from app.utils.string_utils import (
    normalize_header
)


class EstInactSedeEnum(Enum):
    SEDE_BOGOTA = ("SEDE BOGOTÁ")
    SEDE_MANIZALES = ("SEDE MANIZALES")
    SEDE_MEDELLÍN = ("SEDE MEDELLÍN")
    SEDE_PALMIRA = ("SEDE PALMIRA")
    SEDE_AMAZONIA = ("SEDE AMAZONÍA")
    SEDE_CARIBE = ("SEDE CARIBE")
    SEDE_ORINOQUÍA = ("SEDE ORINOQUÍA")
    SEDE_TUMACO = ("SEDE TUMACO")
    SEDE_DE_LA_PAZ = ("SEDE DE LA PAZ")

    def __init__(self, _name):
        self._name = _name

    @classmethod
    def is_valid_sede(cls, sede_value: str) -> bool:
        """
        Valida si el valor de la sede proporcionado existe en el Enum
        EstInactSedeEnum.
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


class EstudianteInactivos(Enum):
    DOCUMENTO = 1
    NOMBRES = 2
    APELLIDO1 = 3
    APELLIDO2 = 4
    EMAIL = 5
    BLOQUEO = 6
    SEDE = 7
    TIPO_NIVEL = 8

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
