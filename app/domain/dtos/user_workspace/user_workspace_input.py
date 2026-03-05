from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserWorkspaceInput(BaseModel):
    email_unal: str = None
    last_connection: Optional[datetime] = None
    status: Optional[str] = None
    email_usage: Optional[float] = None
    storage_used: Optional[float] = None
    storage_limit: Optional[float] = None
    isUser: Optional[bool] = None
