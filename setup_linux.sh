#!/bin/bash

# setup_linux.sh - Preparar entorno para Jarvis en Linux
# Este script se encarga de instalar dependencias del sistema operativo
# y configurar el entorno virtual de Python aislado para Linux.

echo "========================================="
echo "  Preparando entorno Jarvis para Linux  "
echo "========================================="

# Detectar el gestor de paquetes e instalar dependencias del sistema operativo
if command -v apt-get >/dev/null; then
    echo "[*] Detectado sistema basado en Debian/Ubuntu (apt)"
    echo "[*] Solicitando permisos sudo para instalar dependencias de sistema..."
    sudo apt-get update
    # portaudio19-dev y flac son necesarios para pyaudio y speech_recognition
    sudo apt-get install -y python3-pip python3-venv portaudio19-dev python3-pyaudio flac ffmpeg
elif command -v pacman >/dev/null; then
    echo "[*] Detectado sistema basado en Arch Linux (pacman)"
    sudo pacman -Sy --noconfirm python-pip python-virtualenv portaudio flac ffmpeg
else
    echo "[!] Gestor de paquetes no soportado automáticamente."
    echo "Por favor asegúrate de tener instalado: python3-venv, portaudio, ffmpeg."
fi

# Ir al directorio del proyecto (donde está este script)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Evitar conflictos con el venv de Windows que pueda venir en el pendrive
echo "[*] Configurando entorno virtual de Linux (venv_linux)..."
if [ ! -d "venv_linux" ]; then
    python3 -m venv venv_linux
fi

echo "[*] Activando entorno e instalando requerimientos..."
source venv_linux/bin/activate
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "[!] No se encontró requirements.txt. Puede que falten dependencias."
fi

# Dar permisos de ejecución al script de inicio principal
chmod +x iniciar_jarvis.sh

echo "========================================="
echo "  ¡Listo! El entorno de Linux está preparado."
echo "  Ahora puedes iniciar a Jarvis con:"
echo "  ./iniciar_jarvis.sh"
echo "========================================="
