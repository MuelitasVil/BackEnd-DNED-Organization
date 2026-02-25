from sqlmodel import SQLModel, Field
from typing import Optional


class TypeUser(SQLModel, table=True):
    __tablename__ = "type_user"

    name: Optional[str] = Field(primary_key=True, max_length=100)
    description: Optional[str] = None
