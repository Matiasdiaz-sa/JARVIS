#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DESKTOP_FILE="$HOME/Escritorio/Jarvis.desktop"
if [ ! -d "$HOME/Escritorio" ]; then
    DESKTOP_FILE="$HOME/Desktop/Jarvis.desktop"
fi

echo "[Desktop Entry]
Name=Jarvis
Comment=Asistente Virtual IA
Exec=gnome-terminal -- bash -c '\"$DIR/iniciar_jarvis.sh\"; exec bash'
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Utility;" > "$DESKTOP_FILE"

chmod +x "$DESKTOP_FILE"
chmod +x "$DIR/iniciar_jarvis.sh"

echo "¡Acceso directo creado en tu escritorio!"
