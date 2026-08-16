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