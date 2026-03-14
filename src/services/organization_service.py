"""
File organization service - Single Responsibility Principle.
Coordinates file organization workflow (scanning, planning, executing).
Depends on abstractions (DIP) - uses FileCategorizer protocol.
"""
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Protocol
import threading

from ..config.settings import AppSettings
from ..domain.categorizer import FileCategorizer
from ..domain.file_item import FileItem, FileStatus
from .file_service import FileService

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
        self.file_service = FileService()
    
    def scan_and_plan(self, source: Path, dest: Path) -> list[FileItem]:
        """
        Scan source directory and build organization plan.
        
        Args:
            source: Source directory to scan
            dest: Destination base directory
            
        Returns:
            List of FileItem objects representing the organization plan
        """
        plan: list[FileItem] = []
        
        for root, dirs, files in os.walk(source):
            # Skip hidden directories
            if AppSettings.SKIP_HIDDEN_FILES:
                dirs[:] = [d for d in dirs if not d.startswith(AppSettings.HIDDEN_PREFIX)]
            
            for filename in files:
                # Skip hidden files
                if AppSettings.SKIP_HIDDEN_FILES and filename.startswith(AppSettings.HIDDEN_PREFIX):
                    continue
                
                src_path = Path(root) / filename
                
                try:
                    # Categorize file using injected strategy
                    category = self.categorizer.categorize(src_path)
                    date_folder = self.file_service.get_date_folder(src_path)
                    dst_path = dest / category.value / date_folder / filename
                    
                    plan.append(FileItem(
                        src=src_path,
                        dst=dst_path,
                        category=category.value,
                        date=date_folder,
                        filename=filename,
                        status=FileStatus.PENDING,
                    ))
                except Exception:
                    # Skip files that can't be processed
                    pass
        
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
            max_workers: Number of worker threads (default: from AppSettings)
            
        Returns:
            Tuple of (successful_count, error_count)
        """
        if not plan:
            return 0, 0
        
        if max_workers is None:
            max_workers = AppSettings.get_max_workers()
        
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
