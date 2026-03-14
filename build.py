#!/usr/bin/env python3
"""
Build script para Organizador de Archivos

Uso:
    uv run python build.py [plataforma]

Plataformas disponibles:
    - windows (por defecto si estás en Windows)
    - linux (por defecto si estás en Linux)
    - macos (por defecto si estás en macOS)

Para builds multiplataforma, usa GitHub Actions:
    git push origin main
"""

import subprocess
import sys
import platform
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
BUILD_DIR = ROOT / "build"


def clean_build_artifacts():
    """Remove previous build artifacts."""
    print("🧹 Limpiando builds anteriores...")
    
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    
    print("   ✅ Listo\n")


def detect_platform():
    """Detecta la plataforma nativa."""
    system = platform.system()
    platform_map = {
        "Linux": "linux",
        "Windows": "windows", 
        "Darwin": "macos"
    }
    return platform_map.get(system, system.lower())


def build_executable(target_platform: str):
    """Build the executable using flet build."""
    current_platform = detect_platform()
    
    if target_platform != current_platform:
        print(f"⚠️  Advertencia: Estás en {current_platform} pero intentas construir para {target_platform}")
        print(f"   Los builds cross-platform no están soportados por flet build.")
        print(f"   Construyendo para {current_platform} en su lugar...\n")
        target_platform = current_platform
    
    print(f"🔨 Construyendo para {target_platform}...")
    print()
    
    cmd = [
        "flet", "build", target_platform,
        "--yes",
        "--verbose"
    ]
    
    result = subprocess.run(cmd, cwd=ROOT)
    return result.returncode


def verify_output(target_platform: str):
    """Verify that the executable was created successfully."""
    # flet build crea el output en build/{platform}/
    platform_output = BUILD_DIR / target_platform
    
    if not platform_output.exists():
        print(f"\n❌ Build falló!")
        print(f"   No se encontró: {platform_output}\n")
        return False
    
    # Buscar el ejecutable/binario
    if target_platform == "windows":
        exe_pattern = "*.exe"
    elif target_platform == "macos":
        exe_pattern = "*.app"
    else:  # linux
        exe_pattern = "*"
    
    executables = list(platform_output.glob(exe_pattern))
    
    if not executables:
        print(f"\n❌ Build falló!")
        print(f"   No se encontraron ejecutables en: {platform_output}\n")
        return False
    
    # Calcular tamaño total
    total_size = sum(f.stat().st_size for f in platform_output.rglob("*") if f.is_file())
    size_mb = total_size / (1024 * 1024)
    
    print("\n" + "="*70)
    print("✅ Build exitoso!")
    print("="*70)
    print(f"\n📦 Directorio: {platform_output}")
    print(f"📊 Tamaño total: {size_mb:.1f} MB")
    print(f"🎯 Plataforma: {target_platform}\n")
    
    print("💡 Para builds multiplataforma, usa GitHub Actions:")
    print("   git push origin main\n")
    
    return True


def main():
    """Main build process."""
    print("="*70)
    print("Organizador de Archivos - Build")
    print("="*70)
    print(f"Sistema actual: {platform.system()}")
    print()
    
    # Determinar plataforma target
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()
        if target not in ["windows", "linux", "macos"]:
            print(f"❌ Plataforma no válida: {target}")
            print("   Plataformas válidas: windows, linux, macos\n")
            sys.exit(1)
    else:
        target = detect_platform()
    
    print(f"🎯 Plataforma objetivo: {target}\n")
    
    # Clean
    clean_build_artifacts()
    
    # Build
    returncode = build_executable(target)
    
    if returncode != 0:
        print("\n❌ El build falló. Revisa los errores arriba.")
        sys.exit(1)
    
    # Verify
    if not verify_output(target):
        sys.exit(1)


if __name__ == "__main__":
    main()
