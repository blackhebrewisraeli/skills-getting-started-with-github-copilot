import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]

    # restore state for subsequent tests
    activities[activity_name]["participants"].append(email)


def test_activities_endpoint_disables_browser_caching():
    client = TestClient(app)

    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"].lower() == "no-store"
