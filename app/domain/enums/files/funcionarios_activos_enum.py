from enum import Enum
from typing import List

from app.utils.string_utils import (
    normalize_header
)


class FunSedeEnum(Enum):
    SEDE_BOGOTA = ("BOGOTÁ", "SEDE BOGOTÁ")
    SEDE_MANIZALES = ("MANIZALES", "SEDE MANIZALES")
    SEDE_MEDELLÍN = ("MEDELLÍN", "SEDE MEDELLÍN")
    SEDE_PALMIRA = ("PALMIRA", "SEDE PALMIRA")
    SEDE_AMAZONIA = ("AMAZONÍA", "SEDE AMAZONÍA")
    SEDE_CARIBE = ("CARIBE", "SEDE CARIBE")
    SEDE_ORINOQUÍA = ("ORINOQUÍA", "SEDE ORINOQUÍA")
    SEDE_TUMACO = ("TUMACO", "SEDE TUMACO")
    SEDE_DE_LA_PAZ = ("DE LA PAZ", "SEDE DE LA PAZ")
    NACIONAL = ("NIVEL NACIONAL", "NIVEL NACIONAL")

    def __init__(self, file_name, real_name):
        self.file_name = file_name
        self.real_name = real_name

    @classmethod
    def is_valid_sede(self, sede_value: str) -> bool:
        """
        Valida si el valor de la sede proporcionado existe en el Enum
        FunSedeEnum.
        :param sede_value: El valor de la sede (con tildes, mayúsculas, etc.).
        :return: True si la sede existe, False en caso contrario.
        """
        # Comparar directamente el string con los nombres de los miembros
        # del Enum
        name_members = [member._name for member in self]
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


class FuncionariosActivos(Enum):
    SEDE = 1
    NOMBRES_Y_APELLIDOS = 2
    EMAIL = 3
    NOMBRE_CARGO = 4
    UNIDAD = 5
    NOMBRE_VINCULACION = 6
    FACULTAD_NOMBRE_ZONA = 7

    @classmethod
    def validate_headers(self, headers: List[str]) -> bool:
        """
        Verifica si todos los encabezados en `headers` están en el Enum.
        No requiere que estén en orden, pero sí que estén todos presentes.
        """

        normalized_headers = {normalize_header(h) for h in headers if h}
        enum_headers = {e.name for e in self}

        return enum_headers.issubset(normalized_headers)
