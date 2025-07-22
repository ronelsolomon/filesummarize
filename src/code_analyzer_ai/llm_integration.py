"""
LLM integration module for generating code explanations.
"""
from typing import List, Dict, Any
from ollama import Client

def generate_explanation(code_elements: List[Dict[str, Any]], model: str = "llama2") -> str:
    """
    Generate a non-technical explanation of the code using the specified LLM.
    
    Args:
        code_elements: List of code element dictionaries from extract_elements()
                       Each element may contain a 'file' key indicating its source file.
        model: Name of the LLM model to use (default: "llama2")
        
    Returns:
        Generated explanation as a string
    """
    if not code_elements:
        return "No code elements to analyze."
    
    try:
        # Group elements by file
        elements_by_file = {}
        for el in code_elements:
            file_name = el.get('file', 'main.py')
            if file_name not in elements_by_file:
                elements_by_file[file_name] = []
            elements_by_file[file_name].append(el)
        
        # Compile code elements into a formatted string, grouped by file
        combined_parts = []
        for file_name, elements in elements_by_file.items():
            file_section = f"# File: {file_name}\n\n"
            
            for el in elements:
                element_section = (
                    f"## {el['type']} '{el['name']}'\n"
                    f"Location: Lines {el['start_line']}-{el['end_line']}\n"
                )
                
                if el['docstring']:
                    element_section += f"Documentation: {el['docstring']}\n"
                    
                if el['args']:
                    element_section += f"Arguments: {', '.join(el['args'])}\n"
                    
                if el['type'] != 'Class' and el['has_return']:
                    element_section += "Returns: Yes\n"
                    
                element_section += f"Code:\n```python\n{el['source'] or ''}\n```\n\n"
                file_section += element_section
            
            combined_parts.append(file_section)
        
        combined = "\n".join(combined_parts)
        
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
        
        client = Client(host='http://localhost:11434')
        response = client.chat(
            model=model,
            messages=[{"role": "user", "content": system_prompt}],
            stream=False
        )
        
        return response['message']['content']
        
    except Exception as e:
        raise RuntimeError(f"Error generating explanation: {str(e)}")
