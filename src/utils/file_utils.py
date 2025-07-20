"""Utility functions for file operations."""
import logging
import shutil
from pathlib import Path
from typing import List, Optional, Union, Generator, Tuple

logger = logging.getLogger(__name__)


def ensure_directory_exists(directory: Union[str, Path]) -> Path:
    """Ensure a directory exists, create it if it doesn't.
    
    Args:
        directory: Path to the directory
        
    Returns:
        Path: The path to the directory
    """
    path = Path(directory).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def find_files_by_extension(
    directory: Union[str, Path], 
    extensions: Union[str, List[str]],
    recursive: bool = True
) -> List[Path]:
    """Find files by extension in a directory.
    
    Args:
        directory: Directory to search in
        extensions: File extension(s) to search for
        recursive: Whether to search recursively
        
    Returns:
        List of matching file paths
    """
    if isinstance(extensions, str):
        extensions = [extensions]
    
    directory = Path(directory).resolve()
    if not directory.exists():
        logger.warning(f"Directory does not exist: {directory}")
        return []
    
    pattern = "**/*" if recursive else "*"
    files = []
    
    for ext in extensions:
        ext = ext.lstrip('.')
        files.extend(directory.glob(f"{pattern}.{ext}"))
    
    return sorted(files)


def read_file_safely(file_path: Union[str, Path]) -> Optional[str]:
    """Read a file safely with error handling.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File contents as string, or None if an error occurs
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None


def write_file_safely(
    file_path: Union[str, Path], 
    content: str,
    mode: str = 'w',
    backup: bool = True
) -> bool:
    """Write to a file safely with error handling and optional backup.
    
    Args:
        file_path: Path to the file to write
        content: Content to write
        mode: File open mode ('w' for write, 'a' for append)
        backup: Whether to create a backup if the file exists
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        file_path = Path(file_path).resolve()
        
        # Create backup if file exists and backup is True
        if file_path.exists() and backup:
            backup_path = file_path.with_suffix(f"{file_path.suffix}.bak")
            shutil.copy2(file_path, backup_path)
        
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(content)
            
        return True
    except Exception as e:
        logger.error(f"Error writing to file {file_path}: {e}")
        return False


def chunk_file(
    file_path: Union[str, Path], 
    chunk_size: int = 1024 * 1024  # 1MB chunks
) -> Generator[Tuple[bytes, int, int], None, None]:
    """Read a file in chunks.
    
    Args:
        file_path: Path to the file
        chunk_size: Size of each chunk in bytes
        
    Yields:
        Tuple of (chunk_data, chunk_number, total_chunks)
    """
    file_path = Path(file_path)
    total_size = file_path.stat().st_size
    total_chunks = (total_size + chunk_size - 1) // chunk_size
    
    with open(file_path, 'rb') as f:
        for i in range(total_chunks):
            yield f.read(chunk_size), i + 1, total_chunks
