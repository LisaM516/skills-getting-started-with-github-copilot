from urllib.parse import quote

import src.app as app_module


def test_unregister_successfully_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "michael@mergington.edu"
    request_path = f"/activities/{encoded_activity_name}/participants"

    # Act
    response = client.delete(request_path, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_with_unknown_activity_returns_404(client):
    # Arrange
    request_path = "/activities/Unknown%20Club/participants"
    email = "student@mergington.edu"

    # Act
    response = client.delete(request_path, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_unknown_participant_returns_404(client):
    # Arrange
    request_path = "/activities/Chess%20Club/participants"
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete(request_path, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Participant not found in this activity"


def test_unregister_without_email_returns_422(client):
    # Arrange
    request_path = "/activities/Chess%20Club/participants"

    # Act
    response = client.delete(request_path)
    payload = response.json()

    # Assert
    assert response.status_code == 422
    assert "detail" in payload
