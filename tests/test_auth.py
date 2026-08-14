def test_signup(client):
    response=client.post(
        "auth/signup",
        json={
            "name":"Test User",
            "email":"pytest_user@example.com",
            "password":"Test@123"
        }
    )

    assert response.status_code in [200,201]


#login---------------

def test_login(client):
    response=client.post(
        "/auth/login",
        data={
            "username":"pytest_user@example.com",
            "password":"Test@123"
        }
    )

    assert response.status_code==200

    data=response.json()

    assert "access_token" in data
    assert "refresh_token" in data


#==============================================================

def test_login_invalid_password(client):
    response=client.post(
        "/auth/login",
        data={
            "username":"pytest_user@example.com",
            "password":"Test@123"
        }
    )
    assert response.status_code==401


#=====================================================================

def test_protected_endpoint_without_token(client):
    response=client.get("/users/me")

    assert response.status_code in [401,403]

#=========================================================================

def test_protected_endpoint_invalid_token(client):
    response=client.get(
        "/users/me",
        headers={
            "Authorization":"Bearer invalid-token"
        }
    )

    assert response.status_code==401

