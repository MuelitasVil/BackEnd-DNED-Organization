from fastapi.testclient import TestClient
from app.main import app
from app.utils.auth import get_current_user


app.dependency_overrides[get_current_user] = lambda: "test-user"

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
