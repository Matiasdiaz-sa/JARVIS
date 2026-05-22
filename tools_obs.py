import os
import time
from dotenv import load_dotenv

# Nota: requiere instalar obsws-python (pip install obsws-python)
try:
    import obsws_python as obs
    OBS_AVAILABLE = True
except ImportError:
    OBS_AVAILABLE = False

load_dotenv()

def obtener_cliente_obs():
    """Conecta al OBS WebSocket local. Requiere OBS_PASSWORD en el .env."""
    if not OBS_AVAILABLE:
        return None, "Error: La librería obsws-python no está instalada. Ejecuta: pip install obsws-python"
        
    # Por defecto OBS WebSocket en v5 usa el puerto 4455
    host = os.getenv("OBS_HOST", "localhost")
    port = int(os.getenv("OBS_PORT", 4455))
    password = os.getenv("OBS_PASSWORD", "")
    
    if not password:
        return None, "Error: No hay OBS_PASSWORD en el archivo .env. Ve a OBS -> Herramientas -> Configuración de WebSocket y pon una contraseña, luego añádela al .env."
        
    try:
        client = obs.ReqClient(host=host, port=port, password=password)
        return client, "Éxito"
    except Exception as e:
        return None, f"Error de conexión con OBS. Asegúrate de que OBS esté abierto y el WebSocket habilitado: {e}"

def controlar_obs(accion: str, parametro: str = "") -> str:
    """
    Controla OBS Studio. 
    Acciones soportadas: iniciar_grabacion, detener_grabacion, cambiar_escena.
    """
    client, msg = obtener_cliente_obs()
    if not client:
        return msg
        
    try:
        if accion == "iniciar_grabacion":
            client.start_record()
            with open("obs_rec.lock", "w") as f:
                f.write("1")
            return "Grabación de OBS iniciada correctamente."
            
        elif accion == "detener_grabacion":
            client.stop_record()
            if os.path.exists("obs_rec.lock"):
                os.remove("obs_rec.lock")
            return "Grabación de OBS detenida correctamente."
            
        elif accion == "cambiar_escena":
            if not parametro:
                return "Error: Para cambiar escena debes especificar el nombre de la escena."
            client.set_current_program_scene(parametro)
            return f"Escena de OBS cambiada a: {parametro}"
            
        else:
            return f"Error: Acción '{accion}' desconocida para OBS."
            
    except Exception as e:
        return f"Error al ejecutar comando en OBS: {e}"
