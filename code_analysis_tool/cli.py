"""Command-line interface for the code analysis tool."""
import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from .analyzer import analyze_code

def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze Python code using AI to generate explanations."
    )
    
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to a Python file or directory to analyze (default: current directory)",
    )
    
    parser.add_argument(
        "--model",
        default="llama3",
        help="Ollama model to use for analysis (default: llama3)",
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output file to save results (default: print to stdout)",
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )
    
    parser.add_argument(
        "--exclude",
        nargs="+",
        default=["__pycache__", ".git", ".github", "venv", "env", "node_modules"],
        help="Directories to exclude from analysis",
    )
    
    parser.add_argument(
        "--extensions",
        nargs="+",
        help="File extensions to include (without leading .). If not specified, all supported file types are included.",
    )
    
    parser.add_argument(
        "--list-extensions",
        action="store_true",
        help="List all supported file extensions and exit",
    )
    
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version and exit",
    )
    
    return parser.parse_args(args)

def print_analysis(results: dict, output_format: str = "text", output_file: Optional[str] = None):
    """Print or save analysis results."""
    if output_format == "json":
        output = json.dumps(results, indent=2, ensure_ascii=False)
    else:
        output = []
        for file_path, analysis in results.items():
            file_type = analysis.get('file_type', 'unknown')
            sub_type = analysis.get('sub_type', 'unknown')
            
            output.append(f"\n{'='*100}")
            output.append(f"File: {file_path} ({file_type}/{sub_type})")
            output.append(f"{'='*100}\n")
            
            if 'error' in analysis:
                output.append(f"Error: {analysis['error']}\n")
                continue
                
            analysis_text = analysis.get('analysis', 'No analysis available')
            output.append(analysis_text)
            
            # Add a summary of elements if available
            elements = analysis.get('elements', [])
            if elements and len(elements) > 1:  # Only show if there are multiple elements
                output.append("\nElements found:")
                for element in elements:
                    element_type = element.get('type', 'element')
                    name = element.get('name', 'unnamed')
                    output.append(f"  - {element_type}: {name}")
            
        output = "\n".join(output)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Analysis saved to {output_file}")
    else:
        print(output)

def list_supported_extensions() -> None:
    """List all supported file extensions and their types."""
    print("Supported file extensions:")
    print("\nCode files:")
    code_exts = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.jsx': 'JavaScript (React)',
        '.ts': 'TypeScript',
        '.tsx': 'TypeScript (React)',
        '.java': 'Java',
        '.c': 'C',
        '.cpp': 'C++',
        '.h': 'C/C++ Header',
        '.hpp': 'C++ Header',
        '.cs': 'C#',
        '.go': 'Go',
        '.rs': 'Rust',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.sh': 'Shell Script',
        '.pl': 'Perl',
        '.r': 'R',
        '.m': 'MATLAB',
        '.jl': 'Julia'
    }
    
    for ext, lang in sorted(code_exts.items()):
        print(f"  {ext:8} - {lang}")
    
    print("\nData files:")
    data_exts = {
        '.json': 'JSON',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.xml': 'XML',
        '.csv': 'CSV',
        '.toml': 'TOML',
        '.ini': 'INI',
        '.cfg': 'Config'
    }
    
    for ext, fmt in sorted(data_exts.items()):
        print(f"  {ext:8} - {fmt}")
    
    print("\nDocument files:")
    doc_exts = {
        '.md': 'Markdown',
        '.txt': 'Plain Text',
        '.html': 'HTML',
        '.htm': 'HTML',
        '.css': 'CSS'
    }
    
    for ext, doc_type in sorted(doc_exts.items()):
        print(f"  {ext:8} - {doc_type}")

def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    if args is None:
        args = sys.argv[1:]
    
    # Handle version flag separately
    if "--version" in args or "-v" in args:
        from . import __version__
        print(f"Code Analysis Tool v{__version__}")
        return 0
    
    try:
        parsed_args = parse_args(args)
        
        if parsed_args.version:
            from . import __version__
            print(f"Code Analysis Tool v{__version__}")
            return 0
            
        if parsed_args.list_extensions:
            list_supported_extensions()
            return 0
            
        path = Path(parsed_args.path).resolve()
        
        if not path.exists():
            print(f"Error: Path '{path}' does not exist", file=sys.stderr)
            return 1
            
        print(f"Analyzing files in {path}...")
        
        if path.is_file():
            results = {str(path): analyze_code(path, model=parsed_args.model)}
        else:
            results = analyze_code(
                path, 
                model=parsed_args.model,
                exclude_dirs=parsed_args.exclude,
                file_extensions=parsed_args.extensions
            )
        
        if not results:
            print("No supported files found to analyze.")
            if parsed_args.extensions:
                print(f"No files with extensions: {', '.join(parsed_args.extensions)}")
            else:
                print("No supported file types found in the directory.")
            return 0
            
        print_analysis(
            results,
            output_format=parsed_args.format,
            output_file=parsed_args.output
        )
        
        return 0
        
    except KeyboardInterrupt:
        print("\nAnalysis cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
