"""
File categorization - Open/Closed Principle & Dependency Inversion.
Uses Protocol for extensibility without modification.
"""
from pathlib import Path
from typing import Protocol
from config.settings import FileCategory, EXTENSION_TO_CATEGORY


class FileCategorizer(Protocol):
    """
    Protocol for file categorization strategies.
    This follows the Open/Closed Principle - open for extension, closed for modification.
    New categorization strategies can be added without changing existing code.
    """
    
    def categorize(self, filepath: Path) -> FileCategory:
        """Categorize a file based on its properties."""
        ...


class DefaultFileCategorizer:
    """
    Default categorization strategy based on file extension.
    Implements FileCategorizer protocol.
    """
    
    def categorize(self, filepath: Path) -> FileCategory:
        """Categorize file by extension."""
        extension = filepath.suffix.lower()
        return EXTENSION_TO_CATEGORY.get(extension, FileCategory.OTHER)


# Example of extensibility (Open/Closed Principle):
# class MimeTypeCategor categorizer(FileCategorizer):
#     """Alternative categorizer using MIME types instead of extensions."""
#     def categorize(self, filepath: Path) -> FileCategory:
#         # Implementation using python-magic or mimetypes
#         pass
