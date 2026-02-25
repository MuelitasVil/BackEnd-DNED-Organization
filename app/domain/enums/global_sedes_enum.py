from enum import Enum


# Sedes de presencial nacional.
SPECIAL_SEDES = {
    "SEDE AMAZONÍA",
    "SEDE CARIBE",
    "SEDE ORINOQUÍA",
    "SEDE TUMACO",
    "SEDE DE LA PAZ",
}


class GlobalSedeEnum(Enum):
    SEDE_BOGOTA = ("SEDE BOGOTÁ")
    SEDE_MANIZALES = ("SEDE MANIZALES")
    SEDE_MEDELLÍN = ("SEDE MEDELLÍN")
    SEDE_PALMIRA = ("SEDE PALMIRA")
    SEDE_AMAZONIA = ("SEDE AMAZONÍA")
    SEDE_CARIBE = ("SEDE CARIBE")
    SEDE_ORINOQUÍA = ("SEDE ORINOQUÍA")
    SEDE_TUMACO = ("SEDE TUMACO")
    SEDE_DE_LA_PAZ = ("SEDE DE LA PAZ")
    NACIONAL = ("NIVEL NACIONAL", "NIVEL NACIONAL")

    def __init__(self, _name):
        self._name = _name

    @classmethod
    def is_valid_sede(cls, sede_value: str) -> bool:
        """
        Valida si el valor de la sede proporcionado existe en el Enum
        GlobalSedeEnum.
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
