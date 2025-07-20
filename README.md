# Python Code Explainer with Llama

A Streamlit-based web application that analyzes Python code and generates non-technical explanations using the Llama language model. This tool is perfect for educators, documentation writers, and developers who want to understand or explain complex code in simple terms.

![Python Code Explainer](https://img.shields.io/badge/python-3.8%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🔍 Automatic extraction of functions and classes from Python code
- 📝 Detailed code analysis including arguments, return values, and docstrings
- 🤖 AI-powered non-technical explanations using Llama model
- 📊 Interactive web interface with expandable code sections
- 📥 Export analysis as a well-formatted Word document
- 🚀 Easy to use with just a few clicks

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

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure you have Ollama installed and running:
   ```bash
   # Install Ollama (if not already installed)
   # Visit https://ollama.ai for installation instructions
   
   # Start Ollama server
   ollama serve
   
   # Pull the Llama model (in a separate terminal)
   ollama pull llama2
   ```

### Usage

1. Start the Streamlit application:
   ```bash
   streamlit run main.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Upload a Python file using the file uploader

4. View the code analysis and click "Generate Non-Technical Report with Llama" to get an AI-powered explanation

5. Download the analysis as a Word document for future reference

## 🛠️ How It Works

1. **Code Analysis**: The application parses the uploaded Python file and extracts:
   - Function and class definitions
   - Method signatures and arguments
   - Docstrings and comments
   - Return value indicators

2. **AI Explanation**: The extracted information is sent to the Llama model to generate a non-technical explanation of the code's functionality.

3. **Interactive UI**: The web interface allows you to:
   - Navigate through code elements with expandable sections
   - View detailed information about each function/class
   - Get AI-generated explanations in plain English
   - Export the complete analysis as a Word document

## 📦 Dependencies

- `streamlit` - For the web interface
- `ollama` - For interacting with the Llama model
- `python-docx` - For generating Word documents
- `ast` - For Python code parsing (standard library)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤖 Automated Documentation with GitHub Actions

This repository includes a GitHub Actions workflow that automatically generates documentation whenever you push code changes. Here's how it works:

1. **Automatic Trigger**: The workflow runs on every push to the `main` branch that includes changes to Python files.

2. **Documentation Generation**:
   - The workflow checks out your code
   - Sets up Python and installs dependencies
   - Runs the documentation generator on all Python files
   - Saves the output as a Word document in the `docs` directory

3. **Artifact Storage**: The generated documentation is available as a downloadable artifact in the GitHub Actions run.

4. **Auto-commit**: The workflow will automatically commit and push the updated documentation back to the repository.

### Viewing Documentation

1. Go to the "Actions" tab in your GitHub repository
2. Click on the latest workflow run
3. Download the "code-documentation" artifact to get the Word document

### Manual Trigger

You can also manually trigger the documentation generation:
1. Go to the "Actions" tab
2. Select "Generate Documentation" workflow
3. Click "Run workflow"

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
