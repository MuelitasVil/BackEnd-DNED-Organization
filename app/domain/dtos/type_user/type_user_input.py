from pydantic import BaseModel
from typing import Optional


class TypeUserInput(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
