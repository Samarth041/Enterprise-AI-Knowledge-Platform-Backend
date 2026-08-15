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