from typing import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START,END

from app.ai.llm import get_llm

class ChatState(TypedDict):
    messages:list[BaseMessage]

def generate_response(state:ChatState):
    """
    generate an AI response using the conversation
    contained in graph state.
    
    """

    llm=get_llm()

    response=llm.invoke(
        state["messages"]
    )

    return{
        "messages":[
            response
        ]
    }

#=========================================================
#Build graph
#=================================================


graph_builder=StateGraph(ChatState)

graph_builder.add_node("generate_response",generate_response)

graph_builder.add_edge(START,"generate_response")

graph_builder.add_edge("generate_response",END)

chat_graph=graph_builder.compile()