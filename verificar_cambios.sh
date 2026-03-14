#!/usr/bin/env bash
# Verificación rápida de correcciones Flet (sin imports de Python)

echo "🔍 Verificación de Correcciones Flet"
echo "===================================="
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

all_ok=true

# 1. Verificar ft.run() en lugar de ft.app()
echo -n "1. ft.run() en lugar de ft.app()... "
if grep -q "ft.run(target=main)" src/main.py; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${RED}❌${NC}"
    all_ok=false
fi

# 2. Verificar que FilePicker no agregue al overlay innecesariamente  
echo -n "2. FilePicker simplificado... "
if ! grep -q "self.page.overlay.append(picker)" src/ui/file_organizer_view.py; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${RED}❌${NC}"
    all_ok=false
fi

# 3. Verificar que no haya page.run_thread anidado
echo -n "3. page.run_thread no anidado... "
if ! grep -q "self.page.run_thread(lambda: self.display_plan" src/ui/file_organizer_view.py; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${RED}❌${NC}"
    all_ok=false
fi

# 4. Verificar verificación de plataforma
echo -n "4. Verificación de plataforma... "
if grep -q "if not self.page.web:" src/ui/file_organizer_view.py; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${YELLOW}⚠️${NC}"
fi

# 5. Verificar comentarios thread-safe
echo -n "5. Comentarios de thread-safety... "
if grep -q "page.update() is thread-safe" src/ui/file_organizer_view.py; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${YELLOW}⚠️${NC}"
fi

echo ""
if [ "$all_ok" = true ]; then
    echo -e "${GREEN}✅ Todas las correcciones críticas están aplicadas${NC}"
    exit 0
else
    echo -e "${RED}❌ Algunas correcciones críticas faltan${NC}"
    exit 1
fi

