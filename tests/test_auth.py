def test_signup(client):
    response = client.post(
        "/auth/signup",
        json={
            "name": "Test User",
            "email": "pytest_user@example.com",
            "password": "Test@123",
            "age": 21,
            "phone": "9876543210"
        }
    )

  

    assert response.status_code in [200, 201]

#login---------------
def test_login(client):

    #create user required for this test
    signup_response=client.post(
        "/auth/signup",
        json={
            "name":"Login test user",
            "email":"login_test@example.com",
            "password":"Test@123",
            "age":21,
            "phone":"7275584103"
        }
    )

    assert signup_response.status_code in [200,201]
    response = client.post(
        "/auth/login",
        data={
            "username": "login_test@example.com",
            "password": "Test@123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data

#==============================================================

def test_login_invalid_password(client):

    # Create user required for this test
    signup_response = client.post(
        "/auth/signup",
        json={
            "name": "Invalid Password User",
            "email": "invalid_password@example.com",
            "password": "Test@123",
            "age": 21,
            "phone": "9876543212",
        },
    )
    assert signup_response.status_code in [200, 201]


    response=client.post(
        "/auth/login",
        data={
            "username":"invalid_password@example.com",
            "password":"Test@3"
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


#==================================================================

def test_authenticated_user_can_access_protected_endpoint(client):
    #1. Signup
    signup_response=client.post(
        "/auth/signup",
        json={
            "name":"Authenticated user",
            "email":"authenticated@example.com",
            "password":"Test@123",
            "age":21,
            "phone":"9876543213"
        }
    )

    assert signup_response.status_code in [200,201]

    #2. login
    login_response=client.post(
        "/auth/login",
        data={
            "username":"authenticated@example.com",
            "password":"Test@123"
        }
    )

    assert login_response.status_code==200

    tokens=login_response.json()

    access_token=tokens["access_token"]

    #access protected endpoint

    response=client.get(
        "/users/me",
        headers={
            "Authorization":f"Bearer {access_token}",
        }
    )

    assert response.status_code ==200

#==================================================================

def test_refresh_token(client):
    #signup
    signup_response=client.post(
        "/auth/signup",
        json={
            "name":"Refresh test user",
            "email":"refresh@example.com",
            "password":"Test@123",
            "age":21,
            "phone":"9875486123"
        }
    )

    assert signup_response.status_code in[200,201]

    #login

    login_response=client.post(
        "/auth/login",
        data={
            "username":"refresh@example.com",
            "password":"Test@123"

        }
    )

    assert login_response.status_code==200

    tokens=login_response.json()

    refresh_token=tokens["refresh_token"]

    #refresh

    response=client.post(
        "/auth/refresh",
        json={
            "refresh_token":refresh_token
        }
    )

    assert response.status_code ==200

    data=response.json()

    assert "access_token" in data



#=============================================================


def test_revoked_refresh_token_cannot_be_used(client):

    #1. Signup
    signup_response=client.post(
        "/auth/signup",
        json={
            "name": "Revoke Test User",
            "email": "revoke_test@example.com",
            "password": "Test@123",
            "age": 21,
            "phone": "9876543215",
        },
    )

    assert signup_response.status_code in [200,201]

    #2.login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "revoke_test@example.com",
            "password": "Test@123",
        },
    )

    assert login_response.status_code == 200

    tokens = login_response.json()

    refresh_token = tokens["refresh_token"]

    # 3. Logout → revoke refresh token
    logout_response = client.post(
        "/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert logout_response.status_code in [200, 204]

    # 4. Try using the revoked refresh token
    refresh_response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    # 5. Revoked token must be rejected
    assert refresh_response.status_code == 401

#================================================================================

def test_logout_all_devices_revokes_refresh_tokens(client):

    #1.Signup
    signup_response = client.post(
        "/auth/signup",
        json={
            "name": "Logout All Test User",
            "email": "logout_all@example.com",
            "password": "Test@123",
            "age": 21,
            "phone": "9876543216",
        },
    )

    assert signup_response.status_code in [200, 201]

    # 2. Login - Device A
    login_a = client.post(
        "/auth/login",
        data={
            "username": "logout_all@example.com",
            "password": "Test@123",
        },
    )

    assert login_a.status_code == 200

    refresh_token_a = login_a.json()["refresh_token"]

    # 3. Login - Device B
    login_b = client.post(
        "/auth/login",
        data={
            "username": "logout_all@example.com",
            "password": "Test@123",
        },
    )

    assert login_b.status_code == 200

    refresh_token_b = login_b.json()["refresh_token"]

    #make sure two different refresh tokens were issued

    assert refresh_token_a !=refresh_token_b

    # 4. Logout from all devices
    # Use one valid refresh token to identify the user
    logout_all_response = client.post(
        "/auth/logout-all",
        json={
            "refresh_token": refresh_token_a
        },
    )

    assert logout_all_response.status_code in [200,204]

    #both refresh token should be rejected
    refresh_a_response=client.post(
        "/auth/refresh",
        json={
            "refresh_token":refresh_token_a
        }
    )

    refresh_b_response=client.post(
        "/auth/refresh",
        json={
            "refresh_token":refresh_token_b
        }
    )

    assert refresh_a_response.status_code==401
    assert refresh_b_response.status_code==401
