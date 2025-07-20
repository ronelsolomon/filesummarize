"""
Code Explainer - A tool for analyzing and explaining Python code using AI.

This package provides functionality to parse Python code, extract its structure,
and generate non-technical explanations using language models.
"""

from .code_analyzer import extract_elements
from .llm_integration import generate_explanation
from .document_generator import create_document

__version__ = "0.1.0"
__all__ = ['extract_elements', 'generate_explanation', 'create_document']
