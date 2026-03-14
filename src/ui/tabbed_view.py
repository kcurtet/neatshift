import flet as ft
from config.theme import Theme
from config.user_config import UserConfig
from ui.file_organizer_view import FileOrganizerView
from ui.settings_view import SettingsView


class FileOrganizerApp:
    """
    Main application coordinator - creates and manages tabs.
    Single Responsibility: Application orchestration.
    """
    
    def __init__(self, page: ft.Page):
        self.page = page
        
        # Load user configuration
        self.config = UserConfig.load()
        
        # Create views
        self.organizer_view = FileOrganizerView(page)
        self.settings_view = SettingsView(page, self.config, self._on_config_changed)
        
        # Build UI
        self._build_ui()
    
    def _on_config_changed(self):
        """Handle configuration changes."""
        self.config.save()
        # Refresh organizer view with new config
        self.organizer_view.refresh_config()
    
    def _build_ui(self):
        """Build the tabbed interface."""
        # Configure page
        self.page.title = "Organizador de Archivos"
        self.page.bgcolor = Theme.BG
        self.page.padding = 0
        
        # Configure window only on desktop platforms
        if not self.page.web:
            self.page.window.width = 900
            self.page.window.height = 700
            self.page.window.min_width = 700
            self.page.window.min_height = 500
        
        # Create tabs
        tabs = ft.Tabs(
            length=2,
            selected_index=0,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Organizador", icon=ft.Icons.FOLDER_SPECIAL),
                            ft.Tab(label="Configuración", icon=ft.Icons.SETTINGS),
                        ]
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            self.organizer_view.get_view(),
                            self.settings_view.get_view(),
                        ]
                    ),
                ]
            ),
        )
        
        # Add tabs to the page
        self.page.add(tabs)