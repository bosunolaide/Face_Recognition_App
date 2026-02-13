import io
import os
import pytest
from main import app as flask_app

@pytest.fixture
def client():
    flask_app.testing = True
    with flask_app.test_client() as client:
        yield client

def test_homepage(client):
    """Ensure homepage loads successfully."""
    response = client.get("/")
    assert response.status_code == 200

def test_health(client):
    """Health endpoint should return 200."""
    response = client.get("/health/")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "ok"


def test_api_predict_missing_file(client):
    """Ensure API returns error when no file is sent."""
    response = client.post("/api/predict")
    assert response.status_code == 400
    assert b"error" in response.data

def test_api_predict_valid_image(client):
    """Send a test image to the /api/predict endpoint."""
    test_image_path = "test_images/01.jpg"
    if not os.path.exists(test_image_path):
        pytest.skip("Test image not found.")
    with open(test_image_path, "rb") as img:
        data = {"image": (io.BytesIO(img.read()), "test.jpg")}
        response = client.post("/api/predict", content_type="multipart/form-data", data=data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert "predictions" in json_data
    assert isinstance(json_data["predictions"], list)
