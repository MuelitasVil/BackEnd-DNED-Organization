from sqlmodel import SQLModel, Field
from typing import Optional


class EmailSender(SQLModel, table=True):
    __tablename__ = "email_sender"

    id: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True, max_length=254)
    name: Optional[str] = Field(default=None, max_length=150)
    org_type: str = Field(default='GLOBAL', max_length=50)
    org_code: Optional[str] = Field(default=None, max_length=100)
    sede_code: Optional[str] = Field(default=None, max_length=100)
    # todo: change level to type of user.
    level: str = Field(default='ANY', max_length=3)
    role: str = Field(default='OWNER', max_length=10)
    is_active: bool = Field(default=True)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
