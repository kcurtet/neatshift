"""
Settings view - Manage categories, filters, and application preferences.
"""
import flet as ft
from typing import Callable

from ..config import Theme
from ..config.user_config import UserConfig, CategoryConfig


class SettingsView:
    """
    Settings interface for managing categories and filters.
    Provides UI for customizing organization behavior.
    """
    
    def __init__(self, page: ft.Page, config: UserConfig, on_config_changed: Callable):
        self.page = page
        self.config = config
        self.on_config_changed = on_config_changed
        
        # UI controls
        self.category_list = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)
        
        self._build_ui()
        self._refresh_category_list()
    
    def _build_ui(self) -> None:
        """Build the settings interface."""
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.SETTINGS, color=Theme.ACCENT, size=28),
                ft.Text(
                    "Configuración",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=Theme.TEXT,
                ),
            ]),
            bgcolor=Theme.SURFACE,
            padding=ft.Padding(20, 14, 20, 14),
        )
        
        # Global settings
        global_settings = self._create_global_settings()
        
        # Category management
        category_section = self._create_category_section()
        
        # Build main layout
        self.view = ft.Column(
            [header, global_settings, category_section],
            expand=True,
            spacing=0,
        )
    
    def _create_global_settings(self) -> ft.Container:
        """Create global settings section."""
        skip_hidden = ft.Switch(
            label="Omitir archivos ocultos (que empiezan con .)",
            value=self.config.skip_hidden_files,
            active_color=Theme.ACCENT,
            on_change=self._on_skip_hidden_changed,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("General", size=16, weight=ft.FontWeight.BOLD, color=Theme.TEXT),
                skip_hidden,
            ], spacing=12),
            bgcolor=Theme.BG,
            padding=ft.Padding(20, 12, 20, 12),
        )
    
    def _create_category_section(self) -> ft.Container:
        """Create category management section."""
        # Add category button
        add_button = ft.FilledButton(
            "Nueva categoría",
            icon=ft.Icons.ADD,
            on_click=self._show_add_category_dialog,
            bgcolor=Theme.ACCENT,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(
                        "Categorías y filtros",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=Theme.TEXT,
                        expand=True,
                    ),
                    add_button,
                ]),
                ft.Divider(color=Theme.SURFACE, height=1),
                self.category_list,
            ], spacing=12, expand=True),
            bgcolor=Theme.BG,
            padding=ft.Padding(20, 12, 20, 12),
            expand=True,
        )
    
    def _refresh_category_list(self) -> None:
        """Refresh the category list display."""
        self.category_list.controls.clear()
        
        for cat_name, cat_config in sorted(self.config.categories.items()):
            card = self._create_category_card(cat_config)
            self.category_list.controls.append(card)
        
        if hasattr(self, 'view'):
            self.page.update()
    
    def _create_category_card(self, cat_config: CategoryConfig) -> ft.Container:
        """Create a card for a single category."""
        # Enable/disable switch
        enabled_switch = ft.Switch(
            value=cat_config.enabled,
            active_color=Theme.ACCENT,
            on_change=lambda e, cfg=cat_config: self._on_category_enabled_changed(cfg, e.control.value),
        )
        
        # Organize by date switch
        date_switch = ft.Switch(
            value=cat_config.organize_by_date,
            active_color=Theme.ACCENT,
            on_change=lambda e, cfg=cat_config: self._on_organize_by_date_changed(cfg, e.control.value),
        )
        
        # Extensions display
        ext_text = ", ".join(cat_config.extensions[:10])
        if len(cat_config.extensions) > 10:
            ext_text += f" ... (+{len(cat_config.extensions) - 10} más)"
        
        # Regex patterns display
        regex_text = ""
        if cat_config.regex_patterns:
            regex_text = f"{len(cat_config.regex_patterns)} patrón/es regex"
        
        return ft.Container(
            content=ft.Column([
                # Header row
                ft.Row([
                    ft.Text(
                        cat_config.category,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=Theme.TEXT,
                        expand=True,
                    ),
                    enabled_switch,
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color=Theme.ACCENT,
                        tooltip="Editar filtros",
                        on_click=lambda e, cfg=cat_config: self._show_edit_filters_dialog(cfg),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=Theme.DANGER,
                        tooltip="Eliminar categoría",
                        on_click=lambda e, cfg=cat_config: self._confirm_delete_category(cfg),
                    ),
                ]),
                # Options row
                ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_MONTH, size=16, color=Theme.SUBTEXT),
                    ft.Text("Organizar por fecha:", size=12, color=Theme.SUBTEXT),
                    date_switch,
                ], spacing=6),
                # Extensions
                ft.Row([
                    ft.Icon(ft.Icons.EXTENSION, size=16, color=Theme.SUBTEXT),
                    ft.Text(
                        ext_text or "Sin extensiones",
                        size=11,
                        color=Theme.SUBTEXT,
                        expand=True,
                    ),
                ], spacing=6),
                # Regex patterns
                ft.Row([
                    ft.Icon(ft.Icons.CODE, size=16, color=Theme.SUBTEXT),
                    ft.Text(
                        regex_text or "Sin patrones regex",
                        size=11,
                        color=Theme.SUBTEXT,
                    ),
                ], spacing=6) if regex_text or True else ft.Container(),
            ], spacing=8),
            bgcolor=Theme.CARD,
            border_radius=8,
            padding=ft.Padding(16, 12, 16, 12),
        )
    
    def _show_add_category_dialog(self, e: ft.ControlEvent) -> None:
        """Show dialog to add a new category."""
        name_field = ft.TextField(
            label="Nombre de la categoría",
            bgcolor=Theme.CARD,
            border_color=Theme.ACCENT,
            color=Theme.TEXT,
        )
        
        extensions_field = ft.TextField(
            label="Extensiones (separadas por comas)",
            hint_text=".jpg, .png, .gif",
            bgcolor=Theme.CARD,
            border_color=Theme.ACCENT,
            color=Theme.TEXT,
            multiline=True,
            min_lines=2,
            max_lines=4,
        )
        
        def on_add(e: ft.ControlEvent) -> None:
            """Add button clicked."""
            name = name_field.value.strip()
            if not name:
                return
            
            # Parse extensions
            extensions = []
            if extensions_field.value:
                extensions = [
                    ext.strip()
                    for ext in extensions_field.value.split(',')
                    if ext.strip()
                ]
                # Ensure extensions start with dot
                extensions = [
                    ext if ext.startswith('.') else f'.{ext}'
                    for ext in extensions
                ]
            
            # Add category
            self.config.add_category(name, extensions)
            self.config.save()
            self._refresh_category_list()
            self.on_config_changed()
            
            dlg.open = False
            self.page.update()
        
        def on_cancel(e: ft.ControlEvent) -> None:
            """Cancel button clicked."""
            dlg.open = False
            self.page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nueva categoría"),
            content=ft.Column([name_field, extensions_field], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=on_cancel),
                ft.FilledButton("Añadir", on_click=on_add, bgcolor=Theme.ACCENT),
            ],
            open=True,
        )
        self.page.overlay.append(dlg)
        self.page.update()
    
    def _show_edit_filters_dialog(self, cat_config: CategoryConfig) -> None:
        """Show dialog to edit category filters."""
        # Extensions field
        ext_value = ", ".join(cat_config.extensions)
        extensions_field = ft.TextField(
            label="Extensiones (separadas por comas)",
            value=ext_value,
            bgcolor=Theme.CARD,
            border_color=Theme.ACCENT,
            color=Theme.TEXT,
            multiline=True,
            min_lines=3,
            max_lines=6,
        )
        
        # Regex patterns field
        regex_value = "\n".join(cat_config.regex_patterns)
        regex_field = ft.TextField(
            label="Patrones regex (uno por línea)",
            hint_text="^backup_.*\\.txt$\nreport_\\d{4}.*",
            value=regex_value,
            bgcolor=Theme.CARD,
            border_color=Theme.ACCENT,
            color=Theme.TEXT,
            multiline=True,
            min_lines=3,
            max_lines=6,
        )
        
        def on_save(e: ft.ControlEvent) -> None:
            """Save button clicked."""
            # Parse extensions
            if extensions_field.value:
                extensions = [
                    ext.strip()
                    for ext in extensions_field.value.split(',')
                    if ext.strip()
                ]
                # Ensure extensions start with dot
                extensions = [
                    ext if ext.startswith('.') else f'.{ext}'
                    for ext in extensions
                ]
                cat_config.extensions = extensions
            else:
                cat_config.extensions = []
            
            # Parse regex patterns
            if regex_field.value:
                patterns = [
                    line.strip()
                    for line in regex_field.value.split('\n')
                    if line.strip()
                ]
                cat_config.regex_patterns = patterns
            else:
                cat_config.regex_patterns = []
            
            self.config.save()
            self._refresh_category_list()
            self.on_config_changed()
            
            dlg.open = False
            self.page.update()
        
        def on_cancel(e: ft.ControlEvent) -> None:
            """Cancel button clicked."""
            dlg.open = False
            self.page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Filtros: {cat_config.category}"),
            content=ft.Column([
                extensions_field,
                ft.Divider(color=Theme.SURFACE),
                regex_field,
                ft.Text(
                    "💡 Tip: Los patrones regex permiten filtros avanzados como fechas, números, etc.",
                    size=11,
                    color=Theme.SUBTEXT,
                    italic=True,
                ),
            ], tight=True, height=400),
            actions=[
                ft.TextButton("Cancelar", on_click=on_cancel),
                ft.FilledButton("Guardar", on_click=on_save, bgcolor=Theme.SUCCESS),
            ],
            open=True,
        )
        self.page.overlay.append(dlg)
        self.page.update()
    
    def _confirm_delete_category(self, cat_config: CategoryConfig) -> None:
        """Confirm category deletion."""
        def on_confirm(e: ft.ControlEvent) -> None:
            """Delete confirmed."""
            self.config.remove_category(cat_config.category)
            self.config.save()
            self._refresh_category_list()
            self.on_config_changed()
            
            dlg.open = False
            self.page.update()
        
        def on_cancel(e: ft.ControlEvent) -> None:
            """Cancel deletion."""
            dlg.open = False
            self.page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(
                f"¿Eliminar la categoría '{cat_config.category}'?\n\n"
                "Esta acción no se puede deshacer."
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=on_cancel),
                ft.FilledButton(
                    "Eliminar",
                    on_click=on_confirm,
                    bgcolor=Theme.DANGER,
                ),
            ],
            open=True,
        )
        self.page.overlay.append(dlg)
        self.page.update()
    
    def _on_category_enabled_changed(self, cat_config: CategoryConfig, value: bool) -> None:
        """Category enabled switch changed."""
        cat_config.enabled = value
        self.config.save()
        self.on_config_changed()
        self._refresh_category_list()
    
    def _on_organize_by_date_changed(self, cat_config: CategoryConfig, value: bool) -> None:
        """Organize by date switch changed."""
        cat_config.organize_by_date = value
        self.config.save()
        self.on_config_changed()
        self._refresh_category_list()
    
    def _on_skip_hidden_changed(self, e: ft.ControlEvent) -> None:
        """Skip hidden files switch changed."""
        self.config.skip_hidden_files = e.control.value
        self.config.save()
        self.on_config_changed()
        self.page.update()
    
    def get_view(self) -> ft.Column:
        """Get the settings view control."""
        return self.view
