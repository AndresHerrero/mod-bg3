# 🎸 Through the Fire and Flames — BG3 Bard Mod
## Guía de Instalación Completa

> **Objetivo:** Cuando tu bardo toque un instrumento en Baldur's Gate 3, suena *Through the Fire and Flames* de DragonForce en lugar de la música original del juego.

---

## Estructura del Proyecto

```
mod bg3/
├── build_mod.py                    ← Script automatizado (ejecutar esto)
├── INSTALLATION_GUIDE.md           ← Esta guía
├── _temp/                          ← Archivos temporales de construcción
├── _build/                         ← .pak final generado aquí
└── ThroughFireAndFlamesMod/        ← Estructura del mod
    ├── Mods/
    │   └── ThroughFireAndFlames/
    │       └── meta.lsx            ← Metadatos del mod (ya creado ✅)
    └── Public/
        └── ThroughFireAndFlames/
            └── Assets/
                └── Sound/          ← Aquí van los archivos .wem
```

---

## Herramientas Necesarias

| Herramienta | Para qué sirve | Descarga |
|---|---|---|
| **Python 3.8+** | Ejecutar el script | https://python.org |
| **FFmpeg** | Convertir MP3 → WAV | https://ffmpeg.org/download.html |
| **yt-dlp** | Descargar el audio | `pip install yt-dlp` |
| **Audiokinetic Wwise** | Convertir WAV → WEM | https://www.audiokinetic.com |
| **LSLib (divine.exe)** | Empaquetar el mod en .pak | https://github.com/Norbyte/lslib/releases |
| **BG3 Mod Manager** | Activar el mod en el juego | https://github.com/LaughingLeader/BG3ModManager |

---

## Paso 1 — Instalar las Herramientas

### 1.1 Python
1. Descarga Python desde https://python.org/downloads
2. Durante la instalación, **marca la casilla "Add Python to PATH"**
3. Verifica: abre PowerShell y escribe `python --version`

### 1.2 FFmpeg
1. Descarga FFmpeg desde https://github.com/BtbN/FFmpeg-Builds/releases
2. Descarga `ffmpeg-master-latest-win64-gpl.zip`
3. Extrae en `C:\ffmpeg\`
4. Añade `C:\ffmpeg\bin` al **PATH del sistema**:
   - Busca "Variables de entorno" en el menú inicio
   - En "Variables del sistema" → "Path" → Editar → Añadir `C:\ffmpeg\bin`
5. Verifica: `ffmpeg -version`

### 1.3 yt-dlp
```powershell
pip install yt-dlp
```

### 1.4 Wwise (CRÍTICO para la conversión WEM)
1. Crea una cuenta gratuita en https://audiokinetic.com
2. Descarga el **Wwise Launcher**
3. Instala Wwise versión **2019.2.x** (la más compatible con BG3)
   - En el Launcher, ve a Wwise → Install
   - Selecciona SDK (nativo) + Authoring Tool
4. El `WwiseCLI.exe` estará en:
   ```
   C:\Program Files (x86)\Audiokinetic\Wwise 2019.2.15.7416\Authoring\x64\Release\bin\WwiseCLI.exe
   ```

### 1.5 LSLib
1. Descarga la última versión desde https://github.com/Norbyte/lslib/releases
2. Extrae en `C:\Games\BG3Modding\lslib\`

---

## Paso 2 — Conversión de Audio (Proceso Manual en Wwise)

> IMPORTANTE: Esta es la parte más técnica. Wwise es OBLIGATORIO para generar archivos .wem compatibles con BG3.

### 2.1 Preparar el archivo WAV
Ejecuta el script para descargar y preparar el WAV:
```powershell
cd "c:\Users\Control Energy\Desktop\Projects\mod bg3"
python build_mod.py --skip-convert
```
Esto creará: `_temp\through_fire_flames.wav`

### 2.2 Convertir WAV → WEM en Wwise

1. **Abre Wwise** (Audiokinetic Wwise Authoring Tool)

2. **Crea un nuevo proyecto:**
   - File → New Project → Nombre: `BardModBG3`

3. **Añade el archivo de audio:**
   - En el Project Explorer → pestaña Audio
   - Clic derecho en `Actor-Mixer Hierarchy` → Import Audio Files
   - Selecciona `_temp\through_fire_flames.wav`

4. **Configura la conversión:**
   - Clic derecho en el audio → Properties
   - Conversion Settings: `Vorbis Quality High`
   - Sample Rate: **48000 Hz** | Channels: **Stereo**

5. **Genera el SoundBank:**
   - Project → Generate All SoundBanks
   - Los .wem aparecerán en `.cache\Windows\SFX\`

6. **Copia el .wem generado a:**
   ```
   _temp\through_fire_flames.wem
   ```

---

## Paso 3 — Ejecutar el Script de Construcción

```powershell
cd "c:\Users\Control Energy\Desktop\Projects\mod bg3"

