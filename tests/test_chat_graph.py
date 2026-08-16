from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage, HumanMessage

from app.ai.chat_graph import chat_graph


#=======================================================
#Fake LLM
class FakeLLM:
    def __init__(self, responses):
        self.responses = iter(responses)

    def invoke(self, messages):
        return AIMessage(content=next(self.responses))

#=================================================================
#fake vector store
#=================================================================

class FakeVectorStore:
    def similarity_search(self,query,k,filter):
        return[
            MagicMock(
                page_content=(
                    "FastAPI is a Python web framework "
                    "for building APIs."
                )
            )
        ]


#=============================================================
#Normal Chat
#=============================================================

def test_chat_graph_routes_to_chat():
    fake_llm=FakeLLM(
        [
            "chat",
            "Hello! How can i help you?"
        ]
    )

    with patch(
        "app.ai.chat_graph.get_llm",
        return_value=fake_llm
    ):  
        result=chat_graph.invoke(
            {
                "messages":[
                    HumanMessage(content="Hello")
                ],
                "route":"",
                "user_id":1
            }
        )

    assert result["route"]=="chat"

    assert(
        result["messages"][-1].content=="Hello! How can i help you?"
    )

#================================================
#RAG
#==================================================

def test_chat_graph_routes_to_rag():
    fake_llm = FakeLLM(
        [
            "rag",
            "FastAPI is a Python web framework.",
        ]
    )

    fake_vector_store = FakeVectorStore()

    with patch(
        "app.ai.chat_graph.get_llm",
        return_value=fake_llm,
    ), patch(
        "app.ai.chat_graph.get_vector_store",
        return_value=fake_vector_store,
    ):
        result = chat_graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=(
                            "What does my uploaded "
                            "document say about FastAPI?"
                        )
                    )
                ],
                "route": "",
                "user_id": 1,
            }
        )

    assert result["route"] == "rag"

    assert (
        result["messages"][-1].content
        == "FastAPI is a Python web framework."
    )
