
"""
Code analysis module for extracting structure from Python source code.
"""
import ast
from typing import List, Dict, Any

def extract_elements(code: str) -> List[Dict[str, Any]]:
    """
    Extract all top-level classes and functions with their metadata from Python code.
    
    Args:
        code: Python source code as a string
        
    Returns:
        List of dictionaries containing information about each code element
    """
    try:
        tree = ast.parse(code)
        elements = []
        
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                element_type = node.__class__.__name__.replace('Def', '')
                name = node.name
                doc = ast.get_docstring(node) or ""
                src = ast.get_source_segment(code, node) or ""
                
                start_line = getattr(node, 'lineno', 0)
                end_line = getattr(node, 'end_lineno', start_line)
                
                args = []
                if hasattr(node, 'args') and hasattr(node.args, 'args'):
                    args = [arg.arg for arg in node.args.args]
                
                elements.append({
                    'type': element_type,
                    'name': name,
                    'docstring': doc,
                    'source': src,
                    'start_line': start_line,
                    'end_line': end_line,
                    'args': args if args else None,
                    'has_return': any(isinstance(n, ast.Return) for n in ast.walk(node))
                })
                
        return elements
        
    except SyntaxError as e:
        raise ValueError(f"Error parsing Python code: {e}")
