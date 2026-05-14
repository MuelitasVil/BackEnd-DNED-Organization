import httpx

from app.configuration.config import settings

base_url = settings.WORKSPACE_MANAGER_URL


class WorkspaceJobClient:
    _client = httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
        limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
    )

    @staticmethod
    async def create_job(payload: dict) -> dict:
        url = f"{base_url}/jobs"
        response = await WorkspaceJobClient._client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    @staticmethod
    async def get_job_status(job_id: str) -> dict:
        url = f"{base_url}/jobs/{job_id}"
        response = await WorkspaceJobClient._client.get(url)
        response.raise_for_status()
        return response.json()
