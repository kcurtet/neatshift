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

Platform Support:
- Configuration and logs use platform-appropriate directories via platformdirs
- Linux: ~/.config/neatshift/ and ~/.local/state/neatshift/log/
- macOS: ~/Library/Application Support/neatshift/ and ~/Library/Logs/neatshift/
- Windows: %APPDATA%\\neatshift\\ and %LOCALAPPDATA%\\neatshift\\log\\
"""

import logging
import sys
from pathlib import Path

import flet as ft

from ui.tabbed_view import FileOrganizerApp
from config.user_config import LOG_DIR


def setup_logging() -> None:
    """
    Configure application logging.

    Logs to both console and file for debugging.
    File logs are stored in platform-appropriate directory:
    - Linux: ~/.local/state/neatshift/log/
    - macOS: ~/Library/Logs/neatshift/
    - Windows: %LOCALAPPDATA%\\neatshift\\log\\
    """
    # Create logs directory
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "app.log"
    
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
    logging.getLogger("services").setLevel(logging.INFO)
    logging.getLogger("domain").setLevel(logging.WARNING)
    logging.getLogger("ui").setLevel(logging.WARNING)
    logging.getLogger("config").setLevel(logging.INFO)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")


async def main(page: ft.Page) -> None:
    """
    Application entry point.
    Creates and displays the main tabbed view with configuration support.
    """
    # Initialize logging
    setup_logging()
    
    # Create main app with tabs
    FileOrganizerApp(page)


if __name__ == "__main__":
    ft.run(main)
