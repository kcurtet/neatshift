"""
File Organizer Application

This application follows SOLID principles:

1. **Single Responsibility Principle (SRP)**:
   - AppSettings: Only handles configuration
   - Theme: Only handles visual styling
   - FileItem: Only represents file data
   - FileCategorizer: Only handles categorization logic
   - FileService: Only handles file I/O operations
   - OrganizationService: Only coordinates organization workflow
   - FileOrganizerView: Only handles UI presentation

2. **Open/Closed Principle (OCP)**:
   - FileCategorizer is a Protocol - can add new categorization strategies
     without modifying existing code (e.g., MimeTypeCategorizer)

3. **Liskov Substitution Principle (LSP)**:
   - Any FileCategorizer implementation can be substituted
   - DefaultFileCategorizer can be replaced with any other categorizer

4. **Interface Segregation Principle (ISP)**:
   - Small, focused interfaces (FileCategorizer, ProgressCallback)
   - Clients depend only on what they use

5. **Dependency Inversion Principle (DIP)**:
   - OrganizationService depends on FileCategorizer abstraction (Protocol),
     not on concrete DefaultFileCategorizer
   - Dependencies are injected, not hard-coded

Benefits of this architecture:
- Easy to test (can inject mock services)
- Easy to extend (add new categorizers, file services)
- Clear separation of concerns
- Each module has a single, well-defined purpose
"""

import logging
import sys
from pathlib import Path

# Add project root to Python path
# This allows imports to work when running with 'flet run' or 'python src/main.py'
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import flet as ft

from src.ui import FileOrganizerView


def setup_logging() -> None:
    """
    Configure application logging.
    
    Logs to both console and file for debugging.
    File logs are stored in user's home directory.
    """
    # Create logs directory in user home
    log_dir = Path.home() / ".organizador-archivos" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            # Console handler (INFO and above)
            logging.StreamHandler(sys.stdout),
            # File handler (DEBUG and above, with rotation)
            logging.FileHandler(log_file, mode="a", encoding="utf-8"),
        ],
    )
    
    # Set specific loggers to appropriate levels
    logging.getLogger("src.services").setLevel(logging.INFO)
    logging.getLogger("src.domain").setLevel(logging.WARNING)
    logging.getLogger("src.ui").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")


async def main(page: ft.Page) -> None:
    """
    Application entry point.
    Creates and displays the main view with injected dependencies.
    """
    # Initialize logging
    setup_logging()
    
    # Create main view
    FileOrganizerView(page)


if __name__ == "__main__":
    ft.run(main)
