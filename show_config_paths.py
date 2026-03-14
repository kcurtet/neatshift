#!/usr/bin/env python3
"""
Utility script to show platform-specific directories used by the app.
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.config.user_config import CONFIG_DIR, CONFIG_FILE, LOG_DIR


def main():
    """Display configuration and log directories."""
    print("📁 NeatShift - Directorios del Sistema")
    print("=" * 60)
    print()
    
    print("🗂️  Configuración:")
    print(f"   Directorio: {CONFIG_DIR}")
    print(f"   Archivo:    {CONFIG_FILE}")
    print(f"   Existe:     {'✅ Sí' if CONFIG_FILE.exists() else '❌ No'}")
    print()
    
    print("📝 Logs:")
    print(f"   Directorio: {LOG_DIR}")
    log_file = LOG_DIR / "app.log"
    print(f"   Archivo:    {log_file}")
    print(f"   Existe:     {'✅ Sí' if log_file.exists() else '❌ No'}")
    print()
    
    # Show platform
    import platform
    print(f"💻 Sistema:    {platform.system()} {platform.release()}")
    print(f"🐍 Python:     {platform.python_version()}")
    print()
    
    # Show config content if exists
    if CONFIG_FILE.exists():
        try:
            import json
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print("⚙️  Configuración actual:")
            print(f"   Categorías:        {len(config.get('categories', {}))}")
            print(f"   Omitir ocultos:    {config.get('skip_hidden_files', 'N/A')}")
            print(f"   Última carpeta origen: {config.get('last_source_path', 'N/A')}")
            print(f"   Última carpeta destino: {config.get('last_dest_path', 'N/A')}")
            print()
            
            # List categories
            print("   Categorías configuradas:")
            for cat_name, cat_data in config.get('categories', {}).items():
                enabled = "✅" if cat_data.get('enabled', True) else "❌"
                date_org = "📅" if cat_data.get('organize_by_date', True) else "  "
                ext_count = len(cat_data.get('extensions', []))
                regex_count = len(cat_data.get('regex_patterns', []))
                print(f"   {enabled} {date_org} {cat_name:20s} ({ext_count} ext, {regex_count} regex)")
        except Exception as e:
            print(f"   ⚠️  Error leyendo configuración: {e}")
    
    print()
    print("Para borrar la configuración:")
    print(f"   rm -rf {CONFIG_DIR}")
    print()


if __name__ == "__main__":
    main()
