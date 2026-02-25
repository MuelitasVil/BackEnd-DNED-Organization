from enum import Enum


class OrgType(Enum):
    GLOBAL = "GLOBAL"
    HEADQUARTERS = "HEADQUARTERS"
    SCHOOL = "SCHOOL"
    UNIT = "UNIT"


class OrgLevel(Enum):
    PREGRADO = "PRE"
    POSGRADO = "POS"
    ANY = "ANY"


class Role(Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"
