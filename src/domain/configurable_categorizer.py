"""
Configurable file categorizer - Uses UserConfig for dynamic categorization.
"""
from pathlib import Path
from typing import Optional

from ..config.settings import FileCategory
from ..config.user_config import UserConfig, CategoryConfig


class ConfigurableFileCategorizer:
    """
    File categorizer that uses UserConfig for dynamic category matching.
    Supports custom extensions and regex patterns per category.
    """
    
    def __init__(self, config: UserConfig):
        """
        Initialize with user configuration.
        
        Args:
            config: UserConfig instance with category definitions
        """
        self.config = config
    
    def categorize(self, filepath: Path) -> tuple[str, bool]:
        """
        Categorize file based on user configuration.
        
        Args:
            filepath: Path to the file to categorize
            
        Returns:
            Tuple of (category_name, organize_by_date)
        """
        filename = filepath.name
        
        # Try to match against each enabled category
        for cat_name, cat_config in self.config.categories.items():
            if cat_config.enabled and cat_config.matches_file(filename):
                return cat_name, cat_config.organize_by_date
        
        # Default: OTHER category with date organization enabled
        # Try to find "Otros" category in config, create if missing
        other_config = self.config.categories.get("Otros")
        if other_config:
            return "Otros", other_config.organize_by_date
        
        # Fallback if no "Otros" category exists
        return "Otros", True
    
    def get_category_config(self, category_name: str) -> Optional[CategoryConfig]:
        """Get configuration for a specific category."""
        return self.config.get_category_config(category_name)
