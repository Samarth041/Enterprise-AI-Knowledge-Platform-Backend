from langchain_core.messages import HumanMessage,AIMessage

from app.ai.llm import get_llm

def chat(message:str)->str:
    """
    Generate an AI response from the conversation history.
    """

    history=[]

    for message in messages:
        if message.role=="user":
            history.append(
                HumanMessage(content=message.content)
            )

        else:
            history.append(
                AIMessage(
                    content=message.content
                )
            )

    response=llm.invoke(history)

    return response.content