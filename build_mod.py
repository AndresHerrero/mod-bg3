"""
=============================================================================
  Through the Fire and Flames - BG3 Bard Mod Audio Converter
  ============================================================================
  This script automates the full pipeline to prepare your custom bard music
  for Baldur's Gate 3:
  
    1. Downloads "Through the Fire and Flames" audio via yt-dlp
    2. Converts it to .wav using FFmpeg
    3. Converts .wav to .wem using Wwise (if installed) OR uses the
       community-maintained wwiser/vgmstream approach
    4. Renames and copies .wem files to the correct mod folder
  
  REQUIREMENTS (install before running):
    - Python 3.8+ : https://python.org
    - FFmpeg       : https://ffmpeg.org/download.html
    - yt-dlp       : pip install yt-dlp
    - Wwise        : https://www.audiokinetic.com/en/products/wwise/ 
                     (Free for indie; install the Wwise SDK 2019.x for BG3)

  HOW TO RUN:
    python build_mod.py

  QUICK MODE (if you already have the .wav file):
    Place your .wav file as "through_fire_flames.wav" in this folder,
    then run: python build_mod.py --skip-download
=============================================================================
"""

import os
import sys
import io
import shutil
import subprocess
import argparse
import json
from pathlib import Path

# Force UTF-8 output on Windows so Unicode chars print correctly
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ─────────────────────────────────────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR   = Path(__file__).parent.resolve()
MOD_DIR      = SCRIPT_DIR / "ThroughFireAndFlamesMod"
SOUND_DIR    = MOD_DIR / "Public" / "Shared" / "Assets" / "Sound"
BUILD_DIR    = SCRIPT_DIR / "_build"
TEMP_DIR     = SCRIPT_DIR / "_temp"

SONG_URL     = "https://www.youtube.com/watch?v=kGnjrTkv1gs"   # DragonForce - TTFAF (official)
WAV_FILE     = TEMP_DIR / "through_fire_flames.wav"
WEM_FILE     = TEMP_DIR / "through_fire_flames.wem"

# ─────────────────────────────────────────────────────────────────────────────
#  WEM FILE IDs FOR EACH BARD SONG + INSTRUMENT
#  Source: BG3 community modding wiki & Reddit research
# ─────────────────────────────────────────────────────────────────────────────

WEM_IDS = {
    "The Power (MAIN TARGET)": {
        "drum":   264861677,
        "flute":  247277282,
        "lute":   230164766,
        "lyre":   182777796,
        "violin": 470306917,
        # No whistle for The Power
    },
    "Bard Dance": {
        "drum":    91256288,
        "flute":   98035890,
        "lute":   582548246,
        "lyre":   340373265,
        "violin": 958425049,
        "whistle": 824207806,
    },
    "Of Divinity and Sin": {
        "drum":    575371427,
        "flute":   591535284,
        "lute":   1006554640,
        "lyre":    282455428,
        "violin":   93950250,
        "whistle": 454628062,
    },
    "Old Time Battles": {
        "drum":   1032011443,
        "flute":   688689226,
        "lute":    88231746,
        "lyre":   160641375,
        "violin": 107779537,
        "whistle": 549395448,
    },
    "Sing For Me": {
        "drum":   638547722,
        "flute":  734862967,
        "lute":   242730486,
        "lyre":   214215821,
        "violin":  43926257,
        "whistle": 319298902,
    },
    "The Queen's High Sea": {
        "drum":    712621309,
        "flute":   172278436,
        "lute":    801458525,
        "lyre":    351453867,
        "violin":  813458288,
        "whistle": 1004988978,
    },
}

