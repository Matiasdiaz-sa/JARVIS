#!/bin/bash

# Exportar variables de entorno equivalentes a las de Windows
export PYTHONUNBUFFERED=1
export PYTHONIOENCODING=utf-8

# Obtener la ruta del directorio donde está el script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "Iniciando JARVISSS..."

# Activar el entorno virtual automáticamente
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Determinar el ejecutable de Python
PYTHON_EXE="python3.11"

# Iniciar los componentes en el fondo
$PYTHON_EXE main.py > main.log 2>&1 &
PID_MAIN=$!

$PYTHON_EXE motor_proactivo.py > motor_proactivo.log 2>&1 &
PID_PROACTIVO=$!

# Iniciar la Cara de Jarvis (interfaz web) en primer plano para mantener la terminal abierta
echo "Cerebro y Motor Proactivo iniciados."
echo "Iniciando Cliente de Cara..."
echo "Puedes acceder a la cara en http://localhost:8001"
echo "Cierra esta ventana para apagar a JARVIS."

$PYTHON_EXE cliente_cara.py

# Al cerrar la cara con Ctrl+C (o cerrar la terminal), matar los procesos de fondo
kill $PID_MAIN
kill $PID_PROACTIVO
echo "Jarvis apagado correctamente."
