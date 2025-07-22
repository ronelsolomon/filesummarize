"""
Code Analysis Tool - A tool for analyzing and explaining Python code using AI.
"""

__version__ = "0.1.0"

from .analyzer import analyze_code
from .cli import main

__all__ = ['analyze_code', 'main']
