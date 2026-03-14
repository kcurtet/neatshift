# 📁 Organizador de Archivos

Aplicación multiplataforma para organizar archivos automáticamente por categoría y fecha.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Flet](https://img.shields.io/badge/Flet-0.27+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Características

- **Organización automática** por tipo de archivo (Documentos, Imágenes, Videos, Audio, etc.)
- **Estructura por fecha** (YYYY/MM) basada en fecha de modificación
- **Vista previa** antes de mover archivos
- **Barra de progreso** en tiempo real
- **Interfaz moderna** con tema oscuro
- **Multiplataforma**: Windows, macOS, Linux, Web, Android, iOS

## 📸 Capturas

```
┌─────────────────────────────────────────────────────────────┐
│ 📁 Organizador de Archivos                                  │
├─────────────────────────────────────────────────────────────┤
│ Carpeta de origen:    [/home/user/Downloads    ] [Examinar] │
│ Carpeta de destino:   [/home/user/Organized    ] [Examinar] │
│                                                              │
│ [Vista previa] [Aplicar cambios] [Limpiar]                  │
│                                                              │
│ 📊 Documentos 15  🖼️ Imágenes 8  🎵 Audio 3                │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Archivo        Categoría    Fecha    Destino             │ │
│ │ documento.pdf  Documentos   2024/03  /Organized/Docs/... │ │
│ │ foto.jpg       Imágenes     2024/03  /Organized/Pics/... │ │
│ │ ...                                                       │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 75%   │
│ Moviendo archivos... (12/16)                                │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Instalación

### Desde código fuente

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/file-organizer.git
cd file-organizer

# Instalar dependencias
pip install flet

# Ejecutar
flet run
```

### Build ejecutable

```bash
# Linux
flet build linux

# Windows
flet build windows

# macOS
flet build macos

# Web
flet build web

# Android
flet build apk

# iOS
flet build ipa
```

Ejecutables disponibles en `build/`.

## 🎯 Uso

1. **Selecciona carpeta origen**: Donde están los archivos desordenados
2. **Selecciona carpeta destino**: Donde se organizarán los archivos
3. **Vista previa**: Revisa cómo se organizarán los archivos
4. **Aplicar cambios**: Confirma y mueve los archivos

### Estructura de salida

```
Carpeta_Destino/
├── Documentos/
│   ├── 2024/
│   │   ├── 01/
│   │   │   ├── contrato.pdf
│   │   │   └── reporte.docx
│   │   └── 02/
│   │       └── presupuesto.xlsx
├── Imágenes/
│   └── 2024/
│       └── 03/
│           ├── foto1.jpg
│           └── foto2.png
└── Videos/
    └── 2024/
        └── 03/
            └── video.mp4
```

## 📋 Categorías soportadas

| Categoría | Extensiones |
|-----------|-------------|
| **Documentos** | `.pdf`, `.doc`, `.docx`, `.txt`, `.odt`, `.rtf`, `.tex`, `.wpd`, `.xlsx`, `.xls`, `.csv`, `.ppt`, `.pptx` |
| **Imágenes** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`, `.ico`, `.tiff`, `.psd`, `.ai`, `.raw`, `.heic` |
| **Videos** | `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v`, `.mpg`, `.mpeg` |
| **Audio** | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a`, `.opus`, `.alac` |
| **Archivos Comprimidos** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`, `.xz`, `.iso` |
| **Código** | `.py`, `.js`, `.ts`, `.java`, `.cpp`, `.c`, `.h`, `.cs`, `.php`, `.rb`, `.go`, `.rs`, `.swift` |
| **Ejecutables** | `.exe`, `.msi`, `.app`, `.deb`, `.rpm`, `.apk`, `.dmg` |
| **Otros** | Cualquier extensión no categorizada |

## ⚙️ Configuración

Edita `src/config/settings.py` para personalizar:

- Categorías y extensiones
- Tamaño de ventana
- Colores del tema (en `src/config/theme.py`)

## 🛠️ Desarrollo

### Requisitos

- Python 3.12+
- Flet 0.27+

### Estructura del proyecto

```
file-organizer/
├── src/
│   ├── main.py              # Punto de entrada
│   ├── assets/              # Iconos y recursos
│   ├── config/              # Configuración
│   ├── domain/              # Lógica de negocio
│   ├── services/            # Servicios
│   └── ui/                  # Interfaz de usuario
├── pyproject.toml           # Configuración del proyecto
└── README.md
```

### Ejecutar en modo desarrollo

```bash
flet run
```

### Testing

```bash
# Verificar código
bash verificar_cambios.sh

# Probar app
bash test_app.sh --run
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👤 Autor

**Kevin Curtet**
- Email: kcurtet@gmail.com

## 🐛 Reportar problemas

Si encuentras algún bug o tienes sugerencias, por favor abre un [issue](https://github.com/tu-usuario/file-organizer/issues).

## ⭐ Agradecimientos

- [Flet](https://flet.dev/) - Framework UI multiplataforma
- Comunidad Python

---

**¿Te gusta este proyecto?** ¡Dale una ⭐ en GitHub!
