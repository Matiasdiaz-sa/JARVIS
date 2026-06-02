#!/bin/bash

# Exportar variables de entorno equivalentes a las de Windows
export PYTHONUNBUFFERED=1
export PYTHONIOENCODING=utf-8

# Obtener la ruta del directorio donde está el script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Determinar el ejecutable de Python (usar el del entorno virtual si existe)
PYTHON_EXE="python3"
if [ -f "venv/bin/python3" ]; then
    PYTHON_EXE="venv/bin/python3"
fi

echo "Iniciando JARVISSS en segundo plano..."

# Ejecutar los scripts en segundo plano (equivalente a 'start ""' en .bat)
nohup $PYTHON_EXE main.py > main.log 2>&1 &
nohup $PYTHON_EXE ui_jarvis.py > ui_jarvis.log 2>&1 &
nohup $PYTHON_EXE motor_proactivo.py > motor_proactivo.log 2>&1 &

echo "JARVISSS iniciado. Los registros se guardan en *.log"
