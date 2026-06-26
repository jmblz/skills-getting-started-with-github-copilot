from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_remove_participant_from_activity():
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    activities_response = client.get("/activities")
    assert "michael@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]


def test_remove_participant_returns_not_found_for_unknown_activity():
    response = client.delete("/activities/Unknown Activity/participants/test@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_activities_endpoint_prevents_caching():
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
