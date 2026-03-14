#!/bin/bash
# Script de prueba rápida del Organizador de Archivos
# Verifica que las correcciones de Flet funcionen correctamente

set -e

echo "🧪 Prueba Rápida - Organizador de Archivos"
echo "=========================================="
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Error: No se encuentra pyproject.toml${NC}"
    echo "Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

echo -e "${YELLOW}📋 Verificando dependencias...${NC}"

# Verificar que flet esté instalado
if ! python3 -c "import flet" 2>/dev/null; then
    echo -e "${RED}❌ Flet no está instalado${NC}"
    echo "Instala con: pip install flet"
    exit 1
fi

# Obtener versión de Flet
FLET_VERSION=$(python3 -c "import flet; print(flet.__version__)" 2>/dev/null)
echo -e "${GREEN}✅ Flet ${FLET_VERSION} instalado${NC}"

# Verificar que la estructura sea correcta
echo ""
echo -e "${YELLOW}📂 Verificando estructura del proyecto...${NC}"

required_files=(
    "src/main.py"
    "src/ui/file_organizer_view.py"
    "src/config/settings.py"
    "src/config/theme.py"
    "src/services/organization_service.py"
    "src/domain/file_categorizer.py"
)

all_ok=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ $file (faltante)${NC}"
        all_ok=false
    fi
done

if [ "$all_ok" = false ]; then
    echo ""
    echo -e "${RED}❌ Faltan archivos requeridos${NC}"
    exit 1
fi

# Verificar que los cambios de Flet estén aplicados
echo ""
echo -e "${YELLOW}🔍 Verificando correcciones de Flet...${NC}"

# 1. Verificar ft.run() en lugar de ft.app()
if grep -q "ft.run(target=main)" src/main.py; then
    echo -e "${GREEN}✅ ft.run() (API moderna)${NC}"
else
    echo -e "${RED}❌ No se encontró ft.run() en main.py${NC}"
    all_ok=false
fi

# 2. Verificar que FilePicker no agregue al overlay innecesariamente
if ! grep -q "self.page.overlay.append(picker)" src/ui/file_organizer_view.py; then
    echo -e "${GREEN}✅ FilePicker simplificado (sin overlay innecesario)${NC}"
else
    echo -e "${RED}❌ FilePicker todavía agrega al overlay${NC}"
    all_ok=false
fi

# 3. Verificar que no haya page.run_thread anidado
if ! grep -q "self.page.run_thread(lambda: self.display_plan" src/ui/file_organizer_view.py; then
    echo -e "${GREEN}✅ page.run_thread no anidado${NC}"
else
    echo -e "${RED}❌ Todavía hay page.run_thread anidado${NC}"
    all_ok=false
fi

# 4. Verificar verificación de plataforma
if grep -q "if not self.page.web:" src/ui/file_organizer_view.py; then
    echo -e "${GREEN}✅ Verificación de plataforma agregada${NC}"
else
    echo -e "${YELLOW}⚠️  No se encontró verificación de plataforma${NC}"
fi

echo ""
if [ "$all_ok" = true ]; then
    echo -e "${GREEN}✅ Todas las correcciones están aplicadas${NC}"
else
    echo -e "${RED}❌ Algunas correcciones faltan${NC}"
    exit 1
fi

# Intentar ejecutar la app (solo si se pasa --run)
if [ "$1" = "--run" ]; then
    echo ""
    echo -e "${YELLOW}🚀 Ejecutando aplicación...${NC}"
    echo "(Presiona Ctrl+C para detener)"
    echo ""
    sleep 2
    flet run
else
    echo ""
    echo -e "${YELLOW}💡 Para ejecutar la app:${NC}"
    echo "   ./test_app.sh --run"
    echo "   o"
    echo "   flet run"
fi

echo ""
echo -e "${GREEN}✅ Verificación completada${NC}"

