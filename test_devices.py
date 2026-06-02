import sys
import os

sys.path.append(r"e:\Proyecto-IALOCAL")
from tools_spotify import obtener_cliente_spotify

try:
    sp = obtener_cliente_spotify()
    devices = sp.devices().get('devices', [])
    print("--- DISPOSITIVOS DE SPOTIFY ---")
    if not devices:
        print("NO HAY DISPOSITIVOS.")
    for d in devices:
        print(f"Nombre: {d['name']} | ID: {d['id']} | Activo: {d['is_active']} | Tipo: {d['type']}")
    print("-------------------------------")
except Exception as e:
    print(f"Error: {e}")
