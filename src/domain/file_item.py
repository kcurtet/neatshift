"""
File item entity - Single Responsibility Principle.
Represents a file to be organized with its metadata.
"""
from dataclasses import dataclass
from pathlib import Path
from enum import Enum


class FileStatus(Enum):
    """Status of file operation."""
    PENDING = "pendiente"
    OK = "ok"
    ERROR = "error"


@dataclass
class FileItem:
    """
    File item entity representing a file to be organized.
    Immutable except for status and actual destination.
    """
    src: Path
    dst: Path
    category: str
    date: str
    filename: str
    status: FileStatus = FileStatus.PENDING
    
    def mark_success(self, actual_dst: Path) -> None:
        """Mark file as successfully moved."""
        self.dst = actual_dst
        self.status = FileStatus.OK
    
    def mark_error(self) -> None:
        """Mark file operation as failed."""
        self.status = FileStatus.ERROR
    
    def to_dict(self) -> dict:
        """Convert to dictionary for compatibility."""
        return {
            "src": self.src,
            "dst": self.dst,
            "category": self.category,
            "date": self.date,
            "filename": self.filename,
            "status": self.status.value,
        }
