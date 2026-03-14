"""
Windows-optimized file operations service.
Leverages Python 3.12+ CopyFile2 optimizations for maximum performance.
"""
import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from config.settings import MONTHS_ES

logger = logging.getLogger(__name__)


class WindowsFileService:
    """
    Windows-optimized file service.
    
    Key optimizations:
    - Python 3.12+ uses Windows CopyFile2 API (kernel-level copy)
    - Same-drive moves use instant rename (atomic operation)
    - Cross-drive moves use optimized copy + delete
    - Large file detection with appropriate buffer handling
    """
    
    # File size threshold for "large file" handling (100 MB)
    LARGE_FILE_THRESHOLD = 100 * 1024 * 1024
    
    @staticmethod
    def is_windows() -> bool:
        """Check if running on Windows."""
        return sys.platform == 'win32'
    
    @staticmethod
    def validate_source_path(path: Path) -> None:
        """
        Validate source path before read operations.
        
        Args:
            path: Path to validate
            
        Raises:
            FileNotFoundError: If path does not exist
            PermissionError: If path is not readable
        """
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")
        
        if not os.access(path, os.R_OK):
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
        """
        parent = path.parent if path.is_file() or not path.exists() else path
        
        if parent.exists() and not os.access(parent, os.W_OK):
            raise PermissionError(f"No write access: {parent}")
        
        logger.debug(f"Validated destination path: {path}")
    
    @staticmethod
    def move_file(src: Path, dst: Path) -> Path:
        """
        Move file with Windows-specific optimizations.
        
        Strategy (optimized for Windows):
        1. Validate source and destination paths
        2. Check if same drive → use os.rename() (instant, atomic)
        3. Different drives → use shutil.copy2() + unlink()
           - Python 3.12+ automatically uses CopyFile2 API on Windows
           - CopyFile2 = kernel-level copy (no userspace buffer overhead)
        
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
        WindowsFileService.validate_source_path(src)
        
        # Ensure destination directory exists
        dst.parent.mkdir(parents=True, exist_ok=True)
        WindowsFileService.validate_dest_path(dst)
        
        # Handle duplicates by appending counter
        actual_dst = WindowsFileService._get_unique_path(dst)
        
        # Detect large files for logging
        file_size = src.stat().st_size
        is_large = file_size > WindowsFileService.LARGE_FILE_THRESHOLD
        
        if is_large:
            logger.debug(f"Large file detected: {src.name} ({file_size / (1024*1024):.1f} MB)")
        
        # Try atomic rename first (same filesystem/drive)
        try:
            os.rename(str(src), str(actual_dst))
            logger.debug(f"Moved (instant rename): {src} → {actual_dst}")
            return actual_dst
        except OSError as e:
            # Cross-device/drive: fall back to copy + delete
            # Python 3.12+ uses CopyFile2 API on Windows automatically
            logger.debug(f"Cross-drive move detected, using copy+delete: {e}")
            
            try:
                # shutil.copy2 preserves metadata and uses CopyFile2 on Windows
                shutil.copy2(str(src), str(actual_dst))
                src.unlink()
                logger.debug(f"Moved (copy+delete): {src} → {actual_dst}")
                return actual_dst
            except Exception as copy_error:
                # Clean up partial copy if it exists
                if actual_dst.exists():
                    try:
                        actual_dst.unlink()
                    except Exception:
                        pass
                raise copy_error
    
    @staticmethod
    def _get_unique_path(path: Path) -> Path:
        """
        Get unique path by appending counter if file exists.
        
        Example:
            document.pdf → document (1).pdf → document (2).pdf
        """
        if not path.exists():
            return path
        
        stem, suffix, parent = path.stem, path.suffix, path.parent
        counter = 1
        while path.exists():
            path = parent / f"{stem} ({counter}){suffix}"
            counter += 1
        
        logger.debug(f"Generated unique path: {path}")
        return path
    
    @staticmethod
    def get_date_folder(filepath: Path) -> str:
        """
        Get date-based folder name from file modification time.
        Format: YYYY/MM - MonthName (e.g., "2024/03 - Marzo")
        
        Args:
            filepath: Path to file
            
        Returns:
            Formatted date folder string
        """
        timestamp = filepath.stat().st_mtime
        dt = datetime.fromtimestamp(timestamp)
        month_name = MONTHS_ES[dt.month]
        return f"{dt.year}/{dt.month:02d} - {month_name}"
    
    @staticmethod
    def get_drive(path: Path) -> str:
        """
        Get drive letter from path (Windows-specific).
        
        Args:
            path: Path to extract drive from
            
        Returns:
            Drive letter (e.g., "C:") or empty string if not applicable
        """
        if WindowsFileService.is_windows():
            return os.path.splitdrive(str(path))[0]
        return ""
    
    @staticmethod
    def is_same_drive(src: Path, dst: Path) -> bool:
        """
        Check if source and destination are on the same drive.
        
        Same drive = can use instant rename instead of copy+delete.
        
        Args:
            src: Source path
            dst: Destination path
            
        Returns:
            True if same drive, False otherwise
        """
        if not WindowsFileService.is_windows():
            # On non-Windows, check if same device
            try:
                return src.stat().st_dev == dst.parent.stat().st_dev
            except Exception:
                return False
        
        src_drive = WindowsFileService.get_drive(src)
        dst_drive = WindowsFileService.get_drive(dst)
        return src_drive.lower() == dst_drive.lower()
