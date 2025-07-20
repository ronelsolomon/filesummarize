import pytest
import ast
from src.analyzer import extract_elements

def test_extract_elements_with_functions():
    """Test that extract_elements can parse a simple function."""
    code = """
def hello(name: str) -> str:
    \"\"\"Return a greeting message.\"\"\"
    return f"Hello, {name}!"
"""
    elements = extract_elements(code)
    assert len(elements) == 1
    assert elements[0]['name'] == "hello"
    assert elements[0]['type'] == "Function"
    assert "Return a greeting message" in elements[0]['docstring']
    assert elements[0]['args'] == ['name']
    assert elements[0]['has_return'] is True

def test_extract_elements_with_class():
    """Test that extract_elements can parse a class definition."""
    code = """
class Greeter:
    \"\"\"A class that greets people.\"\"\"
    
    def __init__(self, name: str):
        self.name = name
        
    def greet(self) -> str:
        \"\"\"Return a greeting.\"\"\"
        return f"Hello, {self.name}!"
"""
    elements = extract_elements(code)
    assert len(elements) == 1  # Only the class itself is extracted
    assert elements[0]['type'] == 'Class' and elements[0]['name'] == 'Greeter'

@pytest.fixture
def sample_code():
    return """
def add(a: int, b: int) -> int:
    \"\"\"Add two numbers.\"\"\"
    return a + b
    
class Calculator:
    def multiply(self, x: float, y: float) -> float:
        \"\"\"Multiply two numbers.\"\"\"
        return x * y
"""

def test_extract_elements_with_fixture(sample_code):
    """Test extract_elements using a fixture."""
    elements = extract_elements(sample_code)
    assert len(elements) == 2  # add function and Calculator class
    assert any(e['name'] == 'add' and e['type'] == 'Function' for e in elements)
    assert any(e['name'] == 'Calculator' and e['type'] == 'Class' for e in elements)
