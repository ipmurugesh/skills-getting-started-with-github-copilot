def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert isinstance(activities["Chess Club"]["participants"], list)


def test_signup_activity(client):
    email = "test.student@mergington.edu"
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_fails(client):
    email = "duplicate@mergington.edu"
    response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": email},
    )

    assert response.status_code == 200

    duplicate = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": email},
    )

    assert duplicate.status_code == 400
    assert duplicate.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_remove_missing_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
