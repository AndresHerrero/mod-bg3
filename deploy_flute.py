import os
import shutil
import sys
import io
from pathlib import Path

# Forzar salida en UTF-8 para evitar errores con emojis en Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuración de rutas
MOD_DIR = Path("ThroughFireAndFlamesMod")
SOUND_DIR = MOD_DIR / "Public" / "Shared" / "Assets" / "Sound"
TEMP_DIR = Path("_temp")
SOURCE_WEM = TEMP_DIR / "flauta.wem"

# ID de Baldur's Gate 3 para: canción 'The Power' - instrumento 'Flauta'
FLUTE_WEM_ID = "247277282.wem"

def main():
    print("🎸  Iniciando despliegue de canción para flauta...")

    # Verificar que el archivo de audio existe
    if not SOURCE_WEM.exists():
        print(f"❌ ERROR: No se encuentra el archivo {SOURCE_WEM}")
        print("Asegúrate de haber puesto tu archivo .wem en la carpeta _temp con el nombre flauta.wem")
        return

    # Asegurar que la carpeta de destino existe
    SOUND_DIR.mkdir(parents=True, exist_ok=True)

    # Copiar y renombrar
    dest_path = SOUND_DIR / FLUTE_WEM_ID
    shutil.copy2(SOURCE_WEM, dest_path)

    print(f"✅ ÉXITO: Se ha copiado '{SOURCE_WEM.name}' como '{dest_path.name}'")
    print(f"📍 Ubicación: {dest_path}")
    print("\nSiguientes pasos:")
    print("1. Si tienes más canciones en la carpeta Sound, ahora esta se habrá añadido a ellas.")
    print("2. Usa BG3 Modder's Multitool para empaquetar la carpeta 'ThroughFireAndFlamesMod' en un nuevo .pak")

if __name__ == "__main__":
    main()
