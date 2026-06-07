#!/bin/bash
echo "=========================================="
echo " Instalador de Jarvis Face (Modo Kiosco)  "
echo "=========================================="

echo "Asegúrate de tener conexión a Internet."
echo "Este proceso instalará Jarvis en tu computadora."
echo ""

# 1. Instalar dependencias del sistema operativo
echo "[1/4] Instalando paquetes de Linux (puede pedir tu contraseña)..."
sudo apt update
sudo apt install -y python3-pip python3-venv python3-pyqt6 portaudio19-dev libasound2-dev alsa-utils x11-xserver-utils

# 2. Determinar ubicación
# Asumimos que el script se corre desde el pendrive
SOURCE_DIR=$(pwd)
DEST_DIR="$HOME/JarvisOS"

echo "[2/4] Copiando Jarvis desde el pendrive ($SOURCE_DIR) a tu disco duro ($DEST_DIR)..."
mkdir -p "$DEST_DIR"
cp -r "$SOURCE_DIR/"* "$DEST_DIR/"

# 3. Entorno Virtual Python
echo "[3/4] Configurando el Cerebro de Python..."
cd "$DEST_DIR"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Asegurar dependencias visuales y de audio críticas
pip install PyQt6 PyAudio

# 4. Crear Autostart (El Truco Kiosco)
echo "[4/4] Configurando arranque automático..."
mkdir -p "$HOME/.config/autostart"

# Archivo de auto-arranque para la cara
cat << EOF > "$HOME/.config/autostart/jarvis_face.desktop"
[Desktop Entry]
Type=Application
Exec=$DEST_DIR/venv/bin/python $DEST_DIR/ui_face.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Jarvis Face
Comment=Arranca la cara de Jarvis a pantalla completa al iniciar sesión
EOF

# Archivo para evitar que la pantalla se apague sola (xset)
cat << 'EOF' > "$DEST_DIR/disable_screensaver.sh"
#!/bin/bash
xset s off
xset -dpms
xset s noblank
EOF
chmod +x "$DEST_DIR/disable_screensaver.sh"

cat << EOF > "$HOME/.config/autostart/disable_screensaver.desktop"
[Desktop Entry]
Type=Application
Exec=$DEST_DIR/disable_screensaver.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Evitar Apagado de Pantalla
EOF

echo "=========================================="
echo " ¡Instalación Completada con Éxito!       "
echo "=========================================="
echo "Ya puedes retirar el pendrive si lo deseas."
echo "Para ver a Jarvis, simplemente reinicia la computadora."
echo "Al volver a encender, arrancará directamente en la Cara."
echo ""
read -p "Presiona ENTER para cerrar esta ventana..."
