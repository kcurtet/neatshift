"""
File organization service - Single Responsibility Principle.
Coordinates file organization workflow (scanning, planning, executing).
Depends on abstractions (DIP) - uses FileCategorizer protocol.
"""
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Protocol
import threading

from config.settings import AppSettings
from domain.categorizer import FileCategorizer
from domain.file_item import FileItem, FileStatus
from services.file_service import FileService
from services.performance_optimizer import PerformanceOptimizer

# Use Windows-optimized service on Windows, fallback otherwise
if sys.platform == 'win32':
    try:
        from services.windows_file_service import WindowsFileService
        FileServiceImpl = WindowsFileService
    except ImportError:
        FileServiceImpl = FileService
else:
    FileServiceImpl = FileService

# Configure logging
logger = logging.getLogger(__name__)


class ProgressCallback(Protocol):
    """
    Progress callback protocol for file operations.
    
    Provides better type safety and documentation than Callable.
    
    Args:
        idx: Index of current file being processed
        item: FileItem being processed
        completed: Number of files completed so far
        total: Total number of files to process
    """
    
    def __call__(self, idx: int, item: FileItem, completed: int, total: int) -> None:
        """Called after each file is processed."""
        ...


class OrganizationService:
    """
    High-level service for organizing files.
    Single Responsibility: Coordinate the organization workflow.
    Dependency Inversion: Depends on FileCategorizer abstraction, not concrete implementation.
    """
    
    def __init__(self, categorizer: FileCategorizer):
        """
        Initialize with a categorizer strategy.
        
        Args:
            categorizer: Strategy for categorizing files (follows DIP)
        """
        self.categorizer = categorizer
        self.file_service = FileServiceImpl()
        logger.info(f"Using file service: {FileServiceImpl.__name__}")
    
    def scan_and_plan(self, source: Path, dest: Path, skip_hidden: bool = True) -> list[FileItem]:
        """
        Scan source directory and build organization plan.
        
        Args:
            source: Source directory to scan
            dest: Destination base directory
            skip_hidden: Whether to skip hidden files/directories
            
        Returns:
            List of FileItem objects representing the organization plan
        """
        plan: list[FileItem] = []
        
        for root, dirs, files in os.walk(source):
            # Skip hidden directories
            if skip_hidden:
                dirs[:] = [d for d in dirs if not d.startswith(AppSettings.HIDDEN_PREFIX)]
            
            for filename in files:
                # Skip hidden files
                if skip_hidden and filename.startswith(AppSettings.HIDDEN_PREFIX):
                    continue
                
                src_path = Path(root) / filename
                
                try:
                    # Categorize file using injected strategy
                    result = self.categorizer.categorize(src_path)
                    
                    # Handle both old-style (FileCategory) and new-style (tuple) results
                    if isinstance(result, tuple):
                        category, organize_by_date = result
                    else:
                        # Backward compatibility with DefaultFileCategorizer
                        category = result.value
                        organize_by_date = True
                    
                    # Build destination path
                    if organize_by_date:
                        date_folder = self.file_service.get_date_folder(src_path)
                        dst_path = dest / category / date_folder / filename
                    else:
                        date_folder = ""
                        dst_path = dest / category / filename
                    
                    plan.append(FileItem(
                        src=src_path,
                        dst=dst_path,
                        category=category,
                        date=date_folder,
                        filename=filename,
                        status=FileStatus.PENDING,
                    ))
                except Exception as ex:
                    # Skip files that can't be processed
                    logger.debug(f"Skipping {src_path}: {ex}")
        
        return plan
    
    def execute_plan(
        self,
        plan: list[FileItem],
        progress_callback: ProgressCallback | None = None,
        max_workers: int | None = None,
    ) -> tuple[int, int]:
        """
        Execute the organization plan by moving files in parallel.
        
        Args:
            plan: List of FileItem objects to process
            progress_callback: Optional callback for progress updates
            max_workers: Number of worker threads (default: auto-calculated based on operations)
            
        Returns:
            Tuple of (successful_count, error_count)
        """
        if not plan:
            return 0, 0
        
        # Auto-calculate optimal workers if not specified
        if max_workers is None:
            # Check if operations are cross-drive or network
            is_network = any(
                PerformanceOptimizer.is_network_path(item.src) or
                PerformanceOptimizer.is_network_path(item.dst)
                for item in plan[:10]  # Sample first 10 files
            )
            
            # Check if majority are cross-drive operations
            _, is_cross_drive = PerformanceOptimizer.estimate_cross_drive_operations(plan)
            
            max_workers = PerformanceOptimizer.calculate_optimal_workers(
                file_count=len(plan),
                is_cross_drive=is_cross_drive,
                is_network=is_network,
            )
        
        total = len(plan)
        completed = 0
        lock = threading.Lock()
        start_time = time.time()
        
        logger.info(f"Starting file organization: {total} files with {max_workers} workers")
        
        def move_single_file(idx: int, item: FileItem) -> tuple[int, FileItem]:
            """Move a single file and update its status."""
            try:
                actual_dst = self.file_service.move_file(item.src, item.dst)
                item.mark_success(actual_dst)
                logger.debug(f"Successfully moved: {item.src} → {actual_dst}")
            except Exception as ex:
                item.mark_error()
                logger.error(f"Error moving {item.src}: {ex}", exc_info=True)
            return idx, item
        
        # Execute moves in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(move_single_file, idx, item): idx
                for idx, item in enumerate(plan)
            }
            
            for future in as_completed(futures):
                idx, item = future.result()
                
                with lock:
                    completed += 1
                    count = completed
                
                # Call progress callback if provided
                if progress_callback:
                    progress_callback(idx, item, count, total)
        
        # Count results
        successful = sum(1 for item in plan if item.status == FileStatus.OK)
        errors = sum(1 for item in plan if item.status == FileStatus.ERROR)
        
        # Log metrics
        duration = time.time() - start_time
        files_per_sec = successful / duration if duration > 0 else 0
        logger.info(
            f"Organization complete: {successful} successful, {errors} errors "
            f"in {duration:.2f}s ({files_per_sec:.1f} files/sec)"
        )
        
        return successful, errors
