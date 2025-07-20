# Python Code Explainer with Llama

A powerful tool that analyzes Python code and generates comprehensive documentation and explanations using the Llama language model. Available both as a Streamlit web application and a command-line interface.

![Python Code Explainer](https://img.shields.io/badge/python-3.8%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🔍 Automatic extraction of functions, classes, and methods from Python code
- 📝 Detailed code analysis including arguments, return values, and docstrings
- 🤖 AI-powered non-technical explanations using Llama model
- 🖥️ Multiple interfaces: Web UI and Command Line
- 📥 Export analysis as well-formatted Word documents
- 🔄 GitHub Action for automated documentation generation
- 🧩 Modular architecture for easy extension

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Ollama server running locally (with Llama model installed)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/python-code-explainer.git
   cd python-code-explainer
   ```

2. Install the package in development mode:
   ```bash
   pip install -e .
   ```
   
   Or install the required packages directly:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Ollama:
   ```bash
   # Install Ollama (if not already installed)
   # Visit https://ollama.ai for installation instructions
   
   # Start Ollama server in one terminal
   ollama serve
   
   # In another terminal, pull the Llama model
   ollama pull llama2
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
4. Automatically commits and pushes generated documentation to the repository

### Workflow Triggers

- **Push to main branch**: Runs tests, performs analysis, and updates documentation
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

## 📧 Contact

For any questions or feedback, please open an issue on the GitHub repository.
