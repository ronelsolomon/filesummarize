from setuptools import setup, find_packages
import os

# Read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get package version
about = {}
with open(os.path.join(this_directory, 'code_analysis_tool', '__init__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name="code-analysis-tool",
    version=about['__version__'],
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for analyzing and explaining Python code using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code-analysis-tool",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "ollama>=0.1.5",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
            'twine>=4.0.0',
            'build>=0.10.0',
        ],
    },
    entry_points={
        "console_scripts": [
            "code-analyze=code_analysis_tool.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="code analysis documentation ai ollama",
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/code-analysis-tool/issues',
        'Source': 'https://github.com/yourusername/code-analysis-tool',
    },
)
