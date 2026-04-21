from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserWorkspaceInput(BaseModel):
    email_unal: str = None
    last_connection: Optional[datetime] = None
    status: Optional[bool] = None
    email_usage: Optional[float] = None
    storage_used: Optional[float] = None
    storage_limit: Optional[float] = None
    is_person: Optional[bool] = None
    is_active_in_period: Optional[bool] = None
    cod_period: Optional[str] = None
