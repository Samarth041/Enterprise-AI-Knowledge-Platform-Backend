from unittest.mock import patch
from langchain_core.messages import AIMessage



def test_chat_requires_authentication(client):
    response=client.post(
        "/chat",
        json={
            "session_id":1,
            "message":"Hello"
        }
    )

    assert response.status_code in [401,403]

#==========================================================
def test_chat_authenticated(auth_client):
    fake_graph_result={
        "messages":[
            AIMessage(
                content="hello ! how can i help you?"
            )
        ]
    }

    with patch(
        "app.services.chat_service.chat_graph.invoke",
        return_value=fake_graph_result
    ):
        response=auth_client.post(
            "/chat",
            json={
                "session_id":None,
                "message":"Hello"
            }
        )

    assert response.status_code == 200

    data=response.json()

    assert "session_id" in data
    assert "response" in data

    assert data["response"]=="hello ! how can i help you?"


#===================================================================

def test_chat_creates_session_and_messages(auth_client):
    fake_graph_result = {
        "messages": [
            AIMessage(
                content="This is a test response."
            )
        ]
    }

    with patch(
        "app.services.chat_service.chat_graph.invoke",
        return_value=fake_graph_result,
    ):
        response = auth_client.post(
            "/chat",
            json={
                "session_id": None,
                "message": "What is FastAPI?",
            },
        )

    assert response.status_code == 200

    data = response.json()

    session_id = data["session_id"]

    assert session_id is not None
    assert data["response"] == "This is a test response."

#================================================================

#==========================================================
#List chat sessions
#===============================================================

def test_list_chat_sessions(auth_client):
    fake_graph_result = {
        "messages": [
            AIMessage(content="Test response")
        ]
    }

    with patch(
        "app.services.chat_service.chat_graph.invoke",
        return_value=fake_graph_result,
    ):
        chat_response = auth_client.post(
            "/chat",
            json={
                "session_id": None,
                "message": "Create a session",
            },
        )

    assert chat_response.status_code == 200

    response = auth_client.get("/chat/sessions")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1

#=================================================================
#get chat history
#======================================================================

def test_get_chat_history(auth_client):
    fake_graph_result = {
        "messages": [
            AIMessage(
                content="This is the AI response."
            )
        ]
    }

    with patch(
        "app.services.chat_service.chat_graph.invoke",
        return_value=fake_graph_result,
    ):
        chat_response = auth_client.post(
            "/chat",
            json={
                "session_id": None,
                "message": "Hello",
            },
        )

    assert chat_response.status_code == 200

    session_id = chat_response.json()["session_id"]

    response = auth_client.get(
        f"/chat/session/{session_id}"
    )

    assert response.status_code == 200


#===================================================================
#nonexistent session
#================================================================

def test_get_non_existent_chat_session(auth_client):
    response=auth_client.get(
        "/chat/session/999999"
    )

    assert response.status_code==404

#======================================================================
def test_delete_chat_session(auth_client):

    fake_graph_result = {
        "messages": [
            AIMessage(
                content="Temporary response"
            )
        ]
    }

    with patch(
        "app.services.chat_service.chat_graph.invoke",
        return_value=fake_graph_result,
    ):
        chat_response = auth_client.post(
            "/chat",
            json={
                "session_id": None,
                "message": "Temporary chat",
            },
        )

    assert chat_response.status_code == 200

    session_id = chat_response.json()["session_id"]

    delete_response = auth_client.delete(
        f"/chat/sessions/{session_id}"
    )

    assert delete_response.status_code == 200

    history_response = auth_client.get(
        f"/chat/session/{session_id}"
    )

    assert history_response.status_code == 404


# ============================================================
# Session Ownership / Authorization
# ============================================================

def test_user_cannot_access_another_users_session(client):
    # --------------------------------------------------------
    # User A: Signup
    # --------------------------------------------------------

    signup_a = client.post(
        "/auth/signup",
        json={
            "name": "Chat User A",
            "email": "chat_user_a@example.com",
            "password": "Test@123",
            "age": 21,
            "phone": "9876543218",
        },
    )

    assert signup_a.status_code in [200, 201]

    # --------------------------------------------------------
    # User A: Login
    # --------------------------------------------------------

    login_a = client.post(
        "/auth/login",
        data={
            "username": "chat_user_a@example.com",
            "password": "Test@123",
        },
    )

    assert login_a.status_code == 200

    token_a = login_a.json()["access_token"]

    client.headers.update(
        {
            "Authorization": f"Bearer {token_a}"
        }
    )

    # --------------------------------------------------------
    # User A: Create session
    # --------------------------------------------------------

    fake_graph_result = {
        "messages": [
            AIMessage(
                content="User A response"
            )
        ]
    }

    with patch(
        "app.services.chat_service.chat_graph.invoke",
        return_value=fake_graph_result,
    ):
        chat_response = client.post(
            "/chat",
            json={
                "session_id": None,
                "message": "User A private message",
            },
        )

    assert chat_response.status_code == 200

    session_id = chat_response.json()["session_id"]

    # --------------------------------------------------------
    # User B: Signup
    # --------------------------------------------------------

    signup_b = client.post(
        "/auth/signup",
        json={
            "name": "Chat User B",
            "email": "chat_user_b@example.com",
            "password": "Test@123",
            "age": 21,
            "phone": "9876543219",
        },
    )

    assert signup_b.status_code in [200, 201]

    # --------------------------------------------------------
    # User B: Login
    # --------------------------------------------------------

    login_b = client.post(
        "/auth/login",
        data={
            "username": "chat_user_b@example.com",
            "password": "Test@123",
        },
    )

    assert login_b.status_code == 200

    token_b = login_b.json()["access_token"]

    client.headers.update(
        {
            "Authorization": f"Bearer {token_b}"
        }
    )

    # --------------------------------------------------------
    # User B tries to access User A's session
    # --------------------------------------------------------

    response = client.get(
        f"/chat/session/{session_id}"
    )

    # User A's session must not be visible to User B
    assert response.status_code == 404


#=====================================================================
#Streaming Chat
#====================================================================


def test_stream_chat(auth_client):
    def fake_stream_response(history,user_id):
        yield "Hello"
        yield " from"
        yield " AI"

    with patch(
        "app.services.chat_service.stream_response",
        side_effect=fake_stream_response
    ):
        response=auth_client.post(
            "/chat/stream",
            json={
                "session_id":None,
                "message":"Hello"
            }
        )

    assert response.status_code==200

    assert response.headers["content-type"].startswith(
        "text/event-stream"
    )

    assert "X-Session-ID" in response.headers

    body=response.text

    assert "event: token" in body
    assert "Hello" in body
    assert "event:done" in body