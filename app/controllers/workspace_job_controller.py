from fastapi import APIRouter, HTTPException

from app.clients.workspace_manager.job_client import WorkspaceJobClient
from app.domain.dtos.workspace_jobs.job_input import WorkspaceJobCreateInput
from app.domain.dtos.workspace_jobs.job_status_output import (
    WorkspaceJobStatusOutput,
    JobResponse,
)

router = APIRouter(prefix="/workspace-jobs", tags=["Workspace Jobs"])


@router.post("/", response_model=JobResponse)
async def create_workspace_job(payload: WorkspaceJobCreateInput):
    try:
        request_body = payload.model_dump()
        request_body["origin"] = "organizational"
        response = await WorkspaceJobClient.create_job(request_body)
        return response
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.get("/{job_id}", response_model=WorkspaceJobStatusOutput)
async def get_workspace_job_status(job_id: str):
    try:
        response = await WorkspaceJobClient.get_job_status(job_id)
        return response
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
