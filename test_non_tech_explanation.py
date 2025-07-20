"""
Test script for the non-technical explanation feature.
"""
import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from src.code_explainer.document_generator import generate_non_tech_explanation

def test_non_tech_explanation():
    """Test the non-technical explanation generation."""
    # Sample code elements that would come from the analyzer
    sample_elements = [
        {
            'name': 'calculate_total',
            'type': 'Function',
            'docstring': 'Calculates the total price of items in a shopping cart.',
            'args': ['items', 'tax_rate'],
            'has_return': True,
            'source': 'def calculate_total(items, tax_rate=0.08):\n    """Calculates the total price of items in a shopping cart."""\n    subtotal = sum(item["price"] for item in items)\n    tax = subtotal * tax_rate\n    return subtotal + tax',
            'start_line': 10,
            'end_line': 15
        },
        {
            'name': 'ShoppingCart',
            'type': 'Class',
            'docstring': 'Represents a shopping cart with items and checkout functionality.',
            'source': 'class ShoppingCart:\n    """Represents a shopping cart with items and checkout functionality."""\n    def __init__(self):\n        self.items = []\n    \n    def add_item(self, item):\n        self.items.append(item)',
            'start_line': 18,
            'end_line': 25
        }
    ]
    
    # Generate the explanation
    explanation, elements = generate_non_tech_explanation(sample_elements)
    
    # Print the results
    print("=" * 80)
    print("NON-TECHNICAL EXPLANATION")
    print("=" * 80)
    print(explanation)
    
    print("\n" + "=" * 80)
    print("CODE ELEMENT DESCRIPTIONS")
    print("=" * 80)
    for elem in elements:
        print(f"\n{elem.type}: {elem.name}")
        print(f"Description: {elem.description}")
        if elem.example:
            print(f"Example: {elem.example}")

if __name__ == "__main__":
    test_non_tech_explanation()
