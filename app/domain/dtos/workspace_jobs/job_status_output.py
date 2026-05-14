from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class JobResponse(BaseModel):
    id: str
    process_type: str
    status: str
    params: Dict[str, Any]
    requested_by: Optional[str] = None
    origin: Optional[str] = None
    priority: int
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None


class JobProgressResponse(BaseModel):
    phase: str
    total_units: int
    processed_units: int
    total_emails: int
    processed_emails: int
    last_error: Optional[str] = None


class JobResultResponse(BaseModel):
    success_count: int
    error_count: int
    error_samples: Optional[Dict[str, Any]] = None
    artifacts: Optional[Dict[str, Any]] = None


class WorkspaceJobStatusOutput(BaseModel):
    job: JobResponse
    progress: Optional[JobProgressResponse] = None
    result: Optional[JobResultResponse] = None
