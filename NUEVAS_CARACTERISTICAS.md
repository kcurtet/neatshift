# Organizador de Archivos - Nuevas Características

## Sistema de Pestañas (Tabs)

La aplicación ahora cuenta con una interfaz de pestañas que separa las funciones principales:

### 1. Pestaña "Organizador"
- Interfaz original para organizar archivos
- Selección de carpetas origen/destino
- Vista previa de organización
- Progreso en tiempo real
- Resumen por categorías

### 2. Pestaña "Configuración"
- Gestión completa de categorías
- Configuración de filtros personalizados
- Opciones avanzadas de organización

## Gestión de Categorías

### Crear Categoría Personalizada
1. Ve a la pestaña "Configuración"
2. Haz clic en "Nueva categoría"
3. Define nombre y extensiones iniciales

### Editar Filtros por Categoría

Cada categoría soporta dos tipos de filtros:

#### **Filtros por Extensión**
```
.jpg, .png, .gif, .webp
```
- Separados por comas
- El punto (.) es opcional, se añade automáticamente
- No sensible a mayúsculas

#### **Filtros por Regex**
```
^backup_.*\.txt$
report_\d{4}_\d{2}_\d{2}.*
IMG_\d{8}_\d{6}\.jpg
```
- Un patrón por línea
- Útiles para:
  - Archivos con fechas en el nombre
  - Prefijos/sufijos específicos
  - Patrones numéricos
  - Nombres complejos

### Ejemplos de Patrones Regex Útiles

| Patrón | Descripción | Ejemplo de archivo |
|--------|-------------|-------------------|
| `^backup_.*` | Archivos que empiezan con "backup_" | backup_2024.zip |
| `.*_\d{4}\.pdf$` | PDFs que terminan con año | report_2024.pdf |
| `IMG_\d{8}.*` | Fotos con fecha YYYYMMDD | IMG_20240315_142530.jpg |
| `^[A-Z]{2,3}_\d+` | Códigos + número | ABC_12345.doc |
| `(factura|invoice).*` | Facturas en español/inglés | factura_enero.pdf |

## Organización por Fecha

### Activar/Desactivar por Categoría

Cada categoría puede configurarse independientemente:

- **Activado**: Crea subcarpetas `YYYY/MM` (ejemplo: `2024/03`)
- **Desactivado**: Archivos directamente en la carpeta de categoría

**Ejemplo con fecha activada:**
```
Destino/
  ├── Documentos/
  │   ├── 2024/
  │   │   ├── 01/
  │   │   │   └── factura.pdf
  │   │   └── 03/
  │   │       └── contrato.pdf
```

**Ejemplo con fecha desactivada:**
```
Destino/
  ├── Documentos/
  │   ├── factura.pdf
  │   └── contrato.pdf
```

### Casos de Uso

**Con organización por fecha:**
- ✅ Fotos y vídeos (organizados cronológicamente)
- ✅ Documentos frecuentes
- ✅ Backups

**Sin organización por fecha:**
- ✅ Archivos de código (mejor por proyecto)
- ✅ Música (mejor por artista/álbum)
- ✅ Categorías con pocos archivos

## Opciones Globales

### Omitir Archivos Ocultos
- **Activado**: Ignora archivos y carpetas que empiezan con `.`
- **Desactivado**: Procesa todos los archivos

Útil para:
- Evitar archivos de sistema (`.DS_Store`, `.git`, etc.)
- Procesar configuraciones ocultas si es necesario

## Persistencia de Configuración

La configuración se guarda automáticamente en:
```
~/.organizador-archivos/config.json
```

Incluye:
- Categorías personalizadas
- Filtros (extensiones y regex)
- Opciones de organización por fecha
- Última carpeta origen/destino usada
- Preferencias globales

## Flujo de Trabajo Recomendado

### Primera Vez
1. **Ir a Configuración**
   - Revisar categorías predeterminadas
   - Añadir categorías personalizadas si es necesario
   - Configurar filtros regex para casos especiales

2. **Configurar Organización por Fecha**
   - Activar para fotos, vídeos, documentos
   - Desactivar para código, música

3. **Probar con Vista Previa**
   - Ir a pestaña "Organizador"
   - Seleccionar carpeta de prueba
   - Verificar que la organización sea correcta

### Uso Regular
1. Seleccionar carpeta origen y destino
2. Hacer clic en "Vista previa"
3. Revisar la tabla de archivos
4. Aplicar cambios si todo está correcto

## Tips y Trucos

### Categorías Múltiples para Mismo Archivo
Si un archivo coincide con múltiples categorías, se usa la **primera coincidencia** en orden alfabético de categoría.

### Testing de Patrones Regex
Usa https://regex101.com/ para probar tus patrones antes de añadirlos.

### Backup Antes de Organizar
Siempre haz backup de tus archivos importantes antes de ejecutar la organización masiva.

### Performance
- La app usa multi-threading para operaciones I/O
- En Windows, usa CopyFile2 API nativa para mejor rendimiento
- Auto-detecta operaciones cross-drive y ajusta workers

## Troubleshooting

### Los archivos no aparecen en la categoría esperada
1. Verifica que la categoría esté **activada** (switch verde)
2. Revisa que las extensiones incluyan el punto (`.jpg` no `jpg`)
3. Si usas regex, prueba el patrón en regex101.com
4. Recuerda que se usa la primera categoría que coincida

### Patrones regex no funcionan
1. Verifica la sintaxis del patrón
2. Los patrones son case-insensitive por defecto
3. Usa `^` para inicio de nombre y `$` para final
4. Escapa caracteres especiales: `\.` para punto literal

### La configuración no se guarda
1. Verifica permisos de escritura en `~/.organizador-archivos/`
2. Revisa los logs en `~/.organizador-archivos/logs/app.log`

## Arquitectura Técnica

```
src/
├── config/
│   ├── settings.py              # Configuración estática
│   ├── theme.py                 # Tema visual
│   └── user_config.py           # Configuración persistente (NUEVO)
├── domain/
│   ├── categorizer.py           # Categorizador por defecto
│   ├── configurable_categorizer.py  # Categorizador configurable (NUEVO)
│   └── file_item.py             # Modelo de datos
├── services/
│   ├── organization_service.py  # Lógica de organización
│   └── file_service.py          # Operaciones de archivos
└── ui/
    ├── file_organizer_view.py   # Vista original (legacy)
    ├── tabbed_view.py           # Vista con tabs (NUEVO)
    └── settings_view.py         # Vista de configuración (NUEVO)
```

### Cambios Principales

1. **UserConfig**: Modelo de configuración persistente con soporte JSON
2. **CategoryConfig**: Configuración por categoría (extensiones, regex, fecha)
3. **ConfigurableFileCategorizer**: Categorizador que usa UserConfig
4. **FileOrganizerApp**: Vista principal con tabs
5. **SettingsView**: Interfaz de configuración completa

### Backward Compatibility

El código mantiene compatibilidad con `DefaultFileCategorizer`:
- OrganizationService acepta ambos tipos de categorizadores
- Los resultados de categorización soportan tanto `FileCategory` como `tuple[str, bool]`

## Próximas Mejoras Sugeridas

- [ ] Importar/exportar configuración
- [ ] Plantillas de configuración predefinidas
- [ ] Vista previa de regex en tiempo real
- [ ] Estadísticas de uso por categoría
- [ ] Historial de organizaciones
- [ ] Modo "dry run" con log detallado
- [ ] Soporte para categorización por contenido (MIME type)
- [ ] Reglas de conflicto de nombres personalizables
