import os
import sys
import threading
import motor_audio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import tempfile
import time

# Variables globales compartidas entre el motor de audio y el servidor web
estado_actual = "esperando"

def callback_ui(estado, energia, conf):
    global estado_actual
    
    # Lógica para detectar si Jarvis está hablando
    lock_file = motor_audio.LOCK_FILE
    if os.path.exists(lock_file):
        estado_actual = "hablando"
    else:
        # Si no está hablando, usamos el estado que nos manda motor_audio
        # pero si acaba de soltar el lock, volvemos a lo que dictamine motor_audio
        if estado_actual == "hablando":
            estado_actual = estado
        else:
            estado_actual = estado

# 1. Iniciar el motor de audio en un hilo secundario
def iniciar_hilo_audio():
    print("[UI] Iniciando Hilo de Audio (Micrófono)...")
    try:
        motor_audio.escuchar_continuo(callback_ui=callback_ui)
    except Exception as e:
        print(f"[UI] Error en motor de audio: {e}")

hilo_audio = threading.Thread(target=iniciar_hilo_audio, daemon=True)
hilo_audio.start()

# 2. Configurar el Servidor FastAPI para servir la UI BMO y los estados
app = FastAPI()

# Endpoint de estado para que el JS de BMO consulte qué cara poner
@app.get("/api/estado")
def get_estado():
    return {"estado": estado_actual}

# Montar archivos estáticos (HTML, CSS, JS) de la carpeta ui_web
base_dir = os.path.dirname(os.path.abspath(__file__))
ui_dir = os.path.join(base_dir, "ui_web")

@app.get("/")
def read_root():
    return FileResponse(os.path.join(ui_dir, "index.html"))

# Montar estáticos genéricos (css, js)
app.mount("/", StaticFiles(directory=ui_dir), name="static")

if __name__ == "__main__":
    print("\n" + "="*40)
    print(" INICIANDO CLIENTE CARA BMO")
    print(" URL: http://localhost:8001")
    print("="*40 + "\n")
    # Escucha en 0.0.0.0 puerto 8001 (donde main.py va a mandar requests si en el futuro queremos widgets web)
    uvicorn.run(app, host="0.0.0.0", port=8001)
