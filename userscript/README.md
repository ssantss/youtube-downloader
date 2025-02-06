# YouTube Downloader UserScript

Script para Tampermonkey que agrega un botón de descarga en los videos de YouTube.

## Instalación

1. Instala la extensión Tampermonkey en tu navegador
2. Crea un nuevo script
3. Copia y pega el contenido de `youtube-downloader.user.js`
4. Modifica la URL en la línea:
   ```javascript
   window.open(`http://192.168.1.115:5270?url=${encodeURIComponent(window.location)}`, '_blank');
   ```
   Reemplaza `192.168.1.115:5270` con tu IP y puerto
5. Guarda el script

## Uso

El script agregará un botón "🐧 Descargar pekin" en cada video de YouTube. 