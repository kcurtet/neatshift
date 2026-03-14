"""
User configuration model - Persists category settings and filters.
"""
import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional
import logging

from .settings import FileCategory, CATEGORY_EXTENSIONS

logger = logging.getLogger(__name__)

# Configuration file location
CONFIG_DIR = Path.home() / ".organizador-archivos"
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class CategoryConfig:
    """Configuration for a single file category."""
    
    category: str  # Category name (value from FileCategory enum)
    enabled: bool = True  # Whether this category is active
    organize_by_date: bool = True  # Whether to create date subfolders
    extensions: list[str] = field(default_factory=list)  # Custom extensions
    regex_patterns: list[str] = field(default_factory=list)  # Regex patterns
    
    def matches_file(self, filename: str) -> bool:
        """
        Check if a file matches this category's filters.
        
        Args:
            filename: Name of the file to check
            
        Returns:
            True if file matches any extension or regex pattern
        """
        if not self.enabled:
            return False
        
        # Check extensions
        file_lower = filename.lower()
        for ext in self.extensions:
            if file_lower.endswith(ext.lower()):
                return True
        
        # Check regex patterns
        for pattern in self.regex_patterns:
            try:
                if re.search(pattern, filename, re.IGNORECASE):
                    return True
            except re.error:
                logger.warning(f"Invalid regex pattern: {pattern}")
        
        return False


@dataclass
class UserConfig:
    """Complete user configuration."""
    
    categories: dict[str, CategoryConfig] = field(default_factory=dict)
    skip_hidden_files: bool = True
    last_source_path: str = ""
    last_dest_path: str = ""
    
    @classmethod
    def load(cls) -> "UserConfig":
        """
        Load configuration from file, or create default if not exists.
        
        Returns:
            UserConfig instance
        """
        if not CONFIG_FILE.exists():
            return cls.create_default()
        
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Deserialize category configs
            categories = {}
            for cat_name, cat_data in data.get('categories', {}).items():
                categories[cat_name] = CategoryConfig(**cat_data)
            
            config = cls(
                categories=categories,
                skip_hidden_files=data.get('skip_hidden_files', True),
                last_source_path=data.get('last_source_path', ''),
                last_dest_path=data.get('last_dest_path', ''),
            )
            
            logger.info(f"Loaded configuration from {CONFIG_FILE}")
            return config
            
        except Exception as e:
            logger.error(f"Error loading config: {e}, using defaults")
            return cls.create_default()
    
    @classmethod
    def create_default(cls) -> "UserConfig":
        """
        Create default configuration from built-in categories.
        
        Returns:
            UserConfig with default settings
        """
        categories = {}
        
        # Initialize from built-in categories
        for cat in FileCategory:
            extensions = CATEGORY_EXTENSIONS.get(cat, [])
            categories[cat.value] = CategoryConfig(
                category=cat.value,
                enabled=True,
                organize_by_date=True,
                extensions=extensions.copy(),
                regex_patterns=[],
            )
        
        config = cls(categories=categories)
        logger.info("Created default configuration")
        return config
    
    def save(self) -> None:
        """Save configuration to file."""
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            
            # Serialize
            data = {
                'categories': {
                    name: asdict(config)
                    for name, config in self.categories.items()
                },
                'skip_hidden_files': self.skip_hidden_files,
                'last_source_path': self.last_source_path,
                'last_dest_path': self.last_dest_path,
            }
            
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved configuration to {CONFIG_FILE}")
            
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def get_category_config(self, category_name: str) -> Optional[CategoryConfig]:
        """Get configuration for a specific category."""
        return self.categories.get(category_name)
    
    def add_category(self, name: str, extensions: Optional[list[str]] = None) -> CategoryConfig:
        """
        Add a new custom category.
        
        Args:
            name: Category name
            extensions: Initial extensions (default: empty)
            
        Returns:
            The created CategoryConfig
        """
        config = CategoryConfig(
            category=name,
            enabled=True,
            organize_by_date=True,
            extensions=extensions or [],
            regex_patterns=[],
        )
        self.categories[name] = config
        return config
    
    def remove_category(self, category_name: str) -> bool:
        """
        Remove a category from configuration.
        
        Args:
            category_name: Name of category to remove
            
        Returns:
            True if category was removed, False if not found
        """
        if category_name in self.categories:
            del self.categories[category_name]
            return True
        return False
