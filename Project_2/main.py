from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

def  main():
    model = ChatOpenAI(temperature =0)

    tools =[]
    agent_executor = create_react_agent(model,tools)

    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("YOu can ask me to perform calculations or chat with me.")

    while True:
        user_input = input("\n You: ").strip()

        if user_input == "quit":
            break
        
        print("\n Assistant: ",end="")
        for chunk in agent_executor.stream(
            {
                "messages":[HumanMessage(content = user_input)]
            }
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content,end="")
        print()

if __name__ == "__main__":
    main()