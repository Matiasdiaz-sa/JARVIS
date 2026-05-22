import threading
import time
import os
import winsound

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

_sentinel_active = False
_sentinel_thread = None

def _sentinel_loop(cap):
    """Bucle de fondo del centinela. Vigila la cámara y dispara alerta si hay movimiento."""
    global _sentinel_active
    
    print("[Seguridad] 👁️ Modo Centinela ACTIVADO. Vigilando cámara...")
    
    
    # Leer un par de frames para estabilizar la cámara
    for _ in range(5):
        cap.read()
        time.sleep(0.1)
        
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    
    while _sentinel_active:
        if not os.path.exists("centinela.lock"):
            _sentinel_active = False
            break
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        movimiento_detectado = False
        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            movimiento_detectado = True
            break
            
        if movimiento_detectado:
            print("[Seguridad] ⚠️ ¡MOVIMIENTO DETECTADO!")
            
            # Guardar evidencia
            if not os.path.exists("evidencias"):
                os.makedirs("evidencias")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            ruta_foto = f"evidencias/intruso_{timestamp}.jpg"
            cv2.imwrite(ruta_foto, frame1)
            print(f"[Seguridad] 📸 Foto guardada en {ruta_foto}")
            
            # Alarma sonora (Pitidos de alerta)
            for _ in range(3):
                winsound.Beep(2000, 200)
                time.sleep(0.1)
                
            # Dejar enfriar unos segundos antes de volver a detectar
            time.sleep(5)
            
            # Reestabilizar frames
            cap.read()
            ret, frame1 = cap.read()
            ret, frame2 = cap.read()
            continue
            
        frame1 = frame2
        ret, frame2 = cap.read()
        time.sleep(0.2) # No usar 100% de CPU
        
    cap.release()
    if os.path.exists("centinela.lock"):
        os.remove("centinela.lock")
    print("[Seguridad] 👁️ Modo Centinela DESACTIVADO.")

def gestionar_seguridad(accion: str) -> str:
    """
    Activa o desactiva el modo centinela de Jarvis.
    """
    global _sentinel_active, _sentinel_thread
    
    if not CV2_AVAILABLE:
        return "Error: La librería de visión artificial no está instalada. Ejecuta: pip install opencv-python"
        
    if accion == "activar":
        if _sentinel_active:
            return "El modo centinela ya estaba activado."
            
        # Probar la cámara sincrónicamente para no mentirle al usuario
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Error: No se pudo acceder a la cámara web. Puede que no esté conectada o que otra aplicación la esté usando."
            
        _sentinel_active = True
        with open("centinela.lock", "w") as f:
            f.write("1")
        _sentinel_thread = threading.Thread(target=_sentinel_loop, args=(cap,), daemon=True)
        _sentinel_thread.start()
        return "Modo Centinela activado. Cámara web vigilando movimiento en segundo plano."
        
    elif accion == "desactivar":
        if not _sentinel_active:
            return "El modo centinela ya estaba desactivado."
        _sentinel_active = False
        return "Modo Centinela desactivado."
        
    else:
        return f"Error: Acción '{accion}' desconocida para Seguridad."
