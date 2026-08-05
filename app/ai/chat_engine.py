from langchain_core.messages import HumanMessage,AIMessage

from app.ai.llm import get_llm

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