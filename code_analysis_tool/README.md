# Code Analysis Tool

A powerful command-line tool for analyzing Python codebases using AI to generate explanations and documentation.

## Features

- **AI-Powered Analysis**: Uses Ollama's language models to analyze and explain Python code
- **Flexible Input**: Works with single files or entire directories
- **Customizable**: Configure which directories to exclude from analysis
- **Multiple Output Formats**: Supports both human-readable and JSON output
- **Easy Integration**: Can be used as a Python library or command-line tool

## Installation

1. **Install the package**

   ```bash
   # Install from source
   git clone https://github.com/yourusername/code-analysis-tool.git
   cd code-analysis-tool
   pip install .
   
   # Or install directly from GitHub
   pip install git+https://github.com/yourusername/code-analysis-tool.git
   ```

2. **Set up Ollama**

   Make sure you have Ollama installed and running on your system:
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Start the Ollama server
   ollama serve
   
   # Pull the desired model (e.g., llama3)
   ollama pull llama3
   ```

## Usage

### Command Line Interface

```bash
# Analyze the current directory
code-analyze

# Analyze a specific file or directory
code-analyze path/to/your/code

# Use a different Ollama model
code-analyze --model codellama

# Save output to a file
code-analyze --output analysis.txt
code-analyze --output analysis.json --format json

# Show help
code-analyze --help
```

### As a Python Library

```python
from code_analysis_tool import analyze_code

# Analyze a single file
results = analyze_code("example.py")
print(results['analysis'])

# Analyze a directory
directory_results = analyze_code("src/", exclude_dirs=["tests", "venv"])
for file_path, analysis in directory_results.items():
    print(f"\nFile: {file_path}")
    print(analysis['analysis'])
```

## Configuration

### Environment Variables

- `OLLAMA_HOST`: URL of the Ollama server (default: `http://localhost:11434`)
- `OLLAMA_MODEL`: Default model to use (default: `llama3`)

### Excluding Directories

By default, the following directories are excluded from analysis:
- `__pycache__`
- `.git`
- `.github`
- `venv`
- `env`

You can customize this list using the `--exclude` option:

```bash
code-analyze --exclude tests build dist
```

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   pre-commit install
   ```

### Running Tests

```bash
pytest
```

### Building the Package

```bash
python -m build
```

## License

MIT

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Support

If you find this tool useful, please consider giving it a ⭐ on GitHub!
