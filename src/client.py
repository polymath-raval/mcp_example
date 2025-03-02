import asyncio
from typing import Dict, Any
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

# Load environment variables from .env file
load_dotenv()

async def run_calculator_agent(calculation: str) -> Dict[str, Any]:
    """
    Run the calculator agent with the given calculation
    
    Args:
        calculation: The calculation to process
    
    Returns:
        The response from the agent
    """
    model = ChatOpenAI(
        model="openai/gpt-4",
        openai_api_key=os.getenv('openrouter_key'),
        openai_api_base="https://openrouter.ai/api/v1",
        max_tokens=1000
    )
    
    async with MultiServerMCPClient() as client:
        await client.connect_to_server(
            "calculator",
            command="python",
            args=["src/servers/calculator_server.py"],
        )
        
        agent = create_react_agent(model, client.get_tools())
        response = await agent.ainvoke({"messages": calculation})
        
        print(f"\nQuestion: {calculation}")
        print(f"Response: {response}")
        
        return response

if __name__ == "__main__":
    # Run some example calculations when script is run directly
    calculations = [
        "What is 15 plus 27?",
        "What is 100 divided by 5?",
        "What is 12 times 8 minus 15?"
    ]
    
    async def run_examples():
        for calc in calculations:
            await run_calculator_agent(calc)
    
    asyncio.run(run_examples()) 