import pytest
from tests.conftest import client

def get_auth_token(client):
    client.post("/auth/register", json={
        "username": "issueuser",
        "email": "issue@gmail.com",
        "password": "test123"
    })
    response = client.post("/auth/login", data={
        "username": "issueuser",
        "password": "test123"
    })
    return response.json()["access_token"]

def test_create_issue(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/issues/", json={
        "title": "Test pipeline failure",
        "description": "Test description",
        "pipeline_name": "test_pipeline",
        "error_message": "Test error",
        "severity": "HIGH"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test pipeline failure"
    assert response.json()["status"] == "OPEN"

def test_create_issue_no_token(client):
    response = client.post("/issues/", json={
        "title": "Test pipeline failure",
        "pipeline_name": "test_pipeline",
    })
    assert response.status_code == 401

def test_get_all_issues(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/issues/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_all_issues_no_token(client):
    response = client.get("/issues/")
    assert response.status_code == 401

def test_get_issue(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/issues/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_issue_not_found(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/issues/9999", headers=headers)
    assert response.status_code == 404

def test_update_issue(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.patch("/issues/1", json={
        "status": "IN_PROGRESS",
        "assigned_to": "issueuser"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"

def test_update_issue_not_found(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.patch("/issues/9999", json={
        "status": "IN_PROGRESS"
    }, headers=headers)
    assert response.status_code == 404

def test_delete_issue(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete("/issues/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "CLOSED"