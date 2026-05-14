from typing import Any, Dict, Optional

from pydantic import BaseModel


class WorkspaceJobCreateInput(BaseModel):
    process_type: str
    params: Dict[str, Any]
    requested_by: Optional[str] = None
