import os
import time
import sys
import threading
from tools_vision import analizar_pantalla

# Archivo donde se guardará el contexto en vivo
ARCHIVO_CONTEXTO = "contexto_pantalla.txt"

def bucle_vision():
    """Toma una captura de pantalla cada 45 segundos y extrae el contexto visual."""
    print("[Proactivo] Iniciando Motor de Visión Continua...")
    while True:
        try:
            # Extraer contexto visual usando la IA de visión
            prompt = "Describe en una sola oración breve (máximo 15 palabras) qué programa o contenido está viendo el usuario en su pantalla ahora mismo. Empieza directo con la acción, ej: 'Viendo un video de YouTube sobre autos' o 'Escribiendo código en Visual Studio'."
            contexto = analizar_pantalla(prompt)
            
            if contexto and not contexto.startswith("Error"):
                with open(ARCHIVO_CONTEXTO, "w", encoding="utf-8") as f:
                    f.write(contexto)
                # print(f"[Proactivo] Contexto actualizado: {contexto}")
            
        except Exception as e:
            print(f"[Proactivo] Error en bucle_vision: {e}")
        
        # Esperar 45 segundos para no saturar la API (Gemini tiene límite de 15 RPM gratuito)
        time.sleep(45)

def iniciar_motor_proactivo():
    print("========================================")
    print(" Iniciando Motor Proactivo de Jarvis... ")
    print("========================================")
    
    # Iniciar el hilo de visión
    hilo_vision = threading.Thread(target=bucle_vision, daemon=True)
    hilo_vision.start()
    
    # Aquí en el futuro se pueden añadir más bucles (como revisar correos, reloj, etc)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Proactivo] Apagando el motor proactivo.")
        sys.exit(0)

if __name__ == "__main__":
    iniciar_motor_proactivo()
