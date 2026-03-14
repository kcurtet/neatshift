"""
File operations service - Single Responsibility Principle.
Handles low-level file operations (move, copy, delete).
"""
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path

from config.settings import MONTHS_ES

# Configure logging
logger = logging.getLogger(__name__)


class FileService:
    """
    Service for file system operations.
    Single Responsibility: File I/O operations only.
    """
    
    @staticmethod
    def validate_source_path(path: Path) -> None:
        """
        Validate source path before read operations.

        Args:
            path: Path to validate

        Raises:
            FileNotFoundError: If path does not exist (including broken symlinks)
            PermissionError: If path is not readable
            ValueError: If path is not a file or directory
        """
        # Check if path exists or is a broken symlink
        # Use os.path.lexists() to detect broken symlinks
        if not os.path.lexists(str(path)):
            raise FileNotFoundError(f"Path does not exist: {path}")

        # For broken symlinks, check if we can read the link itself
        if path.is_symlink() and not path.exists():
            logger.warning(f"Broken symlink detected: {path}")
            # We can still access the symlink itself even if target doesn't exist

        if not os.access(str(path), os.R_OK):
            raise PermissionError(f"No read access: {path}")

        logger.debug(f"Validated source path: {path}")
    
    @staticmethod
    def validate_dest_path(path: Path) -> None:
        """
        Validate destination path before write operations.
        
        Args:
            path: Destination path to validate (file or parent directory)
            
        Raises:
            PermissionError: If path/parent is not writable
            ValueError: If parent directory doesn't exist and can't be created
        """
        # Check parent directory for write access
        parent = path.parent if path.is_file() or not path.exists() else path
        
        if parent.exists() and not os.access(parent, os.W_OK):
            raise PermissionError(f"No write access: {parent}")
        
        logger.debug(f"Validated destination path: {path}")
    
    @staticmethod
    def move_file(src: Path, dst: Path) -> Path:
        """
        Move file with automatic duplicate handling.
        Returns actual destination path (may differ if renamed).
        
        Strategy:
        1. Validate source and destination paths
        2. Try os.rename() first (atomic, instant on same filesystem)
        3. Fall back to shutil.copy2() + unlink() for cross-device moves
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            Actual destination path (may differ if file was renamed to avoid duplicates)
            
        Raises:
            FileNotFoundError: If source doesn't exist
            PermissionError: If insufficient permissions
        """
        # Validate paths
        FileService.validate_source_path(src)
        
        # Ensure destination directory exists
        dst.parent.mkdir(parents=True, exist_ok=True)
        FileService.validate_dest_path(dst)
        
        # Handle duplicates by appending counter
        actual_dst = FileService._get_unique_path(dst)
        
        # Try atomic rename first (same filesystem)
        try:
            os.rename(str(src), str(actual_dst))
            logger.debug(f"Moved (rename): {src} → {actual_dst}")
            return actual_dst
        except OSError:
            # Cross-device: fall back to copy + delete
            shutil.copy2(str(src), str(actual_dst))
            src.unlink()
            logger.debug(f"Moved (copy+delete): {src} → {actual_dst}")
            return actual_dst
    
    @staticmethod
    def _get_unique_path(path: Path) -> Path:
        """Get unique path by appending counter if file exists."""
        if not path.exists():
            return path
        
        stem, suffix, parent = path.stem, path.suffix, path.parent
        counter = 1
        while path.exists():
            path = parent / f"{stem} ({counter}){suffix}"
            counter += 1
        return path
    
    @staticmethod
    def get_date_folder(filepath: Path) -> str:
        """
        Get date-based folder name from file modification time.
        Format: YYYY/MM - MonthName (e.g., "2024/03 - Marzo")
        """
        timestamp = filepath.stat().st_mtime
        dt = datetime.fromtimestamp(timestamp)
        month_name = MONTHS_ES[dt.month]
        return f"{dt.year}/{dt.month:02d} - {month_name}"
