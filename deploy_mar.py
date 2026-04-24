import os
import shutil
import subprocess
from pathlib import Path

# Paths
MOD_DIR = Path("ThroughFireAndFlamesMod")
SOUND_DIR = MOD_DIR / "Public" / "Shared" / "Assets" / "Sound"
TEMP_DIR = Path("_temp")
WEM_FILE = TEMP_DIR / "bajo_el_mar.wem"
BUILD_DIR = Path("_build")
OUTPUT_PAK = BUILD_DIR / "ThroughFireAndFlames.pak"
DIVINE_EXE = Path("tools/Packed/Tools/Divine.exe")

# BG3 IDs for 'Old Time Battles'
OLD_TIME_BATTLES_IDS = {
    "drum": 1032011443,
    "flute": 688689226,
    "lute": 88231746,
    "lyre": 160641375,
    "violin": 107779537,
    "whistle": 549395448
}

def main():
    if not WEM_FILE.exists():
        print(f"❌ ERROR: No se encuentra {WEM_FILE}")
        print("Recuerda que debes generar el .wem con Wwise a partir de bajo_el_mar.wav")
        return

    SOUND_DIR.mkdir(parents=True, exist_ok=True)

    print("🦀  Copiando 'Bajo el mar' sobre 'Old Time Battles'...")
    for instrument, wem_id in OLD_TIME_BATTLES_IDS.items():
        dest = SOUND_DIR / f"{wem_id}.wem"
        shutil.copy2(WEM_FILE, dest)
        print(f"  ✅ {instrument:8s} -> {dest.name}")

    print("\n✅ Archivos desplegados en la carpeta del mod.")
    print("Siguiente paso: Arrastra la carpeta 'ThroughFireAndFlamesMod' al BG3 Modders Multitool para empaquetarlo.")

if __name__ == "__main__":
    main()
