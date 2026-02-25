from sqlmodel import SQLModel, Field
from typing import Optional


class Headquarters(SQLModel, table=True):
    __tablename__ = "headquarters"

    cod_headquarters: str = Field(primary_key=True, max_length=50)
    email: Optional[str] = Field(default=None, max_length=100)
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None
    general_code: Optional[str] = Field(default=None, max_length=50)
    type_user: Optional[str] = Field(default=None, max_length=100)
