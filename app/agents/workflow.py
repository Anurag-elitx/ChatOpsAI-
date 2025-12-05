import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.agents.tools import get_all_tools

def run_agent(user_message: str):
    """
    Run the multi-step agentic workflow using LangChain and OpenAI.
    """
    tools = get_all_tools()
    
    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Create the prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant for Astiva AI, a Competitive Intelligence platform. "
                   "Use your tools to answer questions about the brand's visibility and internal knowledge."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Construct the OpenAI Functions agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    
    # Create an agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    # Execute the agent
    response = agent_executor.invoke({"input": user_message})
    
    return {
        "status": "success",
        "input": user_message,
        "output": response["output"]
    }
