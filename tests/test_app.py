from app.app import app


def test_home_returns_project_name():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["project"] == "Secure Collaborative DevOps"


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
