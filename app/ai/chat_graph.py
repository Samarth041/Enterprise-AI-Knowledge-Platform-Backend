from typing import TypedDict,Literal
from langchain_core.messages import BaseMessage,AIMessage, HumanMessage
from langgraph.graph import StateGraph, START,END
from app.ai.cache import get_cached_response, set_cached_response
from app.ai.llm import get_llm
from app.ai.monitoring import start_ai_request , log_ai_request
from app.ai.vector_store import get_vector_store

class ChatState(TypedDict):
    messages:list[BaseMessage]
    route:str
    user_id:int


#=============================
#Router
#================================


def get_route(messages: list[BaseMessage]) -> str:
    """Decide whether the request needs normal chat or RAG."""

    user_message = messages[-1].content

    llm = get_llm()

    prompt = f"""
You are a router for an enterprise AI assistant.

Decide whether the user's question should be answered using:

1. "rag" - if the question requires information
   from the user's uploaded documents.

2. "chat" - if the question is general conversation,
   programming, general knowledge, explanation,
   or does not require uploaded documents.

Return ONLY one word:

rag

or

chat

User question:
{user_message}
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    route = response.content.strip().lower()

    if "rag" in route:
        return "rag"

    return "chat"



def route_message(state:ChatState)->dict:
    route = get_route(state["messages"])

    return {
        "route": route
    }


#---------------------------------------------------------

#normal chat
def generate_response(state:ChatState):
    """
    generate an AI response using the conversation
    contained in graph state.
    
    """

    messages=state["messages"]
    user_message=messages[-1].content
    
    user_id=state["user_id"]

    cache_key=f"{user_id}:{user_message}"

    start_time=start_ai_request()

    #=================================================================
    #Check Cache
    #================================================================

    cached_response=get_cached_response(cache_key)

    if cached_response is not None:
        print("Cache hit")

        log_ai_request(
            user_id=user_id,
            route="chat",
            start_time=start_time,
            success=True
        )

        return{
            "messages":[AIMessage(content=cached_response)]
        }


    #Cache miss-->call gemini
    try:

        print("CACHE MISS")

        llm=get_llm()

        response=llm.invoke(messages)
            

        #========================================================
        #Store response
        #=====================================================
        set_cached_response(cache_key,response.content)

        log_ai_request(
            user_id=user_id,
            route="chat",
            start_time=start_time,
            success=True
        )

        return{
            "messages":[
                response
            ]
        }

    except Exception:
        log_ai_request(
            user_id=user_id,
            route="chat",
            start_time=start_time,
            success=False
        )

        raise

#======================================================
#RAG
#=======================================================

def generate_rag_response(state:ChatState)->dict:
    messages=state["messages"]

    question=messages[-1].content
    user_id=state["user_id"]

    start_time=start_au_request()

    try:

        vector_store=get_vector_store()

        documents=vector_store.similarity_search(
            question,
            k=5,
            filter={
                "user_id": state["user_id"],
            },
        )

        if not documents:

            log_ai_request(
                user_id=user_id,
                route="rag",
                start_time=start_time,
                success=True,
                documents=0
            )
            response=AIMessage(content=("I Could not find any relevant information in the documents"))

            return{
                "messages":[response]
            }

        context="\n\n".join(
            document.page_content for document in documents
        )

        prompt=f"""
        You are an enterprise knowledge assistant.

    Answer the user's question using ONLY
    the provided document context.

    Do not invent information.

    If the answer cannot be found in the context,
    say that the information is not available
    in the uploaded documents.

    DOCUMENT CONTEXT:

    {context}

    USER QUESTION:

    {question}
        """

        llm=get_llm()

        response=llm.invoke(
            [HumanMessage(content=prompt)]
        )

        log_ai_request(
            user_id=user_id,
            route="rag",
            start_time=start_time,
            success=True,
            documents=len(documents),
        )


        return{
            "messages":[response]
        }
    except Exception:

        log_ai_request(
            user_id=user_id,
            route="rag",
            start_time=start_time,
            success=False
        )

        raise

#=====================================================
#conditional Routing
#======================================================

def decide_next_node(state:ChatState)->Literal["chat","rag"]:
    return state["route"]
#=========================================================
#Build graph
#=================================================


graph_builder=StateGraph(ChatState)
graph_builder.add_node("router",route_message)

graph_builder.add_node("chat",generate_response)
graph_builder.add_node("rag",generate_rag_response)


graph_builder.add_edge(START,"router")

graph_builder.add_conditional_edges(
    "router",
    decide_next_node,
    {
        "chat":"chat",
        "rag":"rag"
    }
)

graph_builder.add_edge("chat",END)
graph_builder.add_edge("rag",END)

chat_graph=graph_builder.compile()