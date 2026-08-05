from langchain_core.messages import HumanMessage

from app.ai.llm import get_llm

def chat(message:str)->str:
    """
    Sends a message to the LLM and returns the response
    """

    llm=get_llm()

    response=llm.invoke(
        [
            HumanMessage(content=message)
        ]
    )

    return response.content