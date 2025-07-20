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
    system_prompt = (
    "You are a helpful assistant. Your job is to explain the Python code and workflow described below "
    "in plain, non-technical English to someone without a programming background. Avoid technical jargon. "
    "Use relatable analogies and simple examples where appropriate.\n\n"

    "📌 Task Overview:\n"
    "- Break down the Python code into understandable parts.\n"
    "- Present the explanation in a two-column table:\n"
    "    1. Section of the prompt\n"
    "    2. Whether it is dynamic or static\n\n"

    "🧠 User Context:\n"
    "- The user is building an automated assessment tool using LLMs.\n"
    "- The tool generates subtopics and test questions from a topic + grade + learning objective.\n"
    "- They want help modifying Prompt 1 to include a new variable: the learning objective.\n\n"

    "💡 Input Example:\n"
    "    topic = 'Ratios and Proportional Relationships'\n"
    "    student_class = '6th standard'\n"
    "    learning_objective = 'Understand ratio concepts and use ratio reasoning to solve problems.'\n\n"

    "📝 Full Prompt 1 (Subtopic Generator):\n"
    "I want a list of sub-topics for the topic \"{topic}\" which is taught to a \"{student_class}\" student "
    "with a learning objective \"{learning_objective}\".\n"
    "First, output the learning objective exactly as given.\n"
    "Then, output the sub-topics ONLY as a Python list. Do not include any commentary or explanation.\n\n"

    "🔧 System Context:\n"
    "We are building an automated assessment web app where questions are usually uploaded manually into a MySQL database. "
    "This tool uses large language models to generate those questions automatically, saving time and effort.\n\n"

    "📋 Additional User Requests:\n"
    "- Modify the original code to include the new learning objective variable.\n"
    "- Ensure that generate_questions_for_subtopic also uses the learning objective.\n"
    "- Recreate the dynamic/static breakdown table of Prompt 1 and Prompt 2.\n"
    "- Show an example of what Prompt 1 and Prompt 2 look like after the code runs.\n"
    "- Give a step-by-step guide to feeding these prompts into a ChatGPT conversation.\n"
    "- Convert the instructions into clean documentation.\n"
    "- Provide a downloadable .docx version of the documentation.\n\n"

    f"{combined}\n\n"
    "🧾 Now, please provide a detailed, beginner-friendly explanation:"
)
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
        
        doc_buffer = create_document(
            all_elements, 
            explanation,
            model=ollama_model,
            host=ollama_host
        )
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