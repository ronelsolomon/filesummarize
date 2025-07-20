import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from .config import settings
from .utils import (
    find_files_by_extension,
    read_file_safely,
    ensure_directory_exists,
    get_llm_client
)
from .analyzer import extract_elements
from .code_explainer.document_generator import create_document

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def collect_python_files(root: Path = Path(".")) -> List[Path]:
    return find_files_by_extension(root, ".py")

def parse_python_file(py_file: Path) -> List[Dict[str, Any]]:
    try:
        code = read_file_safely(py_file, encoding='utf-8')
        elements = extract_elements(code)
        for el in elements:
            el['file'] = str(py_file)
        return elements
        with open(py_file, 'r', encoding='utf-8') as f:
            code = f.read()
            elements = extract_elements(code)
            for el in elements:
                el['file'] = str(py_file)
            return elements
    except Exception as e:
        logger.warning(f"Error processing {py_file}: {e}")
        return []

def build_prompt(elements: List[Dict[str, Any]]) -> str:
    """Build a prompt for the LLM based on the code elements.
    
    Args:
        elements: List of code element dictionaries
        
    Returns:
        Formatted prompt string
    """
    def format_element(el: Dict[str, Any]) -> str:
        """Format a single code element for the prompt."""
        parts = [
            f"File: {el['file']}",
            f"{el['type']} '{el['name']}':",
            f"Location: Lines {el['start_line']}-{el['end_line']}",
            f"Documentation: {el.get('docstring', 'No documentation')}"
        ]
        
        if el.get('args'):
            parts.append(f"Arguments: {', '.join(el['args'])}")
            
        if el.get('has_return', False) and el['type'] != 'Class':
            parts.append("Returns: Yes")
            
        if el.get('source'):
            parts.append(f"Code:\n{el['source']}")
            
        return "\n".join(parts)
    
    # Combine all elements into a single string
    combined = "\n\n".join(format_element(el) for el in elements)
    
    # System prompt with clear instructions
    system_prompt = (
        "You are a helpful code analysis assistant. Your task is to analyze the provided Python code "
        "and explain it in clear, non-technical language that would be understandable to someone "
        "without a programming background. Focus on what the code does and why it's important, "
        "rather than how it works technically. Use analogies and examples to make complex concepts "
        "more accessible.\n\n"
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
    
    return system_prompt

def run_ollama_analysis(prompt: str, model: str, host: str) -> str:
    """Run analysis using the Ollama LLM.
    
    Args:
        prompt: The prompt to send to the model
        model: The model to use for generation
        host: The Ollama server host
        
    Returns:
        The generated text from the model
        
    Raises:
        RuntimeError: If there's an error communicating with the LLM
    """
    try:
        client = get_llm_client()
        response = client.generate(
            prompt=prompt,
            model=model,
            system_prompt=(
                "You are a helpful code analysis assistant. Your task is to analyze "
                "the provided Python code and explain it in clear, non-technical language."
            )
        )
        return response.content
    except Exception as e:
        logger.error(f"Error in LLM analysis: {e}")
        raise RuntimeError(f"Failed to generate analysis: {e}")

def save_document(
    elements: List[Dict[str, Any]],
    explanation: str,
    model: str,
    host: str,
    output_dir: Path
) -> Optional[Path]:
    """Save the analysis document to a file.
    
    Args:
        elements: List of code element dictionaries
        explanation: The generated explanation text
        model: The model used for generation
        host: The Ollama server host
        output_dir: Directory to save the document in
        
    Returns:
        Path to the saved document if successful, None otherwise
    """
    try:
        ensure_directory_exists(output_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        doc_path = output_dir / f"code_analysis_{timestamp}.docx"
        
        logger.info(f"Generating document: {doc_path}")
        doc_buffer = create_document(
            elements=elements,
            explanation=explanation,
            model=model,
            host=host,
            include_summary=True
        )
        
        if not doc_buffer:
            logger.error("Failed to generate document buffer")
            return None
            
        with open(doc_path, 'wb') as f:
            f.write(doc_buffer.getvalue())
            
        logger.info(f"Document successfully saved to: {doc_path}")
        return doc_path
        
    except Exception as e:
        logger.error(f"Error saving document: {e}", exc_info=True)
        return None

def analyze_repository() -> None:
    ollama_model = os.getenv('OLLAMA_MODEL', 'llama2')
    ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')

    logger.info("Collecting .py files ...")
    python_files = collect_python_files()
    if not python_files:
        logger.error("No Python files found!")
        return

    logger.info(f"Found {len(python_files)} Python files.")
    all_elements = []
    for py_file in python_files:
        elements = parse_python_file(py_file)
        if elements:
            all_elements.extend(elements)
        else:
            logger.info(f"No elements extracted from {py_file}")

    if not all_elements:
        logger.error("No code elements found to analyze.")
        return

    prompt = build_prompt(all_elements)

    logger.info("Contacting Ollama LLM ...")
    try:
        explanation = run_ollama_analysis(prompt, ollama_model, ollama_host)
        print("\n" + "="*80)
        print("CODE ANALYSIS REPORT")
        print("="*80)
        print(explanation)
    except Exception as e:
        logger.error(f"Error during LLM analysis: {e}")
        return

    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    try:
        save_document(all_elements, explanation, ollama_model, ollama_host, docs_dir)
    except Exception as e:
        logger.error(f"Document creation failed: {e}")

if __name__ == "__main__":
    analyze_repository()
