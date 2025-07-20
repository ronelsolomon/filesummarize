import os
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from ollama import Client

from .analyzer import extract_elements
from .code_explainer.document_generator import create_document

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
    
    # Create docs directory if it doesn't exist
    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    
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
    
    # Generate explanation
    client = Client(host=ollama_host)
    system_prompt = """You are a helpful assistant. Your job is to explain the Python code and workflow described below 
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
        explanation = response['message']['content']
        print("\n" + "="*80)
        print("CODE ANALYSIS REPORT")
        print("="*80)
        print(explanation)
        
        # Generate and save the document
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        doc_path = docs_dir / f"code_analysis_{timestamp}.docx"
        
        doc_buffer = create_document(all_elements, explanation, "Python Code Analysis Report")
        if doc_buffer:
            with open(doc_path, 'wb') as f:
                f.write(doc_buffer.getvalue())
            print(f"\nDocument generated: {doc_path}")
        else:
            print("\nWarning: Could not generate Word document. Make sure python-docx is installed.")
            
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    analyze_repository()