#!/bin/bash

# Exportar variables de entorno
export PYTHONUNBUFFERED=1
export PYTHONIOENCODING=utf-8

# Obtener la ruta del directorio donde está el script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "========================================="
echo "        Iniciando JARVISSS (Linux)       "
echo "========================================="

# Auto-configuración si es la primera vez que se ejecuta en este Linux
if [ ! -d "venv_linux" ]; then
    echo "[!] No se detectó el entorno de Linux (venv_linux)."
    echo "[*] Ejecutando configuración inicial..."
    chmod +x setup_linux.sh
    ./setup_linux.sh
fi

# Activar el entorno virtual de Linux
if [ -f "venv_linux/bin/activate" ]; then
    source venv_linux/bin/activate
else
    echo "[!] Error crítico: No se pudo encontrar venv_linux/bin/activate."
    echo "    Prueba ejecutando: ./setup_linux.sh manualmente."
    exit 1
fi

# Determinar el ejecutable de Python
PYTHON_EXE="python3"

echo "[*] Iniciando servicios de backend..."

# Iniciar los componentes en el fondo
$PYTHON_EXE main.py > main.log 2>&1 &
PID_MAIN=$!

$PYTHON_EXE motor_proactivo.py > motor_proactivo.log 2>&1 &
PID_PROACTIVO=$!

echo "[*] Cerebro y Motor Proactivo iniciados en segundo plano."
echo "[*] Iniciando Aplicación Nativa de BMO a Pantalla Completa..."
echo "=========================================================="
echo " BMO tomará el control de la pantalla."
echo " (Presiona la tecla ESC o haz DOBLE CLIC en la cara para salir)"
echo "=========================================================="

# Iniciar la interfaz nativa en primer plano
$PYTHON_EXE ui_bmo_nativa.py

# --- Cuando el script recibe Ctrl+C, se ejecutan estas líneas ---

echo ""
echo "[*] Apagando servicios de JARVIS..."
kill $PID_MAIN 2>/dev/null
kill $PID_PROACTIVO 2>/dev/null
echo "[*] Jarvis apagado correctamente. ¡Hasta luego!"
