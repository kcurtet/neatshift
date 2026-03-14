"""
Application configuration - Single Responsibility Principle.
This module only handles configuration and constants.
"""
from enum import Enum
from typing import Final
import multiprocessing


class FileCategory(Enum):
    """File categories for organization."""
    IMAGES = "Imágenes"
    VIDEOS = "Vídeos"
    DOCUMENTS = "Documentos"
    MUSIC = "Música"
    CODE = "Código"
    ARCHIVES = "Comprimidos"
    OTHER = "Otros"


# Category to extensions mapping
CATEGORY_EXTENSIONS: Final[dict[FileCategory, list[str]]] = {
    FileCategory.IMAGES: [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
        ".webp", ".heic", ".raw", ".cr2", ".nef", ".arw",
    ],
    FileCategory.VIDEOS: [
        ".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv",
        ".m4v", ".3gp", ".webm", ".mpg", ".mpeg",
    ],
    FileCategory.DOCUMENTS: [
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        ".txt", ".odt", ".ods", ".odp", ".rtf", ".csv",
    ],
    FileCategory.MUSIC: [
        ".mp3", ".wav", ".flac", ".aac", ".ogg",
        ".wma", ".m4a", ".opus", ".aiff",
    ],
    FileCategory.CODE: [
        ".py", ".js", ".ts", ".html", ".css", ".java", ".cpp",
        ".c", ".h", ".cs", ".php", ".rb", ".go", ".rs",
        ".json", ".xml", ".yaml", ".yml", ".sh", ".bat", ".ps1",
    ],
    FileCategory.ARCHIVES: [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
    ],
}

# Reverse lookup: extension -> category
EXTENSION_TO_CATEGORY: Final[dict[str, FileCategory]] = {
    ext.lower(): category
    for category, extensions in CATEGORY_EXTENSIONS.items()
    for ext in extensions
}

# Spanish month names
MONTHS_ES: Final[list[str]] = [
    "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


class AppSettings:
    """Application runtime settings."""
    
    # Window dimensions
    WINDOW_WIDTH: Final[int] = 1100
    WINDOW_HEIGHT: Final[int] = 720
    MIN_WIDTH: Final[int] = 820
    MIN_HEIGHT: Final[int] = 540
    
    # Threading configuration
    MAX_WORKERS_MULTIPLIER: Final[int] = 4
    MAX_WORKERS_CAP: Final[int] = 16
    
    # UI update batching (deprecated - use get_ui_batch_size)
    UI_UPDATE_BATCH_SIZE: Final[int] = 5
    
    # File filtering
    SKIP_HIDDEN_FILES: Final[bool] = True
    HIDDEN_PREFIX: Final[str] = "."

    @classmethod
    def get_max_workers(cls) -> int:
        """Calculate optimal thread count for I/O-bound operations."""
        cpu_count = multiprocessing.cpu_count() or 4
        return min(cls.MAX_WORKERS_CAP, cpu_count * cls.MAX_WORKERS_MULTIPLIER)
    
    @classmethod
    def get_ui_batch_size(cls, total_files: int) -> int:
        """
        Calculate optimal UI update batch size based on total file count.
        
        Fewer files → more frequent updates (better responsiveness)
        More files → less frequent updates (better performance)
        
        Args:
            total_files: Total number of files to process
            
        Returns:
            Optimal batch size for UI updates
        """
        if total_files < 100:
            return 1  # Update on every file
        elif total_files < 1000:
            return 5
        elif total_files < 10000:
            return 50
        else:
            return 100  # Large operations: update every 100 files
