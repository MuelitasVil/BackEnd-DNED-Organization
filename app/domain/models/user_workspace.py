from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class UserWorkspace(SQLModel, table=True):
    __tablename__ = "user_workspace"

    user_workspace_id: str = Field(default=None, primary_key=True)
    email_unal: str = Field(default=None, max_length=50)
    last_connection: Optional[datetime] = None
    status: bool = True
    email_usage: Optional[float] = None
    storage_used: Optional[float] = None
    storage_limit: Optional[float] = None
    is_person: bool = False
    cod_period: Optional[str] = None
