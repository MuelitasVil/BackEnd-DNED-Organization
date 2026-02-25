from pydantic import BaseModel
from typing import Optional


class SchoolInput(BaseModel):
    cod_school: str
    email: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    general_code: Optional[str] = None
    type_user: Optional[str] = None
