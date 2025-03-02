import pytest
from dotenv import load_dotenv
import os
from src.client import run_calculator_agent

# Load environment variables before running tests
load_dotenv()

@pytest.mark.asyncio
async def test_calculator_agent():
    """Test that the calculator agent can process basic calculations"""
    try:
        response = await run_calculator_agent("What is 5 plus 3?")
        
        assert response is not None, "No response received"
        assert isinstance(response, dict), "Response should be a dictionary"
        assert "8" in str(response).lower(), "Expected answer (8) not found in response"
        
        print(f"Calculator Response: {response}")
        
    except Exception as e:
        import traceback
        print(f"Full exception traceback:")
        print(traceback.format_exc())
        pytest.fail(f"Failed to run calculator agent: {str(e)}")

@pytest.mark.asyncio
async def test_calculator_complex_operation():
    """Test that the calculator agent can handle more complex calculations"""
    try:
        response = await run_calculator_agent("What is 10 times 5 divided by 2 plus 3?")
        
        assert response is not None, "No response received"
        assert isinstance(response, dict), "Response should be a dictionary"
        assert "28" in str(response).lower(), "Expected answer (28) not found in response"
        
        print(f"Complex Calculation Response: {response}")
        
    except Exception as e:
        import traceback
        print(f"Full exception traceback:")
        print(traceback.format_exc())
        pytest.fail(f"Failed to run complex calculation: {str(e)}") 