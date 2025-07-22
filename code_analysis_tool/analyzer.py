"""Core analysis functionality for the code analysis tool."""
import ast
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

import ollama

def detect_file_type(file_path: Union[str, Path]) -> str:
    """Detect the type of file based on its extension."""
    path = Path(file_path)
    ext = path.suffix.lower()
    
    # Common code file extensions
    code_extensions = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.c': 'c',
        '.cpp': 'cpp',
        '.h': 'cpp',
        '.hpp': 'cpp',
        '.cs': 'csharp',
        '.go': 'go',
        '.rs': 'rust',
        '.rb': 'ruby',
        '.php': 'php',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.sh': 'shell',
        '.pl': 'perl',
        '.r': 'r',
        '.m': 'matlab',
        '.jl': 'julia',
    }
    
    # Data file extensions
    data_extensions = {
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.xml': 'xml',
        '.csv': 'csv',
        '.toml': 'toml',
        '.ini': 'ini',
        '.cfg': 'ini',
    }
    
    # Document extensions
    doc_extensions = {
        '.md': 'markdown',
        '.txt': 'text',
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
    }
    
    if ext in code_extensions:
        return 'code', code_extensions[ext]
    elif ext in data_extensions:
        return 'data', data_extensions[ext]
    elif ext in doc_extensions:
        return 'document', doc_extensions[ext]
    else:
        return 'unknown', ext[1:] if ext else 'text'

