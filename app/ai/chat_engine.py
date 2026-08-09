from langchain_core.messages import HumanMessage,AIMessage
from app.ai.vector_store import get_vector_store
from app.ai.llm import get_llm
from app.ai.chat_graph import get_route

def generate_response(history):
    """
    Generate an AI response from the conversation history.
    """

    print("inside generate_response")
    llm=get_llm()
    langchain_messages=[]

    for message in history:
        print(message.role,":",message.content)
        if message.role=="user":
            langchain_messages.append(
                HumanMessage(content=message.content)
            )

        else:
            langchain_messages.append(
                AIMessage(
                    content=message.content
                )
            )

    print("Calling gemini...")

    response=llm.invoke(langchain_messages)

    print("Gemini replied:",response.content)

    return response.content


#--------------------------------------------------------------
def stream_response(history,user_id):
    """
    Stream an AI response using the same chat/RAG routing as the normal chat endpoint.
    """

    llm=get_llm()

    #Convert database history-->Langchain messages
    langchain_messages=[]

    for message in history:
        if message.role=="user":
            langchain_messages.append(HumanMessage(content=message.content))

        elif message.role == "assistant":
            langchain_messages.append(
                AIMessage(content=message.content)
            )

    #===========================================================
    #Decide whether this is chat or Rag
    #=============================================================

    route=get_route(langchain_messages)
    #==========================================
    #Normal chat
    #=========================================

    if route=="chat":
        for chunk in llm.stream(langchain_messages):
            if chunk.content:
                yield chunk.content

        return 

    #==============================
    #Rag
    #=================================


    vector_store=get_vector_store()

    user_message=langchain_messages[-1].content

    documents=vector_store.similarity_search(
        user_message,
        k=5,
        filter={
            "user_id":user_id
        }
    )

    if not documents:
        yield(
            "I could not find any relevant information "
            "in your uploaded documents."
        )

        return

    context="\n\n".join(document.page_content for document in documents)

    prompt = f"""
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

{user_message}
"""

    # Stream RAG answer

    for chunk in llm.stream(
        [HumanMessage(content=prompt)]
    ):

        if chunk.content:
            yield chunk.content