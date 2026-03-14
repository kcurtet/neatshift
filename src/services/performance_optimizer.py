"""
Performance optimizer for Windows file operations.
Based on robocopy best practices and Python threading benchmarks.
"""
import logging
import multiprocessing
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


class PerformanceOptimizer:
    """
    Calculates optimal threading configuration for file operations.
    
    Based on robocopy research:
    - robocopy /MT:8 is default (8 threads)
    - robocopy /MT:16 is recommended for network/large operations
    - More threads ≠ always better (diminishing returns + overhead)
    
    For Python ThreadPoolExecutor with I/O operations:
    - I/O-bound: can use more threads than CPU cores
    - Sweet spot: 2-4x CPU cores for local disk
    - Sweet spot: 8-16 threads for network/mixed drives
    """
    
    # Thread count limits
    MIN_WORKERS = 2
    MAX_WORKERS_LOCAL = 16      # Max for same-drive operations
    MAX_WORKERS_NETWORK = 8     # Max for network/cross-drive operations
    
    # Multiplier for CPU-based calculation
    MULTIPLIER_LOCAL = 4        # Local I/O can handle more parallelism
    MULTIPLIER_NETWORK = 2      # Network I/O benefits from less contention
    
    @staticmethod
    def get_cpu_count() -> int:
        """Get CPU core count with fallback."""
        try:
            return multiprocessing.cpu_count() or 4
        except Exception:
            logger.warning("Could not determine CPU count, defaulting to 4")
            return 4
    
    @staticmethod
    def calculate_optimal_workers(
        file_count: int,
        is_cross_drive: bool = False,
        is_network: bool = False,
    ) -> int:
        """
        Calculate optimal thread count for file operations.
        
        Factors considered:
        1. CPU core count
        2. Operation type (same drive vs cross-drive vs network)
        3. File count (fewer files = fewer threads needed)
        
        Args:
            file_count: Number of files to process
            is_cross_drive: True if moving between different drives
            is_network: True if source or destination is network path
            
        Returns:
            Optimal worker thread count
        """
        cpu_count = PerformanceOptimizer.get_cpu_count()
        
        # For very few files, don't over-parallelize
        if file_count < 10:
            return min(file_count, PerformanceOptimizer.MIN_WORKERS)
        
        # Calculate base workers from CPU count
        if is_network or is_cross_drive:
            # Network/cross-drive: lower parallelism (I/O bottleneck)
            base_workers = cpu_count * PerformanceOptimizer.MULTIPLIER_NETWORK
            max_workers = PerformanceOptimizer.MAX_WORKERS_NETWORK
        else:
            # Same drive: higher parallelism possible
            base_workers = cpu_count * PerformanceOptimizer.MULTIPLIER_LOCAL
            max_workers = PerformanceOptimizer.MAX_WORKERS_LOCAL
        
        # Apply limits
        optimal = max(
            PerformanceOptimizer.MIN_WORKERS,
            min(base_workers, max_workers, file_count)
        )
        
        logger.info(
            f"Performance config: {optimal} workers "
            f"(CPU: {cpu_count}, Files: {file_count}, "
            f"Cross-drive: {is_cross_drive}, Network: {is_network})"
        )
        
        return optimal
    
    @staticmethod
    def is_network_path(path: Path) -> bool:
        """
        Check if path is a network location.
        
        Windows: Checks for UNC paths (\\\\server\\share)
        
        Args:
            path: Path to check
            
        Returns:
            True if network path, False otherwise
        """
        path_str = str(path.resolve())
        
        # Windows UNC paths
        if sys.platform == 'win32':
            return path_str.startswith('\\\\')
        
        # Linux/Mac: check if mounted network share
        # (simplified check - could be enhanced)
        return False
    
    @staticmethod
    def estimate_cross_drive_operations(plan: list) -> tuple[int, bool]:
        """
        Estimate how many operations are cross-drive.
        
        Args:
            plan: List of FileItem objects with src and dst paths
            
        Returns:
            Tuple of (cross_drive_count, is_majority_cross_drive)
        """
        if not plan:
            return 0, False
        
        cross_drive_count = 0
        
        for item in plan:
            src_drive = item.src.drive if hasattr(item.src, 'drive') else ""
            dst_drive = item.dst.drive if hasattr(item.dst, 'drive') else ""
            
            if src_drive and dst_drive and src_drive.lower() != dst_drive.lower():
                cross_drive_count += 1
        
        is_majority = cross_drive_count > (len(plan) / 2)
        
        logger.debug(
            f"Cross-drive analysis: {cross_drive_count}/{len(plan)} "
            f"({'majority' if is_majority else 'minority'})"
        )
        
        return cross_drive_count, is_majority


class OptimizationPresets:
    """
    Pre-configured optimization presets for common scenarios.
    """
    
    @staticmethod
    def for_local_backup(file_count: int) -> int:
        """Optimize for backing up to external USB/local drive."""
        return PerformanceOptimizer.calculate_optimal_workers(
            file_count=file_count,
            is_cross_drive=True,
            is_network=False,
        )
    
    @staticmethod
    def for_network_backup(file_count: int) -> int:
        """Optimize for backing up to network share."""
        return PerformanceOptimizer.calculate_optimal_workers(
            file_count=file_count,
            is_cross_drive=True,
            is_network=True,
        )
    
    @staticmethod
    def for_same_drive_organize(file_count: int) -> int:
        """Optimize for organizing files on same drive."""
        return PerformanceOptimizer.calculate_optimal_workers(
            file_count=file_count,
            is_cross_drive=False,
            is_network=False,
        )
