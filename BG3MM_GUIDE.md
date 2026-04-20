# ⚙️ Guía Definitiva: BG3 Mod Manager (BG3MM) y Activación de tu Mod

Para que Baldur's Gate 3 detecte correctamente la música que acabas de crear sin romper el juego (ni las partidas multijugador), el estándar de la comunidad es usar **BG3 Mod Manager**. 

Esta guía cubre todo el proceso desde cero.

---

## Fase 1: Descarga e Instalación de BG3 Mod Manager

1. Abre tu navegador y ve a la página oficial de GitHub:
   👉 https://github.com/LaughingLeader/BG3ModManager/releases/latest
2. Desplázate hacia abajo hasta la sección **Assets**.
3. Haz clic en el archivo llamado **`BG3ModManager_Latest.zip`** para descargarlo.
4. Una vez descargado, **crea una nueva carpeta** en tu ordenador donde no vaya a ser borrado (p. ej., `C:\Games\BG3 Mod Manager` o en tu propio escritorio).
5. Extrae el contenido del archivo `.zip` dentro de esa nueva carpeta.
6. Localiza el archivo con el logo del dado azul llamado **`BG3ModManager.exe`** y ábrelo.

---

## Fase 2: Configuración Inicial (Solo la primera vez)

Si es la primera vez que lo abres, es posible que el Mod Manager necesite saber dónde tienes instalado el juego.

1. Abre `BG3ModManager.exe`.
2. En la barra superior, haz clic en **`Settings`** -> **`Preferences`**.
3. Revisa la pestaña de la izquierda llamada **`General`**. Fíjate en los dos apartados principales:
   * **Game Data Path:** Debería ser la ruta a la carpeta "Data" del juego. Suele auto-detectarse (p. ej. `C:\Program Files (x86)\Steam\steamapps\common\Baldurs Gate 3\Data`).
   * **Game Executable Path:** Debe ser la ruta al ejecutable `bg3_dx11.exe` o `bg3.exe` (p. ej. `C:\Program Files (x86)\Steam\steamapps\common\Baldurs Gate 3\bin\bg3_dx11.exe`).
4. Si ves que las rutas están en rojo o vacías, dales al botón de los tres puntos `[...]` para buscar las carpetas en tu equipo. Cuando estén bien, haz clic en el botón de abajo **`Save`**.

---

## Fase 3: Instalación de tu Mod (`.pak` o `.zip`)

Ahora vamos a decirle al gestor que quieres instalar tu obra de arte musical.

1. En tu ordenador, localiza el archivo que generaste con el BG3 Modders Multitool (generalmente **`ThroughFireAndFlames.zip`** o el `.pak` si seguiste sacando los empaquetados del Multitool).
2. Sin cerrar el BG3 Mod Manager, ve a la barra superior y pulsa **`File`** -> **`Import Mod...`** (o pulsa `CTRL + M`).
3. Selecciona tu archivo modificado. 
4. Verás que en la parte inferior del programa dice *"Imported ThroughFireAndFlames successfully"*.

> **¿Qué acaba de hacer el programa?** De fondo, de forma invisible, BG3MM ha extraído el archivo .pak y lo ha guardado en la carpeta mágica oculta de los perfiles de tu juego: `AppData\Local\Larian Studios\Baldur's Gate 3\Mods`.

---

## Fase 4: Orden de Carga (Load Order) y Activación

Aunque el mod ya está "cargado" en el programa, el juego todavía no sabe que quieres leerlo. BG3 usa un sistema estricto llamado "Load Order" (Orden de carga) que le dice al juego qué modificaciones inyectar y en qué prioridad.

1. Al abrir el programa, verás el panel dividido en dos mitades gigantes:
   * **Izquierda (Active Mods):** Qué mods se van a cargar en el juego.
   * **Derecha (Inactive Mods):** Qué mods tienes instalados, pero el juego ignorará.
