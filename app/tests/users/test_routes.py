
from fastapi.testclient import TestClient
from app.main import app
from app.auth.dependencies import get_current_active_user

# Mock user
def override_current_active_user():
    return {
        "email": "test@example.com",
        "firstname": "Test",
        "lastname": "User",
        "is_active": True
    }

# Override dependency
app.dependency_overrides[get_current_active_user] = override_current_active_user

def test_get_current_user_profile():
    client = TestClient(app)
    response = client.get("/users/me")
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["firstname"] == "Test"
    assert data["lastname"] == "User"
    assert data["is_active"] is True
