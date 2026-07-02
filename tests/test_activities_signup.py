from urllib.parse import quote

import src.app as app_module


def test_signup_successfully_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "new.student@mergington.edu"
    request_path = f"/activities/{encoded_activity_name}/signup"

    # Act
    response = client.post(request_path, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_with_unknown_activity_returns_404(client):
    # Arrange
    request_path = "/activities/Unknown%20Club/signup"
    email = "student@mergington.edu"

    # Act
    response = client.post(request_path, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_existing_email_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    request_path = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(request_path, params={"email": existing_email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_without_email_returns_422(client):
    # Arrange
    request_path = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(request_path)
    payload = response.json()

    # Assert
    assert response.status_code == 422
    assert "detail" in payload