2. Tu mod debería estar en la **columna derecha (Inactive)**.
3. Haz **clic izquierdo mantenido** sobre tu mod, **arrástralo hacia la columna izquierda (Active)** y suéltalo.
4. Fíjate que al lado izquierdo ahora le aparecerá un número (p. ej. `[ 1 ]`), indicando su orden.

---

## Fase 5: Exportar al juego y 🤘 ¡Jugar!

**Este es el paso fundamental donde mucha gente se equivoca. No basta con moverlo a la izquierda y cerrar el programa.**

1. En la barra de iconos superior (justo debajo del menú `File`), verás un icono que es una pequeña **hoja de papel verde con flechas hacia abajo** (si pones el ratón encima dirá *"Export Order to Game"*). Haz clic en él.
   * *Alternativa: Puedes hacer clic en el menú superior `File` -> `Export Order to Game`.*
2. En la parte de abajo de tu pantalla, aparecerá una barra verde indicando éxito. Esto acaba de programar el juego para arrancar el mod.
3. En la barra superior, a la derecha del mismo icono verde, verás el icono clásico de un **disquete** (*"Save Load Order to File"*). Dale clic también para guardar en el propio gestor esa combinación y que lo recuerde al volver a abrir.

**¡Ya has terminado!** 

Cierra BG3 Mod Manager. Inicia Baldur's Gate 3 desde Steam con normalidad, equípate tu instrumento para tocar, elige tu canción modificada, y ¡que empiece el espectáculo!

---

### 🌐 ¿Qué ocurre con el Multijugador Cooperativo?
* Para jugar online con esto, **tus amigos tienen que hacer exactamente lo mismo que tú a partir de la Fase 3**.
* Pásales tu mod modificado final.
* Ellos deben descargar e instalar el **BG3 Mod Manager**, hacer el Import, arrastrar el mod a la izquierda *"Active"* y exportar al juego (botón de la hoja verde). 
* Si todos tenéis la lista *"Active Mods"* sincronizada, el juego no pondrá problemas de conexión y escucharéis exactamente la misma música durante las tonadas.

---

### 🎮 Cómo jugar con tu mod en la Steam Deck
El archivo `.pak` que has creado es 100% universal y su audio modificado funciona de forma nativa en la Steam Deck sin problemas.

Dado que BG3 Mod Manager es un programa de Windows (`.exe`), la forma más fácil para jugar en la Deck no es instalando el mod manager ahí, sino **exportando lo que ya has montado en tu PC de sobremesa**. Tienes dos vías:

#### Vía A: Transferencia Manual (Recomendada)
Como ya ordenaste el mod en tu PC, tu ordenador ya generó el archivo maestro donde dice "cargar este mod". Solo copia dos archivos de tu PC a la Steam Deck (puedes usar KDE Connect, Warpinator, o un USB):

1. **Tu mod:** Copia el archivo `ThroughFireAndFlames.pak`  
   👉 Ruta destino en Desktop Mode de Steam Deck:  
   `/home/deck/.local/share/Steam/steamapps/compatdata/1086940/pfx/drive_c/users/steamuser/AppData/Local/Larian Studios/Baldur's Gate 3/Mods/`
2. **El archivo de texto de ordenación (Load Order):** Copia tu archivo `modsettings.lsx` de tu PC.  
   👉 Ruta destino en Desktop Mode de Steam Deck:  
   `/home/deck/.local/share/Steam/steamapps/compatdata/1086940/pfx/drive_c/users/steamuser/AppData/Local/Larian Studios/Baldur's Gate 3/PlayerProfiles/Public/`

#### Vía B: Gestor Nativo del Juego (Con el Parche 7)
1. Simplemente copia el `.pak` a la larga ruta descrita en la Vía A.
2. Inicia Baldur's Gate 3 normalmente en la consola en Modo Juego. 
3. Dirígete a la opción de **"Administrador de Mods"** -> **"Ajustes" / "Instalados"** (arriba del todo).
4. El juego escaneará los mods manuales metidos en la carpeta y te permitirá marcar con un ✅ (tick) tu mod, activándolo directamente para esa sesión en Steam Deck.
