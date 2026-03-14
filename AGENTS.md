# 🤖 Guía para LLMs - Organizador de Archivos

**Proyecto:** Organizador de Archivos (File Organizer)  
**Autor:** Kevin Curtet (kcurtet@gmail.com)  
**Tecnología:** Python + Flet (UI multiplataforma)  
**Plataformas:** Linux, Windows, macOS, Web, Android, iOS

---

## 📋 Tabla de Contenidos

- [Resumen del Proyecto](#resumen-del-proyecto)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnología: Flet](#tecnología-flet)
- [Referencias Externas](#referencias-externas)
- [Comandos Comunes](#comandos-comunes)
- [Patrones Importantes](#patrones-importantes)
- [Debugging](#debugging)
- [Build y Publicación](#build-y-publicación)
- [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 📖 Resumen del Proyecto

**¿Qué hace?**
Organiza archivos automáticamente por categoría (Documentos, Imágenes, Videos, etc.) y fecha (YYYY/MM), moviéndolos de una carpeta origen a una carpeta destino estructurada.

**Funcionalidades principales:**
1. Selección de carpetas origen/destino con FilePicker
2. Vista previa de la organización (scan sin mover archivos)
3. Ejecución de movimientos con barra de progreso
4. Categorización automática por extensión
5. Organización por fecha de modificación

**Estado actual:**
- ✅ Código conforme a docs oficiales de Flet v0.82+
- ✅ Optimizaciones de build aplicadas (bytecode, cleanup)
- ✅ Compatible multiplataforma (desktop, web, móvil)
- ✅ Sin memory leaks ni API deprecated

---

## 📁 Estructura del Proyecto

```
file-organizer/
├── src/
│   ├── main.py                    # Entry point (ft.run)
│   ├── assets/                    # Iconos y recursos
│   │   ├── icon.png               # 512×512px app icon
│   │   └── splash.png             # 512×512px splash screen
│   ├── config/
│   │   ├── settings.py            # Configuración (categorías, ventana)
│   │   └── theme.py               # Colores y estilos
│   ├── domain/
│   │   ├── file_categorizer.py   # Protocol + implementación
│   │   └── file_item.py           # Data class FileItem
│   ├── services/
│   │   ├── file_service.py        # I/O operations
│   │   └── organization_service.py # Orquestación del workflow
│   └── ui/
│       └── file_organizer_view.py # UI principal (Vista)
├── pyproject.toml                 # Configuración Flet (optimizada)
├── README.md                      # Documentación para usuarios
└── AGENTS.md                      # Esta guía (para LLMs)
```

**Archivos clave:**
- `src/main.py` - Entry point y setup
- `src/ui/file_organizer_view.py` - UI principal
- `pyproject.toml` - Configuración de build

---

## 🎨 Tecnología: Flet

**Flet** es un framework Python para crear aplicaciones multiplataforma con una sola codebase.

### Conceptos Clave

#### 1. Page
El contenedor principal de la app:

```python
async def main(page: ft.Page) -> None:
    page.title = "Mi App"
    page.add(ft.Text("Hola"))
```

#### 2. Controles
Widgets de UI (TextField, Button, DataTable, etc.):

```python
btn = ft.Button("Click me", on_click=handler)
page.add(btn)
```

#### 3. Async/Await
Flet soporta async handlers:

```python
async def pick_folder(e: ft.ControlEvent) -> None:
    path = await ft.FilePicker().get_directory_path()
    # ✅ Correcto: no necesita overlay
```

#### 4. Threading
Para operaciones bloqueantes:

```python
def heavy_task():
    result = blocking_io_operation()
    # page.update() es thread-safe ✅
    self.display_result(result)
    self.page.update()

page.run_thread(heavy_task)  # ✅ Correcto
```

**⚠️ NO ANIDAR `page.run_thread`:**
```python
# ❌ INCORRECTO
def task():
    result = compute()
    page.run_thread(lambda: update_ui(result))  # ❌ Innecesario

# ✅ CORRECTO
def task():
    result = compute()
    update_ui(result)  # page.update() es thread-safe
    page.update()
```

#### 5. FilePicker
Selector de archivos/carpetas:

```python
# ✅ CORRECTO según docs oficiales
async def pick_folder(e):
    path = await ft.FilePicker().get_directory_path()
    if path:
        field.value = path
        page.update()

# ❌ INCORRECTO (no agregar al overlay)
picker = ft.FilePicker()
page.overlay.append(picker)  # ❌ Innecesario
```

#### 6. Multiplataforma
Verificar plataforma antes de configurar:

```python
# ✅ CORRECTO
if not page.web:
    # Solo en desktop
    page.window.width = 800
    page.window.height = 600
```

### Patrones Flet Importantes

**1. Actualización de UI:**
```python
# Siempre llamar page.update() después de modificar controles
text.value = "Nuevo texto"
page.update()  # ✅ Obligatorio
```

**2. Overlay para diálogos:**
```python
dialog = ft.AlertDialog(title=ft.Text("Confirmar"), ...)
page.overlay.append(dialog)  # ✅ Correcto para diálogos
dialog.open = True
page.update()
```

**3. Async handlers:**
```python
# Handlers pueden ser sync o async
async def async_handler(e):  # ✅ Usa async si haces await
    result = await some_async_operation()

def sync_handler(e):  # ✅ Usa sync si no haces await
    do_something()
```

---

## 🔗 Referencias Externas

### Documentación Oficial de Flet
**Siempre consulta la documentación oficial cuando tengas dudas:**

| Tema | URL |
|------|-----|
| **FilePicker** (selectores) | https://docs.flet.dev/services/filepicker/ |
| **Async Apps** (async/await) | https://docs.flet.dev/cookbook/async-apps/ |
| **Publishing** (builds) | https://docs.flet.dev/publish/ |
| **Page API** (threading) | https://docs.flet.dev/controls/page/ |
| **Controles** (widgets) | https://docs.flet.dev/controls/ |
| **Getting Started** | https://flet.dev/docs/getting-started/ |
| **Gallery** (ejemplos) | https://flet-controls-gallery.fly.dev/ |

### Python
- **pathlib**: https://docs.python.org/3/library/pathlib.html
- **shutil**: https://docs.python.org/3/library/shutil.html
- **asyncio**: https://docs.python.org/3/library/asyncio.html
- **typing (Protocol)**: https://docs.python.org/3/library/typing.html#typing.Protocol

### Empaquetado
- **pyproject.toml**: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- **Flet Build**: https://docs.flet.dev/publish/

---

## 🛠️ Comandos Comunes

### Desarrollo
```bash
# Ejecutar en modo desarrollo
flet run

# Ejecutar con hot reload
flet run --web

# Verificar correcciones aplicadas
bash verificar_cambios.sh
```

### Build
```bash
# Build para Linux
flet build linux --verbose

# Build para Windows
flet build windows --verbose

# Build para macOS
flet build macos --verbose

# Build para Web
flet build web

# Build para Android (requiere SDK)
flet build apk

# Build para iOS (requiere macOS + Xcode)
flet build ipa
```

### Testing
```bash
# Verificar sintaxis
python -m py_compile src/**/*.py

# Type checking (si usas mypy)
mypy src/
```

### Git
```bash
# Ver cambios
git status
git diff

# Commit
git add -A
git commit -m "descripción"
git push origin main
```

---

## 🎯 Patrones Importantes

### 1. FilePicker - Patrón Correcto
**✅ HACER:**
```python
async def pick_source(self, e: ft.ControlEvent) -> None:
    path = await ft.FilePicker().get_directory_path()
    if path:
        self.source_path = path
        self.source_field.value = path
        self.page.update()
```

**❌ NO HACER:**
```python
async def pick_source(self, e: ft.ControlEvent) -> None:
    picker = ft.FilePicker()
    self.page.overlay.append(picker)  # ❌ Innecesario
    self.page.update()
    path = await picker.get_directory_path()
```

### 2. Threading - Patrón Correcto
**✅ HACER:**
```python
def run_task(self):
    def worker():
        result = blocking_operation()
        # page.update() es thread-safe
        self.display_result(result)
        self.page.update()
    
    self.page.run_thread(worker)  # ✅ Un nivel
```

**❌ NO HACER:**
```python
def run_task(self):
    def worker():
        result = blocking_operation()
        # ❌ Anidamiento innecesario
        self.page.run_thread(lambda: self.display_result(result))
    
    self.page.run_thread(worker)
```

### 3. Verificación de Plataforma
**✅ HACER:**
```python
def _configure_page(self):
    self.page.title = "Mi App"
    
    if not self.page.web:
        # Solo en desktop
        self.page.window.width = 800
        self.page.window.height = 600
```

**❌ NO HACER:**
```python
def _configure_page(self):
    self.page.title = "Mi App"
    # ❌ Falla en web/móvil
    self.page.window.width = 800
    self.page.window.height = 600
```

### 4. API Moderna
**✅ HACER:**
```python
if __name__ == "__main__":
    ft.run(target=main)  # ✅ API moderna (Flet 0.21.0+)
```

**❌ NO HACER:**
```python
if __name__ == "__main__":
    ft.app(target=main)  # ❌ Deprecated
```

### 5. Async Handlers
**✅ HACER:**
```python
# Usar async solo si haces await
async def handler_with_await(e):
    result = await async_operation()
    process(result)

# Usar sync si no haces await
def handler_without_await(e):
    process_sync()
```

**❌ NO HACER:**
```python
# ❌ async sin await es innecesario
async def handler(e):
    do_sync_stuff()  # No usa await
```

---

## 🐛 Debugging

### Logs
El proyecto usa logging estándar de Python:

```python
import logging
logger = logging.getLogger(__name__)
logger.info("Mensaje informativo")
logger.warning("Advertencia")
logger.error("Error")
```

**Ubicación de logs:**
- `~/.organizador-archivos/logs/app.log`

**Configuración:**
- `src/main.py` - función `setup_logging()`

### Common Issues

**1. FilePicker no funciona**
- Linux: Requiere Zenity (`sudo apt install zenity`)
- Verificar que se use el patrón correcto (sin overlay)

**2. Error en threading**
- Verificar que NO haya `page.run_thread` anidado
- Confirmar que se llame `page.update()` después de modificar UI

**3. Build falla**
- Verificar `pyproject.toml` tiene configuración correcta
- Ver logs con `--verbose`

**4. Window config no funciona en web**
- Agregar verificación `if not page.web:`
- Ver patrón en `src/ui/file_organizer_view.py`

### Verificación Rápida
```bash
# Verificar que todas las correcciones estén aplicadas
bash verificar_cambios.sh
```

---

## 📦 Build y Publicación

### Configuración de Build
Todo está configurado en `pyproject.toml`:

**Optimizaciones aplicadas:**
- ✅ Bytecode compilation (-50% tamaño)
- ✅ Aggressive file cleanup
- ✅ Platform-specific names
- ✅ Android permissions
- ✅ macOS entitlements

### Build Step-by-Step

**1. Verificar configuración:**
```bash
bash verificar_cambios.sh
```

**2. Primer build (Linux):**
```bash
flet build linux --verbose
```

**Resultado esperado:**
- Tamaño: ~70-100 MB (vs ~150-200 MB sin optimizaciones)
- Tiempo: 2-5 minutos
- Ejecutable: `./build/linux/organizador-archivos`

**3. Probar ejecutable:**
```bash
./build/linux/organizador-archivos
```

**4. Builds adicionales:**
```bash
# Windows
flet build windows --verbose

# macOS
flet build macos --verbose

# Web
flet build web

# Android
flet build apk

# iOS (requiere macOS)
flet build ipa
```

### Estructura de Build Output
```
build/
├── linux/
│   ├── organizador-archivos          # Ejecutable
│   └── ...
├── windows/
│   ├── OrganizadorArchivos.exe       # Ejecutable
│   └── ...
├── macos/
│   ├── OrganizadorArchivos.app       # App bundle
│   └── ...
└── web/
    ├── index.html
    └── ...
```

---

## ❓ Preguntas Frecuentes

### ¿Cómo agrego una nueva categoría de archivos?

Edita `src/config/settings.py`:

```python
class FileCategory(Enum):
    # Categorías existentes...
    MI_CATEGORIA = "Mi Categoría"  # ✅ Agregar aquí

# Y su mapeo de extensiones
FILE_EXTENSIONS = {
    FileCategory.MI_CATEGORIA: [".ext1", ".ext2"],
    # ...
}
```

### ¿Cómo cambio los colores del tema?

Edita `src/config/theme.py`:

```python
class Theme:
    BG = "#1E1E1E"          # Fondo principal
    SURFACE = "#2D2D2D"     # Superficies elevadas
    ACCENT = "#007ACC"      # Color de acento
    # ... etc
```

### ¿Cómo agrego un nuevo categorizador?

Implementa el Protocol `FileCategorizer`:

```python
from src.domain.file_categorizer import FileCategorizer

class MiCategorizador:
    def categorize(self, file_path: Path) -> str:
        # Tu lógica aquí
        return "Categoría"

# Úsalo en FileOrganizerView.__init__
categorizer = MiCategorizador()
self.org_service = OrganizationService(categorizer)
```

### ¿Cómo hago que el build sea más pequeño?

Las optimizaciones ya están aplicadas en `pyproject.toml`. Para más:

1. Desactiva módulos no usados en `exclude_patterns`
2. Considera compilar a bytecode (ya habilitado)

### ¿Dónde busco si algo no funciona en Flet?

**En este orden:**
1. https://docs.flet.dev/ - Documentación oficial
2. https://github.com/flet-dev/flet/issues - Issues conocidos
3. https://discord.gg/dzWXP8SHG8 - Discord de Flet

### ¿Cómo actualizo Flet?

```bash
pip install --upgrade flet

# Verificar versión
python -c "import flet; print(flet.__version__)"

# Actualizar pyproject.toml si hay breaking changes
```

---

## 📝 Checklist para Modificaciones

Cuando modifiques código, verifica:

- [ ] ✅ Usa patrones correctos de Flet (ver sección "Patrones Importantes")
- [ ] ✅ FilePicker sin overlay innecesario
- [ ] ✅ No anidar `page.run_thread`
- [ ] ✅ Verificar plataforma para window config
- [ ] ✅ Llamar `page.update()` después de modificar UI
- [ ] ✅ Usar async solo si haces await
- [ ] ✅ Agregar logging apropiado
- [ ] ✅ Ejecutar `bash verificar_cambios.sh`
- [ ] ✅ Probar con `flet run`

---

## 🆘 Si Estás Atascado

**1. Consulta la documentación oficial de Flet:**
- https://docs.flet.dev/

**2. Verifica que las correcciones estén aplicadas:**
```bash
bash verificar_cambios.sh
```

**3. Revisa los logs:**
```bash
tail -f ~/.organizador-archivos/logs/app.log
```

**4. Pide ayuda:**
- Discord de Flet: https://discord.gg/dzWXP8SHG8
- Stack Overflow con tag `flet`
- GitHub Issues: https://github.com/flet-dev/flet/issues

---

## 📌 TL;DR - Quick Start para LLMs

**Si necesitas trabajar con este proyecto:**

1. **Tecnología:** Flet v0.82+ (async/await, multiplataforma)
2. **Patrones críticos:**
   - FilePicker sin overlay
   - No anidar `page.run_thread`
   - Verificar plataforma para window
   - `ft.run()` no `ft.app()`
3. **Si falta contexto:** Lee docs oficiales de Flet (URLs arriba)
4. **Verificar cambios:** `bash verificar_cambios.sh`
5. **Probar:** `flet run`
6. **Build:** `flet build linux --verbose`

**Archivos más importantes:**
- `src/main.py` - Entry point
- `src/ui/file_organizer_view.py` - UI principal
- `pyproject.toml` - Config de build
- `README.md` - Documentación para usuarios

---

**Última actualización:** 2026-03-14  
**Versión Flet:** ≥0.27.0  
**Python:** ≥3.12  
**Estado:** ✅ Listo para desarrollo

