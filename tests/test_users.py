
def test_register_user(client):
    response = client.post("/auth/register", json={
        "nombre": "Test",
        "email": "test@test.com",
        "password": "test",
    })
    assert response.status_code == 201
    assert response.json()["nombre"] == "Test"
    assert response.json()["email"] == "test@test.com"

def test_login_user(client):
    
    register = client.post("/auth/register", json={
        "nombre": "Test User",
        "email": "test@test.com",
        "password": "testpassword"
    })
    assert register.status_code == 201
    
    
    response = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()