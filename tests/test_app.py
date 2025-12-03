import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestActivities:
    """Test suite for activities endpoints"""

    def test_get_activities(self):
        """Test retrieving all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "Chess Club" in data

    def test_get_activities_structure(self):
        """Test that activities have the correct structure"""
        response = client.get("/activities")
        data = response.json()
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

    def test_signup_for_activity_success(self):
        """Test successful signup for an activity"""
        email = "testuser@mergington.edu"
        activity = "Chess Club"
        
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_signup_duplicate_student(self):
        """Test that a student cannot sign up twice for the same activity"""
        email = "duplicate@mergington.edu"
        activity = "Programming Class"
        
        # First signup should succeed
        response1 = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert response1.status_code == 200
        
        # Second signup should fail
        response2 = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert response2.status_code == 400
        data = response2.json()
        assert "already signed up" in data["detail"].lower()

    def test_signup_nonexistent_activity(self):
        """Test signup for a non-existent activity"""
        email = "testuser@mergington.edu"
        activity = "Nonexistent Activity"
        
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert response.status_code == 404

    def test_unregister_success(self):
        """Test successful unregistration from an activity"""
        email = "unreg@mergington.edu"
        activity = "Tennis Club"
        
        # First, sign up
        signup_response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert signup_response.status_code == 200
        
        # Then, unregister
        unreg_response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert unreg_response.status_code == 200
        data = unreg_response.json()
        assert "message" in data

    def test_unregister_not_signed_up(self):
        """Test unregistering a student who is not signed up"""
        email = "notregistered@mergington.edu"
        activity = "Drama Club"
        
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert response.status_code == 400

    def test_root_redirect(self):
        """Test that root path redirects to static HTML"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
