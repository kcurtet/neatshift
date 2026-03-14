# Directorios de Configuración por Plataforma

El Organizador de Archivos usa directorios estándar según el sistema operativo donde se ejecuta, gracias a la biblioteca `platformdirs`.

## 🐧 Linux (XDG Base Directory)

### Configuración
```bash
~/.config/organizador-archivos/
└── config.json
```

### Logs
```bash
~/.local/state/organizador-archivos/log/
└── app.log
```

### Variables de entorno
Puedes personalizar estas ubicaciones con:
- `XDG_CONFIG_HOME` - Directorio de configuración (default: `~/.config`)
- `XDG_STATE_HOME` - Directorio de estado/logs (default: `~/.local/state`)

## 🍎 macOS

### Configuración
```bash
~/Library/Application Support/organizador-archivos/
└── config.json
```

### Logs
```bash
~/Library/Logs/organizador-archivos/
└── app.log
```

## 🪟 Windows

### Configuración
```
%APPDATA%\organizador-archivos\
└── config.json
```
Ejemplo: `C:\Users\TuUsuario\AppData\Roaming\organizador-archivos\`

### Logs
```
%LOCALAPPDATA%\organizador-archivos\log\
└── app.log
```
Ejemplo: `C:\Users\TuUsuario\AppData\Local\organizador-archivos\log\`

## 📱 Android/iOS (futuro)

Cuando se compile para móvil, usará los directorios apropiados de cada plataforma automáticamente.

## 🔍 Ver Rutas Actuales

Ejecuta este script para ver las rutas específicas en tu sistema:

```bash
python show_config_paths.py
```

O con el venv:
```bash
.venv/bin/python show_config_paths.py
```

Salida de ejemplo (Linux):
```
📁 Organizador de Archivos - Directorios del Sistema
============================================================

🗂️  Configuración:
   Directorio: /home/usuario/.config/organizador-archivos
   Archivo:    /home/usuario/.config/organizador-archivos/config.json
   Existe:     ✅ Sí

📝 Logs:
   Directorio: /home/usuario/.local/state/organizador-archivos/log
   Archivo:    /home/usuario/.local/state/organizador-archivos/log/app.log
   Existe:     ✅ Sí

💻 Sistema:    Linux 6.18.13
🐍 Python:     3.13.12

⚙️  Configuración actual:
   Categorías:        8
   Omitir ocultos:    True
   ...
```

## 🗑️ Limpiar Configuración

### Linux/macOS
```bash
rm -rf ~/.config/organizador-archivos
rm -rf ~/.local/state/organizador-archivos  # Linux
rm -rf ~/Library/Logs/organizador-archivos  # macOS
```

### Windows (PowerShell)
```powershell
Remove-Item -Recurse -Force "$env:APPDATA\organizador-archivos"
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\organizador-archivos"
```

## 🔧 Dependencias

La ubicación de directorios se gestiona con:
- **[platformdirs](https://github.com/platformdirs/platformdirs)** - Biblioteca multiplataforma para directorios de usuario

Instalada automáticamente con:
```bash
uv pip install -r pyproject.toml
```

## 📚 Referencias

- **XDG Base Directory** (Linux): https://specifications.freedesktop.org/basedir-spec/latest/
- **Apple File System** (macOS): https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/
- **Known Folders** (Windows): https://learn.microsoft.com/en-us/windows/win32/shell/known-folders
