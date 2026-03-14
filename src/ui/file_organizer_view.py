"""
Main application view - Coordinates UI and business logic.
Follows Single Responsibility and Dependency Inversion principles.
"""
import flet as ft
from pathlib import Path

from config import AppSettings, Theme
from config.user_config import UserConfig
from domain import DefaultFileCategorizer
from domain.file_item import FileItem, FileStatus
from services import OrganizationService


class FileOrganizerView:
    """
    Main application view coordinating UI and services.
    Single Responsibility: UI coordination and user interaction.
    Dependency Inversion: Depends on service abstractions.
    """

    def __init__(self, page: ft.Page, user_config: UserConfig | None = None):
        self.page = page
        self.user_config = user_config or UserConfig.load()

        # Load saved paths
        self.source_path = self.user_config.last_source_path
        self.dest_path = self.user_config.last_dest_path

        self.plan: list[FileItem] = []
        self.status_texts: list[ft.Text] = []

        # Initialize services (Dependency Injection)
        categorizer = DefaultFileCategorizer()
        self.org_service = OrganizationService(categorizer)

        # Build UI
        self.view = self._build_ui()

        # Initialize field values with saved paths
        if self.source_path:
            self.source_field.value = self.source_path
        if self.dest_path:
            self.dest_field.value = self.dest_path
    
    def _configure_page(self) -> None:
        """Configure page properties."""
        self.page.title = "Organizador de Archivos"
        self.page.bgcolor = Theme.BG
        self.page.padding = 0
        
        # Configure window only on desktop platforms
        # page.web is True when running in browser
        if not self.page.web:
            # Desktop only (Windows, macOS, Linux native)
            self.page.window.width = AppSettings.WINDOW_WIDTH
            self.page.window.height = AppSettings.WINDOW_HEIGHT
            self.page.window.min_width = AppSettings.MIN_WIDTH
            self.page.window.min_height = AppSettings.MIN_HEIGHT
    
    def _build_ui(self) -> ft.Column:
        """Build the user interface."""
        # Header
        header = self._create_header()
        
        # Path selectors
        path_container = self._create_path_selectors()
        
        # Action buttons
        action_bar = self._create_action_bar()
        
        # Summary
        self.summary_row = ft.Row(wrap=True, spacing=8)
        summary_container = ft.Container(
            content=self.summary_row,
            bgcolor=Theme.BG,
            padding=ft.Padding(20, 4, 20, 4),
        )
        
        # File table
        table_container = self._create_table()
        
        # Status bar
        status_bar = self._create_status_bar()
        
        return ft.Column(
            [header, path_container, action_bar, summary_container, 
             table_container, status_bar],
            expand=True,
            spacing=0,
        )
    
    def _create_header(self) -> ft.Container:
        """Create header section."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.FOLDER, color=Theme.ACCENT, size=28),
                    ft.Text(
                        "Organizador de Archivos",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=Theme.TEXT,
                    ),
                    ft.Text(
                        "Organiza tu disco por categoría y fecha",
                        size=12,
                        color=Theme.SUBTEXT,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            bgcolor=Theme.SURFACE,
            padding=ft.Padding(20, 14, 20, 14),
        )
    
    def _create_path_selectors(self) -> ft.Container:
        """Create path selector widgets."""
        self.source_field = ft.TextField(
            label="Carpeta de origen",
            read_only=True,
            bgcolor=Theme.CARD,
            border_color=ft.Colors.TRANSPARENT,
            color=Theme.TEXT,
            expand=True,
        )
        
        self.dest_field = ft.TextField(
            label="Carpeta de destino",
            read_only=True,
            bgcolor=Theme.CARD,
            border_color=ft.Colors.TRANSPARENT,
            color=Theme.TEXT,
            expand=True,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row([
                        self.source_field,
                        ft.Button(
                            "Examinar",
                            icon=ft.Icons.FOLDER_OPEN,
                            on_click=self.pick_source,
                            bgcolor=Theme.CARD,
                            color=Theme.TEXT,
                        ),
                    ], expand=True),
                    ft.Row([
                        self.dest_field,
                        ft.Button(
                            "Examinar",
                            icon=ft.Icons.FOLDER_OPEN,
                            on_click=self.pick_dest,
                            bgcolor=Theme.CARD,
                            color=Theme.TEXT,
                        ),
                    ], expand=True),
                ],
                spacing=10,
            ),
            bgcolor=Theme.BG,
            padding=ft.Padding(20, 10, 20, 10),
        )
    
    def _create_action_bar(self) -> ft.Container:
        """Create action button bar."""
        self.btn_preview = ft.Button(
            "Vista previa",
            icon=ft.Icons.SEARCH,
            on_click=self.run_preview,
            bgcolor=Theme.ACCENT,
            color=ft.Colors.WHITE,
        )
        
        self.btn_apply = ft.Button(
            "Aplicar cambios",
            icon=ft.Icons.CHECK,
            on_click=self.apply_changes,
            bgcolor=Theme.SUCCESS,
            color=Theme.BG,
            disabled=True,
        )
        
        return ft.Container(
            content=ft.Row(
                [
                    self.btn_preview,
                    self.btn_apply,
                    ft.Container(expand=True),
                    ft.Button(
                        "Limpiar",
                        icon=ft.Icons.DELETE_OUTLINE,
                        on_click=self.clear_all,
                        bgcolor=Theme.CARD,
                        color=Theme.TEXT,
                    ),
                ],
            ),
            bgcolor=Theme.BG,
            padding=ft.Padding(20, 4, 20, 4),
        )
    
    def _create_table(self) -> ft.Container:
        """Create file list table."""
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Archivo", color=Theme.SUBTEXT, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Categoría", color=Theme.SUBTEXT, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Fecha", color=Theme.SUBTEXT, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Destino", color=Theme.SUBTEXT, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Estado", color=Theme.SUBTEXT, weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            bgcolor=Theme.CARD,
            heading_row_color=Theme.SURFACE,
            data_row_color={"hovered": Theme.SURFACE},
        )
        
        return ft.Container(
            content=ft.Column([self.data_table], scroll=ft.ScrollMode.AUTO, expand=True),
            bgcolor=Theme.BG,
            padding=ft.Padding(20, 6, 20, 6),
            expand=True,
        )
    
    def _create_status_bar(self) -> ft.Container:
        """Create status and progress bar."""
        self.status_text = ft.Text(
            "Selecciona la carpeta de origen y destino para comenzar.",
            color=Theme.SUBTEXT,
            size=12,
            expand=True,
        )
        
        self.progress_pct = ft.Text(
            "0%",
            color=Theme.ACCENT,
            size=12,
            weight=ft.FontWeight.BOLD,
        )
        
        self.progress_bar = ft.ProgressBar(
            value=0,
            bar_height=8,
            color=Theme.ACCENT,
            bgcolor=Theme.SURFACE,
            expand=True,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([self.status_text, self.progress_pct],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.progress_bar,
            ], spacing=4),
            bgcolor=Theme.SURFACE,
            padding=ft.Padding(16, 8, 16, 8),
        )
    
    # Event handlers
    
    async def pick_source(self, e: ft.ControlEvent) -> None:
        """Pick source directory."""
        path = await ft.FilePicker().get_directory_path()
        if path:
            self.source_path = path
            self.source_field.value = path
            # Save to user config
            self.user_config.last_source_path = path
            self.user_config.save()
            self.page.update()

    async def pick_dest(self, e: ft.ControlEvent) -> None:
        """Pick destination directory."""
        path = await ft.FilePicker().get_directory_path()
        if path:
            self.dest_path = path
            self.dest_field.value = path
            # Save to user config
            self.user_config.last_dest_path = path
            self.user_config.save()
            self.page.update()
    
    def run_preview(self, e: ft.ControlEvent) -> None:
        """Scan files and show organization preview."""
        if not self.source_path or not self.dest_path:
            self.show_snackbar("Selecciona tanto la carpeta de origen como de destino", Theme.WARNING)
            return
        
        if not Path(self.source_path).exists():
            self.show_snackbar("La carpeta de origen no existe", Theme.DANGER)
            return
        
        self.status_text.value = "Analizando archivos..."
        self.btn_preview.disabled = True
        self.btn_apply.disabled = True
        self.page.update()
        
        def scan() -> None:
            """Background task: scan source directory and display organization plan."""
            plan = self.org_service.scan_and_plan(
                Path(self.source_path),
                Path(self.dest_path)
            )
            # page.update() is thread-safe, can call directly from worker thread
            self.display_plan(plan)
            self.page.update()
        
        self.page.run_thread(scan)
    
    def display_plan(self, plan: list[FileItem]) -> None:
        """Display the organization plan in the table."""
        self.plan = plan
        self.data_table.rows.clear()
        self.status_texts.clear()
        
        for item in plan:
            status_color = Theme.SUBTEXT
            status_text = ft.Text(item.status.value, color=status_color, size=11)
            self.status_texts.append(status_text)
            
            self.data_table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(item.filename, color=Theme.TEXT, size=11)),
                ft.DataCell(ft.Text(item.category, color=Theme.TEXT, size=11)),
                ft.DataCell(ft.Text(item.date, color=Theme.TEXT, size=11)),
                ft.DataCell(ft.Text(str(item.dst), color=Theme.TEXT, size=11,
                                   overflow=ft.TextOverflow.ELLIPSIS)),
                ft.DataCell(status_text),
            ]))
        
        self.render_summary()
        total = len(plan)
        self.status_text.value = (
            f"{total} archivo{'s' if total != 1 else ''} encontrado{'s' if total != 1 else ''}. "
            "Revisa la lista y pulsa «Aplicar cambios» para moverlos."
        )
        self.btn_preview.disabled = False
        self.btn_apply.disabled = total == 0
        self.progress_bar.value = 0
        self.page.update()
    
    def render_summary(self) -> None:
        """Render category summary chips."""
        self.summary_row.controls.clear()
        
        counts: dict[str, int] = {}
        for item in self.plan:
            counts[item.category] = counts.get(item.category, 0) + 1
        
        for category, count in sorted(counts.items(), key=lambda x: -x[1]):
            # Get icon from theme - note: category is string value, need to convert
            from config.settings import FileCategory
            cat_enum = next((c for c in FileCategory if c.value == category), FileCategory.OTHER)
            icon = Theme.get_category_icon(cat_enum)
            
            self.summary_row.controls.append(ft.Container(
                content=ft.Row([
                    ft.Icon(icon, color=Theme.TEXT, size=16),
                    ft.Text(f"{category}  {count}", color=Theme.TEXT, size=12),
                ], spacing=6),
                bgcolor=Theme.CARD,
                border_radius=8,
                padding=ft.Padding(10, 4, 10, 4),
            ))
    
    def apply_changes(self, e: ft.ControlEvent) -> None:
        """Apply file organization."""
        if not self.plan:
            return
        
        def confirm(e: ft.ControlEvent) -> None:
            """Confirmation dialog: User confirmed organization."""
            dlg.open = False
            self.page.update()
            self.execute_moves()
        
        def cancel(e: ft.ControlEvent) -> None:
            """Confirmation dialog: User cancelled operation."""
            dlg.open = False
            self.page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar organización"),
            content=ft.Text(
                f"Se moverán {len(self.plan)} archivos a su nueva ubicación.\n\n¿Continuar?"
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel),
                ft.TextButton("Continuar", on_click=confirm),
            ],
            open=True,
        )
        self.page.overlay.append(dlg)
        self.page.update()
    
    def execute_moves(self) -> None:
        """Execute file moves in background."""
        self.btn_apply.disabled = True
        self.btn_preview.disabled = True
        self.progress_bar.value = 0
        self.progress_pct.value = "0%"
        self.status_text.value = "Moviendo archivos..."
        self.page.update()
        
        def move_worker() -> None:
            """Background task: execute file organization plan."""
            successful, errors = self.org_service.execute_plan(
                self.plan,
                progress_callback=self.on_progress,
            )
            # page.update() is thread-safe, can call directly from worker thread
            self.finalize_results(successful, errors)
            self.page.update()
        
        self.page.run_thread(move_worker)
    
    def on_progress(self, idx: int, item: FileItem, count: int, total: int) -> None:
        """Progress callback from organization service."""
        # Update row status
        if idx < len(self.status_texts):
            color = Theme.SUCCESS if item.status == FileStatus.OK else Theme.DANGER
            self.status_texts[idx].value = item.status.value
            self.status_texts[idx].color = color
        
        # Calculate dynamic batch size based on total files
        batch_size = AppSettings.get_ui_batch_size(total)
        
        # Update progress every N files or at the end
        if count % batch_size == 0 or count == total:
            pct = count / total
            self.progress_bar.value = pct
            self.progress_pct.value = f"{int(pct * 100)}%"
            ok = sum(1 for i in self.plan if i.status == FileStatus.OK)
            self.status_text.value = f"Moviendo archivos... ({ok}/{total})"
            self.page.update()
    
    def finalize_results(self, successful: int, errors: int) -> None:
        """Show final results."""
        self.progress_bar.value = 1.0
        self.progress_pct.value = "100%"
        self.status_text.value = (
            f"Completado — {successful} movido{'s' if successful != 1 else ''} correctamente"
            + (f", {errors} con error" if errors else "")
        )
        self.btn_preview.disabled = False
        self.page.update()
        
        def close(e: ft.ControlEvent) -> None:
            """Results dialog: close button clicked."""
            dlg.open = False
            self.page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Organización completada"),
            content=ft.Text(
                f"Archivos movidos: {successful}" + (f"\nCon errores: {errors}" if errors else "")
            ),
            actions=[ft.TextButton("OK", on_click=close)],
            open=True,
        )
        self.page.overlay.append(dlg)
        self.page.update()
    
    def clear_all(self, e: ft.ControlEvent) -> None:
        """Clear all data and reset UI."""
        self.data_table.rows.clear()
        self.summary_row.controls.clear()
        self.plan.clear()
        self.status_texts.clear()
        self.progress_bar.value = 0
        self.progress_pct.value = "0%"
        self.status_text.value = "Selecciona la carpeta de origen y destino para comenzar."
        self.btn_apply.disabled = True
        self.page.update()
    
    def show_snackbar(self, message: str, color: str) -> None:
        """Show snackbar notification."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color,
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def get_view(self) -> ft.Column:
        """Get the file organizer view control."""
        return self.view
    
    def refresh_config(self):
        """Refresh configuration (placeholder for future implementation)."""
        # TODO: Implement configuration refresh logic
        pass
