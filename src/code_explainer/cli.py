"""
Command-line interface for Code Explainer.
"""
import argparse
import sys
from pathlib import Path
from typing import Optional

def main(args: Optional[list] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        args: Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    parser = argparse.ArgumentParser(description="Python Code Explainer")
    parser.add_argument(
        "path",
        type=str,
        help="Python file or directory to analyze"
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Recursively process Python files in subdirectories"
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="llama2",
        help="LLM model to use (default: llama2)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file for the report (default: print to console)"
    )
    
    parsed_args = parser.parse_args(args)
    
    try:
        # Import here to avoid loading everything when the CLI is not used
        from .code_analyzer import extract_elements
        from .llm_integration import generate_explanation
        from .document_generator import create_document
        
        # Process the input path (file or directory)
        path = Path(parsed_args.path)
        if not path.exists():
            print(f"Error: Path '{path}' not found", file=sys.stderr)
            return 1

        # Collect all Python files to process
        python_files = []
        if path.is_file() and path.suffix == '.py':
            python_files = [path]
        elif path.is_dir():
            pattern = '**/*.py' if parsed_args.recursive else '*.py'
            python_files = list(path.glob(pattern))
            if not python_files:
                print(f"No Python files found in {path}")
                return 0
        else:
            print(f"Error: Path must be a Python file or directory")
            return 1

        all_code_elements = []
        for py_file in python_files:
            try:
                print(f"Processing {py_file}...", file=sys.stderr)
                code = py_file.read_text(encoding="utf-8")
                elements = extract_elements(code)
                for el in elements:
                    el['file'] = str(py_file.relative_to(path.parent))
                    el['file_path'] = str(py_file)
                all_code_elements.extend(elements)
            except Exception as e:
                print(f"Error processing {py_file}: {e}", file=sys.stderr)

        if not all_code_elements:
            print("No code elements found in any files.")
            return 0
            
        # Generate explanation
        print("\nAnalyzing code...", file=sys.stderr)
        explanation = generate_explanation(all_code_elements, model=parsed_args.model)
        
        # Output the result
        if parsed_args.output:
            output_path = Path(parsed_args.output)
            if output_path.suffix.lower() == '.docx':
                buffer = create_document(all_code_elements, explanation)
                if buffer:
                    output_path.write_bytes(buffer.getvalue())
                    print(f"Report saved to {output_path}")
                else:
                    print("Error: Could not generate Word document. Is python-docx installed?", file=sys.stderr)
                    return 1
            else:
                with output_path.open('w', encoding='utf-8') as f:
                    f.write("# Code Analysis Report\n\n")
                    f.write(explanation)
                print(f"Report saved to {output_path}")
        else:
            print("\n" + "="*80)
            print("CODE ANALYSIS REPORT")
            print("="*80)
            print(explanation)
            
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
