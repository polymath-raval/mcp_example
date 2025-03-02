import pytest
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os

# Load environment variables before running tests
load_dotenv()

def test_openai_api_key_exists():
    """Test that the OpenAI API key is set in environment variables"""
    assert 'openrouter_key' in os.environ, "openrouter_key not found in environment variables"
    assert os.environ['openrouter_key'].startswith('sk-or-'), "openrouter_key format appears invalid"

@pytest.mark.asyncio
async def test_openai_connection():
    """Test that we can successfully connect to OpenAI via OpenRouter"""
    try:
        # Initialize the chat model with OpenRouter configuration
        model = ChatOpenAI(
            model="openai/gpt-4",
            openai_api_key=os.getenv('openrouter_key'),
            openai_api_base="https://openrouter.ai/api/v1",
            max_tokens=1000
        )
        
        # Create a proper LangChain message
        messages = [
            HumanMessage(content="Say 'Hello, test passed!'")
        ]
        
        # Invoke the model with the correct message format
        response = await model.ainvoke(messages)
        
        # Verify we got a response
        assert response is not None, "No response received"
        assert hasattr(response, 'content'), "Response has no content attribute"
        assert isinstance(response.content, str), "Response content is not a string"
        assert len(response.content) > 0, "Empty response received"
        
        print(f"OpenRouter Response: {response.content}")
        
    except Exception as e:
        import traceback
        print(f"Full exception traceback:")
        print(traceback.format_exc())
        pytest.fail(f"Failed to connect to OpenRouter: {str(e)}") 