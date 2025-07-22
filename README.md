# Code Analysis Tool with Llama

A powerful tool that analyzes code and text files, generating comprehensive documentation and explanations using the Llama language model. Available both as a command-line interface and as a Python library.

![Code Analysis Tool](https://img.shields.io/badge/python-3.8%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🔍 Supports multiple programming languages (Python, JavaScript, Java, C++, and more)
- 📊 Processes data files (JSON, YAML, XML, CSV) and documents (Markdown, HTML, plain text)
- 🤖 AI-powered code analysis and explanations using Llama model
- 🖥️ Command Line Interface with flexible options
- 📝 Detailed analysis including structure, elements, and relationships
- 🚀 Fast and efficient processing of large codebases
- 🧩 Extensible architecture for adding new file type support

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Ollama server running locally (with Llama model installed)

### Installation

1. Install the package using pip:
   ```bash
   pip install code-analysis-tool
   ```

2. Set up Ollama:
   ```bash
   # Install Ollama (if not already installed)
   # Visit https://ollama.ai for installation instructions
   
   # Start Ollama server (in a separate terminal)
   ollama serve
   
   # Pull the Llama model (if not already done)
   ollama pull llama3
   ```

### Basic Usage

```bash
# Analyze all supported files in the current directory
code-analyze

# Analyze specific file types only
code-analyze --extensions py js json

# Analyze a specific directory
code-analyze path/to/your/code

# List all supported file extensions
code-analyze --list-extensions

# Save output to a file
code-analyze --output analysis.txt

# Get help
code-analyze --help
```

## 📖 Usage

### Web Interface

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
   Or:
   ```bash
   python -m src.code_explainer.cli web
   ```

2. Open your web browser to `http://localhost:8501`

3. Upload a Python file and explore the analysis

### Command Line Interface

Analyze a Python file:
```bash
python -m src.code_explainer.cli analyze path/to/your/file.py
```

Generate documentation:
```bash
python -m src.code_explainer.cli document path/to/your/file.py --output docs/
```

### As a Python Library

```python
from code_analysis_tool import analyze_code, CodeAnalyzer

# Analyze a single file
results = analyze_code("example.py")
print(results['analysis'])

# Analyze a directory with specific file types
directory_results = analyze_code(
    "src/", 
    exclude_dirs=["tests", "venv"],
    file_extensions=["py", "js", "json"]
)

# Or use the CodeAnalyzer class directly for more control
analyzer = CodeAnalyzer(model="llama3")
results = analyzer.analyze_directory(
    "project/",
    exclude_dirs=["node_modules", ".git"],
    file_extensions=["py", "js", "ts", "json", "yaml"]
)

for file_path, analysis in results.items():
    print(f"\nFile: {file_path} ({analysis.get('file_type')}/{analysis.get('sub_type')})")
    print(analysis['analysis'])
    
    # Access individual elements if available
    for element in analysis.get('elements', [])[:3]:  # Show first 3 elements
        print(f"\nElement: {element.get('type')} {element.get('name')}")
        print(f"Lines: {element.get('start_line')}-{element.get('end_line')}")
```

## 🛠️ How It Works

1. **Code Analysis**: The tool parses Python files to extract:
   - Function and class definitions
   - Method signatures with arguments and return types
   - Docstrings and inline comments
   - Import statements and module-level documentation

2. **AI Integration**: The extracted information is processed by the Llama model to generate:
   - Clear, non-technical explanations
   - Usage examples
   - Documentation in multiple formats

3. **Output Generation**: Results can be:
   - Viewed in the web interface
   - Exported as Word documents
   - Generated automatically via GitHub Actions

## 📦 Project Structure

```
.
├── src/
│   ├── code_explainer/
│   │   ├── __init__.py
│   │   ├── cli.py          # Command line interface
│   │   ├── code_analyzer.py # Core code analysis logic
│   │   ├── document_generator.py # Document generation
│   │   └── llm_integration.py # Llama model integration
│   ├── action.py          # GitHub Action entry point
│   └── analyzer.py        # Core analysis functionality
├── .github/workflows/     # GitHub Actions workflows
├── app.py                 # Streamlit web app
├── main.py                # Legacy entry point
├── requirements.txt       # Python dependencies
└── setup.py               # Package configuration
```

## GitHub Actions

This project includes a GitHub Actions workflow (`.github/workflows/code_analysis.yml`) that:

1. Runs tests on push and pull requests
2. Performs code analysis using the Python Code Explainer
3. Generates documentation in Word format
## Supported File Types

### Code Files
- **Python** (.py)
- **JavaScript/TypeScript** (.js, .jsx, .ts, .tsx)
- **Java** (.java)
- **C/C++** (.c, .cpp, .h, .hpp)
- **C#** (.cs)
- **Go** (.go)
- **Rust** (.rs)
- **Ruby** (.rb)
- **PHP** (.php)
- **And more** (Shell, Perl, R, MATLAB, Julia, etc.)

### Data Files
- **JSON** (.json)
- **YAML** (.yaml, .yml)
- **XML** (.xml)
- **CSV** (.csv)
- **TOML** (.toml)
- **INI/Config** (.ini, .cfg)

### Document Files
- **Markdown** (.md)
- **HTML** (.html, .htm)
- **CSS** (.css)
- **Plain Text** (.txt)
- **Pull requests**: Runs tests and performs analysis (does not update documentation)
- **Manual trigger**: Can be manually triggered from the Actions tab

### Generated Documentation

When the workflow runs on the main branch, it will:

1. Generate a Word document (`docs/code_analysis_YYYYMMDD_HHMMSS.docx`)
2. Include a summary of all analyzed code elements
3. Provide detailed explanations of the code structure
4. Automatically commit and push the generated documentation

### Required Permissions

The workflow requires the following permissions:
- `contents: write` - To commit and push generated documentation
- `pull-requests: write` - To update pull request statuses
- `statuses: write` - To update commit statuses

These permissions are automatically provided by the default `GITHUB_TOKEN`. No additional configuration is needed for public repositories. For private repositories, ensure the workflow has the necessary permissions in your repository settings.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork and clone the repository
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .[dev]
   ```
3. Make your changes and run tests
4. Submit a pull request


# Code Explainer Extension

A powerful VS Code extension that helps you understand and document your code using AI. Generate detailed documentation, get plain English explanations, and improve code readability with just a few clicks.

## Features

- **AI-Powered Code Explanation**: Get detailed explanations of what your code does
- **Automatic Documentation**: Generate comprehensive documentation for your code
- **Multiple Formats**: Get documentation inline or in a separate Markdown file
- **Plain English Explanations**: Understand complex code in simple terms
- **Multi-language Support**: Works with various programming languages
- **Context-Aware**: Analyzes code context for more accurate explanations

## Installation

1. Install the extension from the [VS Code Marketplace](https://marketplace.visualstudio.com/)
2. Alternatively, install from VSIX:
   ```bash
   code --install-extension code-explainer-0.1.0.vsix

## 📧 Contact

For any questions or feedback, please open an issue on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).

## End-User License Agreement (EULA)

By installing or using this extension, you agree to the terms of the [End-User License Agreement](EULA.md).
