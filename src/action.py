import os
import sys
from pathlib import Path
from typing import List, Dict, Any
from ollama import Client

from .analyzer import extract_elements

def analyze_repository() -> None:
    """Main function to analyze the repository."""
    # Get environment variables
    ollama_model = os.getenv('OLLAMA_MODEL', 'llama2')
    ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    
    # Find all Python files
    python_files = list(Path('.').rglob('*.py'))
    
    all_elements = []
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                code = f.read()
                elements = extract_elements(code)
                for el in elements:
                    el['file'] = str(py_file)
                all_elements.extend(elements)
        except Exception as e:
            print(f"Error processing {py_file}: {e}", file=sys.stderr)
    
    if not all_elements:
        print("No code elements found to analyze.")
        return
    
    # Generate explanation
    client = Client(host=ollama_host)
    
    # Format elements for the prompt
    combined = "\n\n".join(
        f"File: {el['file']}\n"
        f"{el['type']} '{el['name']}':\n"
        f"Location: Lines {el['start_line']}-{el['end_line']}\n"
        f"Documentation: {el['docstring']}\n"
        + (f"Arguments: {', '.join(el['args'])}\n" if el['args'] else "") 
        + ("Returns: Yes\n" if el['has_return'] and el['type'] != 'Class' else "")
        + f"Code:\n{el['source'] or ''}"
        for el in all_elements
    )
    
    system_prompt = f"""You are a helpful assistant. Your job is to explain the Python code and workflow described below 
in plain, non-technical English to someone without a programming background. Avoid technical jargon. 
Use relatable analogies and simple examples where appropriate.

{combined}
"""
    try:
        response = client.chat(
            model=ollama_model,
            messages=[{"role": "user", "content": system_prompt}],
            stream=False
        )
        print("\n" + "="*80)
        print("CODE ANALYSIS REPORT")
        print("="*80)
        print(response['message']['content'])
    except Exception as e:
        print(f"Error generating explanation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    analyze_repository()