class CodeAnalyzer:
    """Analyzes Python code and provides explanations using AI."""
    
    def __init__(self, model: str = "llama3"):
        """Initialize the code analyzer.
        
        Args:
            model: The Ollama model to use for analysis.
        """
        self.model = model
        self.client = ollama.Client()
    
    def analyze_file(self, file_path: Union[str, Path]) -> Dict:
        """Analyze a single file.
        
        Args:
            file_path: Path to the file to analyze.
            
        Returns:
            Dict containing analysis results.
        """
        file_path = Path(file_path)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        file_type, sub_type = detect_file_type(file_path)
        
        if file_type == 'code':
            if sub_type == 'python':
                elements = self._extract_python_elements(content)
            else:
                elements = self._extract_generic_code_elements(content, sub_type)
        elif file_type == 'data':
            elements = self._extract_data_elements(content, sub_type)
        else:
            elements = self._extract_text_elements(content, file_type)
        
        analysis = self._analyze_elements(elements, str(file_path), file_type, sub_type)
        return analysis
    
    def analyze_directory(self, directory: Union[str, Path], 
                         exclude_dirs: Optional[List[str]] = None,
                         file_extensions: Optional[List[str]] = None) -> Dict:
        """Analyze all files in a directory.
        
        Args:
            directory: Path to the directory to analyze.
            exclude_dirs: List of directory names to exclude.
            file_extensions: List of file extensions to include (without leading .).
                            If None, includes all supported file types.
                            
        Returns:
            Dict containing analysis results for all files.
        """
        directory = Path(directory)
        if not directory.is_dir():
            raise ValueError(f"{directory} is not a valid directory")
            
        exclude_dirs = exclude_dirs or ['__pycache__', '.git', '.github', 'venv', 'env', 'node_modules']
        results = {}
        
        # Default supported extensions if none provided
        if file_extensions is None:
            file_extensions = [
                # Code files
                'py', 'js', 'jsx', 'ts', 'tsx', 'java', 'c', 'cpp', 'h', 'hpp',
                'cs', 'go', 'rs', 'rb', 'php', 'swift', 'kt', 'scala', 'sh', 'pl',
                'r', 'm', 'jl',
                # Data files
                'json', 'yaml', 'yml', 'xml', 'csv', 'toml', 'ini', 'cfg',
                # Document files
                'md', 'txt', 'html', 'htm', 'css'
            ]
        
        # Convert to set for faster lookups
        extensions = {f'.{ext.lstrip(".").lower()}' for ext in file_extensions}
        
        for file_path in directory.rglob('*'):
            # Skip directories and files in excluded directories
            if not file_path.is_file():
                continue
                
            if any(part in exclude_dirs for part in file_path.parts):
                continue
                
            # Check file extension
            if file_path.suffix.lower() not in extensions:
                continue
                
            try:
                results[str(file_path)] = self.analyze_file(file_path)
            except Exception as e:
                print(f"Error analyzing {file_path}: {str(e)}")
                continue
                
        return results
    
    def _extract_python_elements(self, code: str) -> List[Dict]:
        """Extract Python code elements (functions, classes) from source code."""
        try:
            tree = ast.parse(code)
            elements = []
            
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                    element_type = node.__class__.__name__.replace('Def', '')
                    doc = ast.get_docstring(node) or ""
                    src = ast.get_source_segment(code, node) or ""
                    
                    elements.append({
                        'type': element_type,
                        'name': node.name,
                        'docstring': doc,
                        'source': src,
                        'start_line': getattr(node, 'lineno', 0),
                        'end_line': getattr(node, 'end_lineno', 0),
                        'language': 'python'
                    })
                    
            return elements
        except Exception as e:
            print(f"Error parsing Python code: {str(e)}")
            return [{
                'type': 'File',
                'name': 'content',
                'docstring': 'Error parsing Python file',
                'source': code[:1000] + ('...' if len(code) > 1000 else ''),
                'language': 'python',
                'error': str(e)
            }]
    
    def _extract_generic_code_elements(self, code: str, language: str) -> List[Dict]:
        """Extract elements from generic code files using simple heuristics."""
        elements = []
        lines = code.split('\n')
        current_element = None
        
        # Common patterns for different languages
        patterns = {
            'javascript': r'(?:function|class|const|let|var)\s+([a-zA-Z0-9_$]+)',
            'typescript': r'(?:function|class|interface|type|enum|const|let|var)\s+([a-zA-Z0-9_$]+)',
            'java': r'(?:public|private|protected|static|final|native|synchronized|abstract|transient|class|interface|enum)\s+([a-zA-Z0-9_$<>, ]+?)[\s<{]',
            'c': r'(?:#define|typedef|struct|union|enum|void|int|char|float|double)\s+([a-zA-Z0-9_]+)',
            'cpp': r'(?:class|struct|union|enum|namespace|template|using)\s+([a-zA-Z0-9_:]+)',
            'csharp': r'(?:class|interface|struct|enum|delegate|namespace|using)\s+([a-zA-Z0-9_.]+)',
            'go': r'func\s+(\([^)]+\)\s+)?([a-zA-Z0-9_]+)',
            'rust': r'(?:fn|struct|enum|trait|impl|mod)\s+([a-zA-Z0-9_]+)',
            'ruby': r'(?:def|class|module)\s+([a-zA-Z0-9_]+[?!]?)',
            'php': r'(?:function|class|interface|trait|namespace)\s+([a-zA-Z0-9_]+)',
            'swift': r'(?:func|class|struct|enum|protocol|extension|typealias)\s+([a-zA-Z0-9_]+)',
            'kotlin': r'(?:fun|class|interface|object|typealias|val|var)\s+([a-zA-Z0-9_]+)',
            'scala': r'(?:def|class|trait|object|type|val|var)\s+([a-zA-Z0-9_]+)',
            'shell': r'(?:function\s+)?([a-zA-Z0-9_]+)\s*\(\s*\)',
            'perl': r'sub\s+([a-zA-Z0-9_]+)',
            'r': r'([a-zA-Z0-9_.]+)\s*<\-\s*function',
            'matlab': r'function\s+(?:\[.*\]\s*=\s*)?([a-zA-Z0-9_]+)',
            'julia': r'(?:function|struct|mutable\s+struct|abstract\s+type|primitive\s+type)\s+([a-zA-Z0-9_!]+)'
        }
        
        pattern = patterns.get(language, r'\b(function|class|def|fn|fun|sub|proc)\s+([a-zA-Z0-9_]+)')
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith(('//', '/*', '*', '--', '#', '--[', '--[[')):
                continue
                
            match = re.search(pattern, line)
            if match:
                if current_element:
                    elements.append(current_element)
                
                name = match.group(1) if len(match.groups()) == 1 else match.group(2)
                current_element = {
                    'type': 'Function' if 'function' in line.lower() or 'def ' in line.lower() or 'fn ' in line.lower() else 'Class',
                    'name': name.strip(),
                    'docstring': '',
                    'source': line,
                    'start_line': i,
                    'end_line': i,
                    'language': language
                }
            elif current_element:
                current_element['source'] += '\n' + line
                current_element['end_line'] = i
        
        if current_element:
            elements.append(current_element)
        
        if not elements:
            elements.append({
                'type': 'File',
                'name': 'content',
                'docstring': 'No structured elements found',
                'source': code[:1000] + ('...' if len(code) > 1000 else ''),
                'language': language
            })
            
        return elements
    
    def _extract_data_elements(self, content: str, data_type: str) -> List[Dict]:
        """Extract elements from data files (JSON, YAML, etc.)."""
        try:
            if data_type == 'json':
                data = json.loads(content)
                return [{
                    'type': 'Data',
                    'name': 'root',
                    'docstring': 'JSON data',
                    'source': json.dumps(data, indent=2)[:1000],
                    'language': 'json'
                }]
            elif data_type in ('yaml', 'yml'):
                data = yaml.safe_load(content)
                return [{
                    'type': 'Data',
                    'name': 'root',
                    'docstring': 'YAML data',
                    'source': yaml.dump(data, default_flow_style=False)[:1000],
                    'language': 'yaml'
                }]
            elif data_type == 'xml':
                # Simple XML parsing - could be enhanced with proper XML parsing
                return [{
                    'type': 'Data',
                    'name': 'xml_content',
                    'docstring': 'XML data',
                    'source': content[:1000] + ('...' if len(content) > 1000 else ''),
                    'language': 'xml'
                }]
            elif data_type == 'csv':
                # Simple CSV parsing - could be enhanced with proper CSV parsing
                return [{
                    'type': 'Data',
                    'name': 'csv_content',
                    'docstring': 'CSV data',
                    'source': content[:1000] + ('...' if len(content) > 1000 else ''),
                    'language': 'csv'
                }]
            else:
                return self._extract_text_elements(content, 'data')
        except Exception as e:
            return [{
                'type': 'Data',
                'name': 'content',
                'docstring': f'Error parsing {data_type} data: {str(e)}',
                'source': content[:1000] + ('...' if len(content) > 1000 else ''),
                'language': data_type,
                'error': str(e)
            }]
    
    def _extract_text_elements(self, content: str, content_type: str) -> List[Dict]:
        """Extract elements from plain text or document files."""
        if content_type == 'markdown':
            # Simple markdown section extraction
            sections = re.split(r'\n(#+\s+.*?)\n', content, flags=re.MULTILINE)
            elements = []
            
            for i in range(1, len(sections), 2):
                if i < len(sections):
                    elements.append({
                        'type': 'Section',
                        'name': sections[i].strip('# ').strip(),
                        'docstring': '',
                        'source': sections[i] + ('\n' + sections[i+1] if i+1 < len(sections) else ''),
                        'language': 'markdown'
                    })
            
            if not elements:
                elements = [{
                    'type': 'Document',
                    'name': 'content',
                    'docstring': 'Markdown content',
                    'source': content[:1000] + ('...' if len(content) > 1000 else ''),
                    'language': 'markdown'
                }]
                
            return elements
        else:
            # For plain text, just return the content
            return [{
                'type': 'Content',
                'name': 'content',
                'docstring': f'{content_type.capitalize()} content',
                'source': content[:1000] + ('...' if len(content) > 1000 else ''),
                'language': content_type
            }]
    
    def _analyze_elements(self, elements: List[Dict], file_path: str, 
                         file_type: str, sub_type: str) -> Dict:
        """Analyze elements using the AI model."""
        if not elements:
            return {}
        
        # Customize prompt based on file type
        if file_type == 'code':
            prompt = f"""Analyze the following {sub_type} code from {file_path}. """
            prompt += "For each element, provide a brief explanation of its purpose and functionality.\n\n"
        elif file_type == 'data':
            prompt = f"""Analyze the following {sub_type.upper()} data from {file_path}. """
            prompt += "Provide a summary of the data structure and its contents.\n\n"
        else:  # document or other text
            prompt = f"""Analyze the following {sub_type} content from {file_path}. """
            prompt += "Provide a summary of the content.\n\n"
        
        # Add elements to the prompt
        for element in elements:
            element_type = element.get('type', 'Element')
            name = element.get('name', 'unnamed')
            
            prompt += f"{element_type} {name}:\n"
            
            if element.get('docstring'):
                prompt += f"Description: {element['docstring']}\n"
                
            if element.get('source'):
                prompt += f"Content:\n{element['source']}\n\n"
        
        # Get analysis from the model
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False
            )
            return {
                'analysis': response['response'],
                'elements': elements,
                'file_type': file_type,
                'sub_type': sub_type
            }
        except Exception as e:
            print(f"Error getting analysis from model: {str(e)}")
            return {
                'error': str(e),
                'elements': elements,
                'file_type': file_type,
                'sub_type': sub_type
            }

def analyze_code(path: Union[str, Path], 
                model: str = "llama3",
                exclude_dirs: Optional[List[str]] = None,
                file_extensions: Optional[List[str]] = None) -> Dict:
    """Convenience function to analyze code at the given path.
    
    Args:
        path: Path to a file or directory to analyze.
        model: The Ollama model to use for analysis.
        exclude_dirs: List of directory names to exclude when analyzing directories.
        file_extensions: List of file extensions to include (without leading .).
                       If None, includes all supported file types.
        
    Returns:
        Dict containing analysis results.
    """
    analyzer = CodeAnalyzer(model=model)
    path = Path(path)
    
    if path.is_file():
        return analyzer.analyze_file(path)
    elif path.is_dir():
        return analyzer.analyze_directory(
            path, 
            exclude_dirs=exclude_dirs,
            file_extensions=file_extensions
        )
    else:
        raise ValueError(f"Path {path} is not a valid file or directory")
