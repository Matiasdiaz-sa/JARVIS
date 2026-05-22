import json
import os

MEMORIA_FILE = "memoria.json"

def leer_memoria() -> dict:
    """Lee el archivo de memoria. Retorna un diccionario."""
    if not os.path.exists(MEMORIA_FILE):
        return {}
    try:
        with open(MEMORIA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Memoria] Error al leer memoria: {e}")
        return {}

def obtener_memoria_texto() -> str:
    """Retorna la memoria formateada como texto para inyectar en el System Prompt."""
    memoria = leer_memoria()
    if not memoria:
        return "Actualmente tu memoria a largo plazo está vacía."
    
    texto = "MEMORIA A LARGO PLAZO (Lo que sabes del usuario):\n"
    for clave, valor in memoria.items():
        texto += f"- {clave}: {valor}\n"
    return texto

def gestionar_memoria(accion: str, clave: str, valor: str = "") -> str:
    """
    Herramienta para que el LLM guarde o borre datos de la memoria.
    Acciones: 'guardar', 'borrar'
    """
    memoria = leer_memoria()
    
    if accion == "guardar":
        if not clave or not valor:
            return "Error: Para guardar, se requiere una clave y un valor."
        memoria[clave] = valor
        msg = f"Dato guardado en memoria -> {clave}: {valor}"
        
    elif accion == "borrar":
        if not clave:
            return "Error: Para borrar, se requiere una clave."
        if clave in memoria:
            del memoria[clave]
            msg = f"Dato borrado de memoria -> {clave}"
        else:
            return f"Error: La clave '{clave}' no existe en memoria."
    else:
        return f"Error: Acción '{accion}' desconocida."
        
    # Guardar archivo
    try:
        with open(MEMORIA_FILE, "w", encoding="utf-8") as f:
            json.dump(memoria, f, ensure_ascii=False, indent=4)
        print(f"[Memoria] {msg}")
        return msg
    except Exception as e:
        return f"Error al escribir en el disco: {e}"

if __name__ == "__main__":
    print(gestionar_memoria("guardar", "Nombre", "Matias"))
    print(obtener_memoria_texto())