# Solo reemplazar "The Power" (recomendado para prueba)
python build_mod.py --skip-download

# Reemplazar TODAS las canciones de bardo
python build_mod.py --skip-download --all-songs

# Usar un .wem que ya tienes
python build_mod.py --wem-path "C:\ruta\a\tu\archivo.wem"

# Todo automático + instalar
python build_mod.py --install
```

---

## Paso 4 — Empaquetar el Mod (.pak)

### Opción A: Con LSLib (Automático si está en la ruta por defecto)
El script lo hace solo.

### Opción B: Con BG3 Modder's Multitool
1. Descarga BG3 Modder's Multitool: https://github.com/ShinyHobo/BG3-Modders-Multitool
2. Ábrelo
3. Arrastra la carpeta `ThroughFireAndFlamesMod/` a la ventana
4. Clic en **Pack Mod**
5. El `.pak` se genera en `_build/ThroughFireAndFlames.pak`

---

## Paso 5 — Instalar y Activar el Mod

### Instalación manual:
Copia `_build/ThroughFireAndFlames.pak` a:
```
C:\Users\[TuUsuario]\AppData\Local\Larian Studios\Baldur's Gate 3\Mods\
```

### Activar en BG3 Mod Manager:
1. Abre **BG3 Mod Manager**
2. El mod aparece en "Available Mods" → arrástralo a "Active Mods"
3. Clic en **Export Order to Game**
4. Lanza BG3

---

## Paso 6 — Probar en el Juego

1. **Coge un instrumento musical** (Lute, Lyre, Flute, Violin, o Drum)
2. Clic derecho en el instrumento → **Play Instrument**
3. **Selecciona "The Power"** en el menú de canciones
4. TTFAF debería sonar! 🎸

---

## IDs de Archivos WEM de los Instrumentos

| Canción | Drum | Flute | Lute | Lyre | Violin | Whistle |
|---|---|---|---|---|---|---|
| **Bard Dance** | 91256288 | 98035890 | 582548246 | 340373265 | 958425049 | 824207806 |
| **Of Divinity and Sin** | 575371427 | 591535284 | 1006554640 | 282455428 | 93950250 | 454628062 |
| **Old Time Battles** | 1032011443 | 688689226 | 88231746 | 160641375 | 107779537 | 549395448 |
| **Sing For Me** | 638547722 | 734862967 | 242730486 | 214215821 | 43926257 | 319298902 |
| **The Power** ⭐ | 264861677 | 247277282 | 230164766 | 182777796 | 470306917 | — |
| **The Queen's High Sea** | 712621309 | 172278436 | 801458525 | 351453867 | 813458288 | 1004988978 |

> **⭐ = Objetivo principal del reemplazo**

---

## Solución de Problemas

- **No suena nada:** Verifica que los .wem tienen exactamente el nombre correcto (números + `.wem`)
- **El audio se corta:** TTFAF dura ~7 min; edita el WAV con Audacity a 2-3 min
- **WwiseCLI.exe falla:** Instala la versión Authoring Tool completa, no solo el SDK
- **divine.exe error:** Usa BG3 Modder's Multitool como alternativa visual

---

## Recursos Adicionales

- BG3 Modding Community Wiki: https://bg3.community/
- LSLib by Norbyte: https://github.com/Norbyte/lslib
- BG3 Modder's Multitool: https://github.com/ShinyHobo/BG3-Modders-Multitool
- BG3 Mod Manager: https://github.com/LaughingLeader/BG3ModManager
