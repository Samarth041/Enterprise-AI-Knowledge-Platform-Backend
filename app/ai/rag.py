from langchain_core.messages import HumanMessage
from pathlib import Path
from app.ai.llm import get_llm
from app.ai.vector_store import get_vector_store

def generate_rag_response(question:str,user_id:int):
    """
    Generate an answer using documents belonging to the current user
    """

    vector_store=get_vector_store()

    #===========================================================
    #Retrieve relevant documents
    #============================================================

    documents=vector_store.similarity_search(
        question,
        k=5,
        filter={
            "user_id":user_id
        }
    )

    #==========================================================
    #No relevant documents
    #============================================================


    if not documents:
        return "I could not find any relevant information in your documents"

    #====================================================================
    #Build Context
    #====================================================================

    context="\n\n".join(
        document.page_content
        for document in documents
    )


    #=====================================
    #Build Prompt
    #===========================================


    prompt=f"""
    You are an AI Assistant that answers questions using the provided document text.

    Rules:
    1.Answer using only the provided context
    2.If the answer cannot be found in the context,
    say that you don't know
    3.Do not invent information

    Document context:
    {context}

    Question
    {question}
    """

    #=============================================================
    #Generate response
    #===========================================================

    llm=get_llm()

    response=llm.invoke(
        [
            HumanMessage(content=prompt)
        ]
    )

    


    #===========================================================
    #build source information
    #==============================================================


    sources=[]

    for document in documents:
        metadata=document.metadata

        source=metadata.get("source","")

        filename=Path(source).name

        sources.append(
            {
                "document_id":metadata.get("document_id"),
                "filename":filename,
                "page":metadata.get("page")

            }
        )


    return {
        "answer":response.content,
        "sources":sources
    }
