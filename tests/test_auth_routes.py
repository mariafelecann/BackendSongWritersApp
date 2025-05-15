def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Registration successful"

def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "securepassword"
    })
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 409
    assert "Email already registered" in response.get_json()["error"]

def test_login_success(client):
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "securepassword"
    })
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "securepassword"
    })

    json_data = response.get_json()
    assert response.status_code == 200
    assert "email" in json_data
    assert "token" in json_data


def test_logout_success(client):
    client.post("/auth/register", json={
        "email": "logout@example.com",
        "password": "logoutpass"
    })
    client.post("/auth/login", json={
        "email": "logout@example.com",
        "password": "logoutpass"
    })
    response = client.post("/auth/logout", json={
        "email": "logout@example.com"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "Successfully logged out"

def test_delete_account_success(client):
    client.post("/auth/register", json={
        "email": "delete@example.com",
        "password": "deletepass"
    })
    response = client.post("/auth/delete_account", json={
        "email": "delete@example.com",
        "password": "deletepass"
    })
    assert response.status_code == 200
    assert "Account successfully deleted" in response.get_json()["messag"]
