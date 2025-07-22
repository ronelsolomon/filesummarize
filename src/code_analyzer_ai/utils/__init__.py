"""Utility functions for the Python Code Explainer application."""

from .file_utils import (
    ensure_directory_exists,
    find_files_by_extension,
    read_file_safely,
    write_file_safely,
    chunk_file
)

from .llm_utils import (
    LLMClient,
    LLMResponse,
    get_llm_client
)

__all__ = [
    'ensure_directory_exists',
    'find_files_by_extension',
    'read_file_safely',
    'write_file_safely',
    'chunk_file',
    'LLMClient',
    'LLMResponse',
    'get_llm_client'
]
