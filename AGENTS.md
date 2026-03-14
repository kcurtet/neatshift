# Guía LLM - Organizador de Archivos

**Stack:** Python 3.12+ + Flet 0.27+ (UI multiplataforma)  
**Plataformas:** Linux, Windows, macOS, Web, Android, iOS

## Resumen

App que organiza archivos automáticamente por categoría (Documentos, Imágenes, Videos, etc.) y fecha (YYYY/MM). Selección de carpetas origen/destino, vista previa, ejecución con progreso, categorización por extensión.

## Estructura

```
src/
├── main.py                    # Entry point (ft.run)
├── config/
│   ├── settings.py            # Categorías, ventana
│   └── theme.py               # Colores
├── domain/
│   ├── file_categorizer.py   # Protocol + implementación
│   └── file_item.py           # Data class
├── services/
│   ├── file_service.py        # I/O operations
│   ├── windows_file_service.py # CopyFile2 API (Windows)
│   ├── performance_optimizer.py # Auto-detección workers
│   └── organization_service.py # Orquestación
└── ui/
    └── file_organizer_view.py # UI principal
```

## Patrones Críticos Flet

### 1. FilePicker (sin overlay)
```python
async def pick_folder(e):
    path = await ft.FilePicker().get_directory_path()
    if path:
        field.value = path
        page.update()
```

### 2. Threading (un nivel, page.update() thread-safe)
```python
def run_task():
    def worker():
        result = blocking_operation()
        self.display_result(result)
        self.page.update()  # Thread-safe
    self.page.run_thread(worker)
```

### 3. Verificación plataforma
```python
if not page.web:
    page.window.width = 800
    page.window.height = 600
```

### 4. API moderna
```python
ft.run(target=main)  # NO ft.app()
```

### 5. Async handlers
```python
async def handler(e):  # Solo si usas await
    result = await async_operation()
```

### 6. Update UI
```python
control.value = "nuevo"
page.update()  # Obligatorio
```

## Comandos

```bash
# Desarrollo
flet run
flet run --web

# Build
flet build linux --verbose
flet build windows --verbose
flet build macos --verbose
flet build web
flet build apk
flet build ipa

# Testing
python -m py_compile src/**/*.py
```

## Modificaciones Comunes

**Nueva categoría:** Edita `src/config/settings.py`
```python
class FileCategory(Enum):
    MI_CATEGORIA = "Mi Categoría"

FILE_EXTENSIONS = {
    FileCategory.MI_CATEGORIA: [".ext1", ".ext2"],
}
```

**Nuevo tema:** Edita `src/config/theme.py`
```python
class Theme:
    BG = "#1E1E1E"
    ACCENT = "#007ACC"
```

**Nuevo categorizador:** Implementa Protocol `FileCategorizer`
```python
from src.domain.file_categorizer import FileCategorizer

class MiCategorizador:
    def categorize(self, file_path: Path) -> str:
        return "Categoría"
```

## Optimizaciones de Rendimiento

### Paralelismo Nativo
- Windows: CopyFile2 API (Python 3.12+)
- Auto-detección: mismo drive (16 workers), cross-drive/red (8 workers)
- Sin dependencias externas (NO robocopy)

### Archivos Clave
- `src/services/windows_file_service.py` - CopyFile2
- `src/services/performance_optimizer.py` - Calculador workers
- `src/services/organization_service.py` - Orquestación

### Métricas Esperadas
- Mismo drive: ~80-100 files/sec (16 workers)
- Cross-drive: ~20-30 files/sec (8 workers)
- Red: ~15-25 files/sec (8 workers)

## Debugging

**Logs:** `~/.organizador-archivos/logs/app.log`

**Issues comunes:**
1. FilePicker no funciona → Linux: `sudo apt install zenity`
2. Threading errors → No anidar `page.run_thread`
3. Build falla → Ver `flet build --verbose`
4. Window config falla en web → Verificar `if not page.web:`

## Referencias

**Flet:**
- Docs: https://docs.flet.dev/
- FilePicker: https://docs.flet.dev/services/filepicker/
- Async: https://docs.flet.dev/cookbook/async-apps/
- Publishing: https://docs.flet.dev/publish/
- Issues: https://github.com/flet-dev/flet/issues
- Discord: https://discord.gg/dzWXP8SHG8

**Python:**
- pathlib: https://docs.python.org/3/library/pathlib.html
- shutil: https://docs.python.org/3/library/shutil.html
- asyncio: https://docs.python.org/3/library/asyncio.html

## Checklist Pre-Commit

- [ ] FilePicker sin overlay
- [ ] No anidar `page.run_thread`
- [ ] Verificar plataforma para window config
- [ ] `page.update()` después de modificar UI
- [ ] Async solo si usas await
- [ ] Logging apropiado
- [ ] `flet run` funciona

## Quick Start

1. Entry point: `src/main.py`
2. UI principal: `src/ui/file_organizer_view.py`
3. Config build: `pyproject.toml`
4. Probar: `flet run`
5. Build: `flet build linux --verbose`
6. Optimizaciones: Bytecode compilation, aggressive cleanup habilitadas

**Estado:** Listo para desarrollo y producción  
**Última actualización:** 2026-03-14