# ─────────────────────────────────────────────────────────────────────────────
#  UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def banner(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def refresh_path():
    """Refresh PATH from registry so newly installed tools are found."""
    import winreg
    try:
        paths = []
        for scope in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            try:
                key = winreg.OpenKey(scope, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment" if scope == winreg.HKEY_LOCAL_MACHINE else r"Environment")
                val, _ = winreg.QueryValueEx(key, "Path")
                paths.append(val)
            except Exception:
                pass
        os.environ["PATH"] = ";".join(paths) + ";" + os.environ.get("PATH", "")
    except Exception:
        pass


def check_tool(name, cmd):
    """Return True if a command-line tool is available."""
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def require_tools():
    """Check all required tool availability and report."""
    banner("Checking required tools")
    refresh_path()   # pick up winget-installed tools
    all_ok = True

    tools = [
        ("Python/yt-dlp", [sys.executable, "-m", "yt_dlp", "--version"]),
        ("ffmpeg",        ["ffmpeg", "-version"]),
    ]
    for name, cmd in tools:
        ok = check_tool(name, cmd)
        status = "✅ Found" if ok else "❌ Missing"
        print(f"  {status}: {name}")
        if not ok:
            all_ok = False

    if not all_ok:
        print("\n  Please install missing tools before continuing.")
        print("  See INSTALLATION_GUIDE.md for download links.")
        sys.exit(1)
    print()

# ─────────────────────────────────────────────────────────────────────────────
#  STEP 1: DOWNLOAD AUDIO VIA yt-dlp
# ─────────────────────────────────────────────────────────────────────────────

def find_node():
    """Return path to node.exe if installed, else None."""
    for candidate in ["node", "node.exe"]:
        try:
            r = subprocess.run([candidate, "--version"], capture_output=True, timeout=5)
            if r.returncode == 0:
                return candidate
        except FileNotFoundError:
            pass
    return None


def download_audio():
    banner("Step 1: Downloading audio from YouTube")
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    temp_mp3 = TEMP_DIR / "through_fire_flames.mp3"
    if temp_mp3.exists():
        print("  MP3 already downloaded, skipping.")
    else:
        # Build base yt-dlp command
        base_cmd = [
            sys.executable, "-m", "yt_dlp",
            "-x", "--audio-format", "mp3",
            "--audio-quality", "0",
            "--geo-bypass",                  # bypass geo-restrictions
            "--no-playlist",
            "-o", str(TEMP_DIR / "through_fire_flames.%(ext)s"),
        ]

        # Add Node.js runtime if available (needed for some YouTube formats)
        node = find_node()
        if node:
            base_cmd += ["--js-runtimes", "nodejs"]
            print(f"  Node.js found: JS runtime enabled")
        else:
            print("  Note: Node.js not found. Trying without JS runtime.")
            print("  Tip: Install Node.js from https://nodejs.org for best results.")

        # List of URLs to try in order (direct → fallback search)
        urls_to_try = [
            SONG_URL,
            "https://www.youtube.com/watch?v=4JDNUMVf2gU",  # alt upload
            "ytsearch1:DragonForce Through the Fire and Flames official audio",
        ]

        success = False
        for url in urls_to_try:
            print(f"  Trying: {url}")
            cmd = base_cmd + [url]
            result = subprocess.run(cmd)
            if result.returncode == 0 and temp_mp3.exists():
                print("  Download complete.")
                success = True
                break
            print(f"  Failed, trying next source...")

        if not success:
            print()
            print("  !! AUTOMATIC DOWNLOAD FAILED !!")
            print("  YouTube is blocking this song in your region (WMG copyright).")
            print()
            print("  MANUAL OPTION: Provide the audio yourself:")
            print(f"    1. Find 'Through the Fire and Flames' audio (MP3 or WAV)")
            print(f"    2. Save it as: {temp_mp3}")
            print(f"       OR as:     {WAV_FILE}")
            print(f"    3. Re-run: py build_mod.py --skip-download")
            print()
            print("  Sources you can try manually:")
            print("    - Spotify / Apple Music (then convert to MP3 with a converter)")
            print("    - You already own the CD/digital copy")
            raise SystemExit(1)

    # Convert MP3 -> WAV (16-bit, 48000 Hz, stereo — matches BG3 WEM spec)
    if WAV_FILE.exists():
        print("  WAV already exists, skipping conversion.")
    else:
        print("  Converting MP3 → WAV (48000 Hz, stereo, 16-bit)...")
        cmd = [
            "ffmpeg", "-i", str(temp_mp3),
            "-ar", "48000",
            "-ac", "2",
            "-sample_fmt", "s16",
            str(WAV_FILE)
        ]
        subprocess.run(cmd, check=True)
        print("  ✅ WAV conversion complete.")

# ─────────────────────────────────────────────────────────────────────────────
#  STEP 2: CONVERT WAV → WEM
#  BG3 uses Wwise Vorbis encoding. This step requires Audiokinetic Wwise.
#  We call the Wwise CLI (WwiseCLI.exe) in batch conversion mode.
# ─────────────────────────────────────────────────────────────────────────────

def find_wwise_cli():
    """Search common Wwise install locations for WwiseCLI.exe"""
    common_paths = [
        Path("C:/Program Files (x86)/Audiokinetic/Wwise 2019.2.15.7416/Authoring/x64/Release/bin/WwiseCLI.exe"),
        Path("C:/Program Files (x86)/Audiokinetic/Wwise 2021.1.14.8108/Authoring/x64/Release/bin/WwiseCLI.exe"),
        Path("C:/Program Files (x86)/Audiokinetic/Wwise 2023.1.4.8496/Authoring/x64/Release/bin/WwiseCLI.exe"),
    ]
    # Also check env variable
    env_wwise = os.environ.get("WWISECLI_PATH")
    if env_wwise:
        common_paths.insert(0, Path(env_wwise))

    for p in common_paths:
        if p.exists():
            return p
    return None

def create_wwise_project():
    """Create a minimal Wwise project XML for batch WEM conversion."""
    wwise_proj_dir = TEMP_DIR / "WwiseProject"
    wwise_proj_dir.mkdir(parents=True, exist_ok=True)
    
    # Minimal Wwise project file
    proj_content = """<?xml version="1.0" encoding="UTF-8"?>
<WwiseDocument Type="WorkUnit" ID="{8E94B613-0501-4FA0-9E2E-0B3A4CD0B4AC}" SchemaVersion="89">
    <SoundBankList>
        <SoundBank ID="{16D76893-17B0-49E0-9B60-10021E9A6FAA}" Name="BardMod">
            <IncludedObjects/>
        </SoundBank>
    </SoundBankList>
</WwiseDocument>
"""
    proj_file = wwise_proj_dir / "BardMod.wproj"
    proj_file.write_text(proj_content, encoding="utf-8")
    return wwise_proj_dir, proj_file

def convert_wav_to_wem_wwise(wwise_cli_path):
    """Convert WAV to WEM using Wwise CLI batch processing."""
    banner("Step 2a: Converting WAV → WEM via Wwise")
    
    if WEM_FILE.exists():
        print("  WEM already exists, skipping.")
        return True

    wwise_proj_dir, proj_file = create_wwise_project()
    
    # Use WwiseCLI to do the conversion
    # WwiseCLI.exe <project> -GenerateSoundBanks -Platform Windows -Language English
    print(f"  Using Wwise CLI: {wwise_cli_path}")
    print("  Note: For BG3 audio, Vorbis quality ~0.6 is recommended.")
    
    # Alternative: use the Wwise batch-mode conversion script approach
    # Many BG3 modders use the sound2wem.bat community script
    # We create a WEM by running through the Wwise project

    conv_cmd = [
        str(wwise_cli_path),
        str(proj_file),
        "-ConvertExternalSources",
        f"-Source", str(WAV_FILE),
    ]
    
    try:
        result = subprocess.run(conv_cmd, capture_output=True, text=True, timeout=120)
        print(result.stdout)
        if result.returncode != 0:
            print(f"  Warning: WwiseCLI returned code {result.returncode}")
            print(result.stderr)
    except Exception as e:
        print(f"  Warning: Wwise CLI conversion failed: {e}")
        return False
    
    return WEM_FILE.exists()

def convert_wav_to_wem_alternative():
    """
    Alternative WEM conversion using vgmstream-compatible encoder.
    This approach uses the community 'ww2ogg' + 'revorb' pipeline or
    wwiser. Not all tools can ENCODE to WEM (most decode WEM->wav).
    The recommended path is always Wwise for BG3 compatibility.
    """
    banner("Step 2b: Alternative WEM conversion")
    print("  ❌ No automatic alternative encoder is available.")
    print("  You MUST use Audiokinetic Wwise to create .wem files.")
    print("  See INSTALLATION_GUIDE.md section 'Converting to WEM'.")
    return False

def step_convert_to_wem():
    wwise_path = find_wwise_cli()
    if wwise_path:
        success = convert_wav_to_wem_wwise(wwise_path)
    else:
        print("\n  ⚠️  Wwise CLI not found automatically.")
        print("  Set WWISECLI_PATH environment variable to your WwiseCLI.exe path,")
        print("  or see INSTALLATION_GUIDE.md to install Wwise.\n")

        # Try the manual approach
        print("  Attempting alternative conversion method...")
        success = convert_wav_to_wem_alternative()

    if not success:
        print("\n  ─────────────────────────────────────────────────────")
        print("  MANUAL STEP REQUIRED: Convert WAV to WEM manually")
        print(f"  Input file  : {WAV_FILE}")
        print(f"  Output file : {WEM_FILE}")
        print("  See INSTALLATION_GUIDE.md → Section 3 for instructions")
        print("  Then re-run this script with: python build_mod.py --skip-convert")
        print("  ─────────────────────────────────────────────────────")
        return False
    return True

# ─────────────────────────────────────────────────────────────────────────────
#  STEP 3: RENAME & COPY WEM FILES TO MOD FOLDER
# ─────────────────────────────────────────────────────────────────────────────

def deploy_wem_files(mode="power_only"):
    """
    Copy and rename the .wem file to all required IDs.
    
    mode="power_only"  → Only replace "The Power" (recommended first test)
    mode="all_songs"   → Replace every bard song
    """
    banner("Step 3: Copying WEM files to mod folder")
    
    if not WEM_FILE.exists():
        print(f"  ❌ WEM file not found: {WEM_FILE}")
        print("  Complete step 2 first (WAV → WEM conversion).")
        return False

    SOUND_DIR.mkdir(parents=True, exist_ok=True)
    count = 0

    if mode == "power_only":
        songs_to_deploy = {"The Power (MAIN TARGET)": WEM_IDS["The Power (MAIN TARGET)"]}
    else:
        songs_to_deploy = WEM_IDS

    for song_name, instruments in songs_to_deploy.items():
        print(f"\n  Song: {song_name}")
        for instrument, wem_id in instruments.items():
            dest = SOUND_DIR / f"{wem_id}.wem"
            shutil.copy2(WEM_FILE, dest)
            print(f"    {instrument:10s} → {dest.name}")
            count += 1

    print(f"\n  ✅ Deployed {count} .wem files to mod folder.")
    return True

# ─────────────────────────────────────────────────────────────────────────────
#  STEP 4: PACKAGE THE MOD (.pak)
#  Requires LSLib's ExportTool (divine.exe) or BG3 Modder's Multitool
# ─────────────────────────────────────────────────────────────────────────────

def find_divine():
    """Look for divine.exe (LSLib)"""
    common = [
        Path("C:/Games/BG3Modding/lslib/divine.exe"),
        Path(os.environ.get("LOCALAPPDATA", "")) / "BG3ModdersMultitool" / "Tools" / "divine.exe",
        SCRIPT_DIR / "tools" / "divine.exe",
    ]
    env_path = os.environ.get("DIVINE_PATH")
    if env_path:
        common.insert(0, Path(env_path))
    for p in common:
        if p.exists():
            return p
    return None

def package_mod():
    banner("Step 4: Packaging mod into .pak file")

    divine = find_divine()
    output_pak = BUILD_DIR / "ThroughFireAndFlames.pak"
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    if divine:
        print(f"  Using divine.exe: {divine}")
        cmd = [
            str(divine),
            "--action", "create-package",
            "--source", str(MOD_DIR),
            "--destination", str(output_pak),
            "--compression-method", "None",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ Packed: {output_pak}")
        else:
            print(f"  ⚠️  divine.exe error: {result.stderr}")
    else:
        print("  ⚠️  divine.exe (LSLib) not found.")
        print("  Set DIVINE_PATH environment variable to your divine.exe path.")
        print("  OR: Drag the 'ThroughFireAndFlamesMod' folder into BG3 Modder's Multitool.")
        print()
        print(f"  Manual pack source folder: {MOD_DIR}")
        print(f"  Expected output .pak:       {output_pak}")
        print()
        print("  Download LSLib from: https://github.com/Norbyte/lslib/releases")
        print("  Download BG3 Modder's Multitool from:")
        print("    https://github.com/ShinyHobo/BG3-Modders-Multitool")

# ─────────────────────────────────────────────────────────────────────────────
#  STEP 5: INSTALL
# ─────────────────────────────────────────────────────────────────────────────

def install_mod():
    banner("Step 5: Installing mod")
    
    pak_src = BUILD_DIR / "ThroughFireAndFlames.pak"
    mods_dir = Path(os.environ.get("LOCALAPPDATA", "")) / \
               "Larian Studios" / "Baldur's Gate 3" / "Mods"

    if not pak_src.exists():
        print("  ❌ .pak file not found. Run step 4 first.")
        return

    mods_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(pak_src, mods_dir / "ThroughFireAndFlames.pak")
    print(f"  ✅ Installed to: {mods_dir}")
    print()
    print("  Now activate the mod in BG3 Mod Manager:")
    print("    https://github.com/LaughingLeader/BG3ModManager")
    print()
    print("  In-game: Give your bard a musical instrument and use")
    print("  'Play Instrument' → 'The Power' to hear TTFAF! 🤘")

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Build the Through the Fire and Flames BG3 Bard Mod"
    )
    parser.add_argument("--skip-download", action="store_true",
                        help="Skip download step (use existing WAV/MP3)")
    parser.add_argument("--skip-convert", action="store_true",
                        help="Skip WAV→WEM conversion (use existing WEM)")
    parser.add_argument("--all-songs", action="store_true",
                        help="Replace ALL bard songs (not just 'The Power')")
    parser.add_argument("--install", action="store_true",
                        help="Auto-install after building")
    parser.add_argument("--wem-path", type=str,
                        help="Path to an already-converted .wem file")
    return parser.parse_args()

def main():
    args = parse_args()

    print()
    print("=" * 60)
    print("  Through the Fire and Flames - BG3 Bard Mod Builder")
    print("  by DragonForce  |  Mod Builder Script")
    print("=" * 60)
    print()

    # Handle pre-supplied WEM file
    if args.wem_path:
        src = Path(args.wem_path)
        if src.exists():
            TEMP_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, WEM_FILE)
            print(f"  ✅ Using provided WEM: {src}")
        else:
            print(f"  ❌ Provided WEM not found: {src}")
            sys.exit(1)

    # Determine song replacement mode
    deploy_mode = "all_songs" if args.all_songs else "power_only"

    # Step 1 – Download
    if not args.skip_download and not args.wem_path:
        require_tools()
        download_audio()
    else:
        print("  ⏭  Skipping download step.")

    # Step 2 – Convert
    if not args.skip_convert and not args.wem_path:
        ok = step_convert_to_wem()
        if not ok:
            print("\n  Stopping. Resolve WEM conversion and re-run.")
            sys.exit(1)
    else:
        print("  ⏭  Skipping WEM conversion step.")

    # Step 3 – Deploy
    ok = deploy_wem_files(mode=deploy_mode)
    if not ok:
        sys.exit(1)

    # Step 4 – Package
    package_mod()

    # Step 5 – Install (optional)
    if args.install:
        install_mod()

    banner("Done! 🎸")
    print("  Your mod files are ready in:")
    print(f"    {MOD_DIR}")
    print()
    print("  Next steps if packaging manually:")
    print("    1. Open BG3 Modder's Multitool")
    print("    2. Drag the 'ThroughFireAndFlamesMod' folder into it")
    print("    3. It will generate ThroughFireAndFlames.pak")
    print("    4. Load .pak in BG3 Mod Manager and activate it")
    print("    5. Launch BG3, pick up an instrument, and SHRED! 🤘")
    print()

if __name__ == "__main__":
    main()
