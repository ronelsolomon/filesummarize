"""
Code Analyzer AI - A tool for analyzing and explaining code in multiple programming languages using AI.

This package provides functionality to parse code, extract its structure,
and generate explanations using language models.
"""

from .code_analyzer import CodeAnalyzer, extract_elements
from .llm_integration import generate_explanation
from .document_generator import create_document
from .cli import main

__version__ = "0.1.0"

__all__ = [
    "CodeAnalyzer",
    "extract_elements",
    "generate_explanation",
    "create_document",
    "main"
]
