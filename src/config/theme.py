"""
UI Theme configuration - Single Responsibility Principle.
Handles all visual styling constants.
"""
from typing import Final
from .settings import FileCategory


class Theme:
    """Application visual theme."""
    
    # Colors
    BG: Final[str] = "#0f1117"
    SURFACE: Final[str] = "#1a1d27"
    CARD: Final[str] = "#22263a"
    ACCENT: Final[str] = "#6c8ef5"
    SUCCESS: Final[str] = "#34d399"
    DANGER: Final[str] = "#f87171"
    WARNING: Final[str] = "#fbbf24"
    TEXT: Final[str] = "#e2e8f0"
    SUBTEXT: Final[str] = "#94a3b8"
    
    @classmethod
    def get_category_icon(cls, category: FileCategory) -> str:
        """Get icon for a file category. Lazy import to avoid flet dependency in tests."""
        import flet as ft
        
        icons = {
            FileCategory.IMAGES: ft.Icons.IMAGE,
            FileCategory.VIDEOS: ft.Icons.VIDEO_FILE,
            FileCategory.DOCUMENTS: ft.Icons.DESCRIPTION,
            FileCategory.MUSIC: ft.Icons.AUDIO_FILE,
            FileCategory.CODE: ft.Icons.CODE,
            FileCategory.ARCHIVES: ft.Icons.FOLDER_ZIP,
            FileCategory.OTHER: ft.Icons.INSERT_DRIVE_FILE,
        }
        return icons.get(category, ft.Icons.INSERT_DRIVE_FILE)
