def test_chat_requires_authentication(client):
    response=client.post(
        "/chat",
        json={
            "session_id":1,
            "message":"Hello"
        }
    )

    assert response.status_code in [401,403]