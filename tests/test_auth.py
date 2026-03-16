def test_register(client):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "test123"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login(client):
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "test123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_register_duplicate(client):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "test123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] is not None

def test_login_wrong_password(client):
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_nonexistent_user(client):
    response = client.post("/auth/login", data={
        "username": "nobody",
        "password": "test123"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"