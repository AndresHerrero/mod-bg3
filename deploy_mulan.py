import os
import shutil
import subprocess
from pathlib import Path

# Paths
MOD_DIR = Path("ThroughFireAndFlamesMod")
SOUND_DIR = MOD_DIR / "Public" / "ThroughFireAndFlames" / "Assets" / "Sound"
TEMP_DIR = Path("_temp")
WEM_FILE = TEMP_DIR / "con_valor.wem"
BUILD_DIR = Path("_build")
OUTPUT_PAK = BUILD_DIR / "ThroughFireAndFlames.pak"
DIVINE_EXE = Path("tools/Packed/Tools/Divine.exe")

# BG3 IDs for 'Bard Dance'
BARD_DANCE_IDS = {
    "drum": 91256288,
    "flute": 98035890,
    "lute": 582548246,
    "lyre": 340373265,
    "violin": 958425049,
    "whistle": 824207806
}

def main():
    if not WEM_FILE.exists():
        print(f"❌ ERROR: No se encuentra {WEM_FILE}")
        print("Recuerda que debes generar el .wem con Wwise a partir de con_valor.wav")
        return

    SOUND_DIR.mkdir(parents=True, exist_ok=True)

    print("🎙️  Copiando 'Con Valor' sobre 'Bard Dance'...")
    for instrument, wem_id in BARD_DANCE_IDS.items():
        dest = SOUND_DIR / f"{wem_id}.wem"
        shutil.copy2(WEM_FILE, dest)
        print(f"  ✅ {instrument:8s} -> {dest.name}")

    if DIVINE_EXE.exists():
        print("\n📦 Empaquetando nuevo mod (.pak)...")
        BUILD_DIR.mkdir(parents=True, exist_ok=True)
        cmd = [
            str(DIVINE_EXE),
            "--action", "create-package",
            "--source", str(MOD_DIR),
            "--destination", str(OUTPUT_PAK),
            "--compression-method", "None"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"🎉 ¡Mod empaquetado con éxito en: {OUTPUT_PAK}!")
            print("Importa este nuevo .zip/.pak en tu BG3 Mod Manager para actualizarlo.")
        else:
            print("⚠️ Error al empaquetar:", res.stderr)
    else:
        print("\n⚠️ No se ha encontrado divine.exe automático.")
        print("Arrastra la carpeta ThroughFireAndFlamesMod al BG3 Modders Multitool para empaquetarlo de nuevo.")

if __name__ == "__main__":
    main()
