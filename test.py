from langchain_core.messages import HumanMessage

from app.ai.chat_graph import chat_graph

result=chat_graph.invoke(
    {
        "messages":[
            HumanMessage(content="What is FastAPi?")
        ]
    }
)


print(result["messages"][-1].content)