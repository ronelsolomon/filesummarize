from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="code-explainer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for analyzing and explaining Python code using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code-explainer",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.24.0",
        "ollama>=0.1.5",
        "python-docx>=0.8.11",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
    },
    entry_points={
        "console_scripts": [
            "code-explainer=code_explainer.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
