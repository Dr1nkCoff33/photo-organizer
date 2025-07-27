"""
File utility functions for photo organizer
"""

import os
import shutil
from pathlib import Path
from typing import List, Set, Optional
import logging

logger = logging.getLogger(__name__)

# Photo file extensions
RAW_EXTENSIONS = {
    '.ARW', '.CR2', '.NEF', '.RAF', '.ORF', '.RW2', 
    '.PEF', '.SRW', '.DNG', '.RAW'
}

IMAGE_EXTENSIONS = {
    '.JPG', '.JPEG', '.PNG', '.TIFF', '.TIF', '.BMP', '.GIF'
}

ALL_PHOTO_EXTENSIONS = RAW_EXTENSIONS | IMAGE_EXTENSIONS

def get_photo_files(directory: Path, extensions: Optional[Set[str]] = None) -> List[Path]:
    """
    Get all photo files from a directory
    
    Args:
        directory: Directory to search
        extensions: Set of file extensions to include (default: all photo extensions)
    
    Returns:
        List of photo file paths
    """
    if extensions is None:
        extensions = ALL_PHOTO_EXTENSIONS
    
    photo_files = []
    for ext in extensions:
        photo_files.extend(directory.rglob(f'*{ext}'))
        photo_files.extend(directory.rglob(f'*{ext.lower()}'))
    
    return sorted(photo_files)

def create_directory_structure(base_path: Path, structure: List[str]) -> None:
    """
    Create directory structure
    
    Args:
        base_path: Base directory path
        structure: List of subdirectory names
    """
    for subdir in structure:
        (base_path / subdir).mkdir(parents=True, exist_ok=True)

def safe_move_file(source: Path, destination: Path, overwrite: bool = False) -> bool:
    """
    Safely move a file with conflict resolution
    
    Args:
        source: Source file path
        destination: Destination file path
        overwrite: Whether to overwrite existing files
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if destination.exists() and not overwrite:
            # Generate unique filename
            counter = 1
            stem = destination.stem
            suffix = destination.suffix
            while destination.exists():
                destination = destination.parent / f"{stem}_{counter}{suffix}"
                counter += 1
        
        shutil.move(str(source), str(destination))
        logger.info(f"Moved {source} to {destination}")
        return True
    except Exception as e:
        logger.error(f"Failed to move {source} to {destination}: {e}")
        return False

def get_file_size_mb(filepath: Path) -> float:
    """
    Get file size in megabytes
    
    Args:
        filepath: Path to file
    
    Returns:
        File size in MB
    """
    return filepath.stat().st_size / (1024 * 1024)

def get_directory_size_mb(directory: Path) -> float:
    """
    Get total size of directory in megabytes
    
    Args:
        directory: Directory path
    
    Returns:
        Total size in MB
    """
    total_size = 0
    for filepath in directory.rglob('*'):
        if filepath.is_file():
            total_size += filepath.stat().st_size
    return total_size / (1024 * 1024) 