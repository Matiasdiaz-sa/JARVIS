import sys
sys.path.append(r"e:\Proyecto-IALOCAL")
from tools_spotify import obtener_cliente_spotify

sp = obtener_cliente_spotify()
pb = sp.current_playback()
if pb and pb.get('is_playing'):
    print(f"ESTÁ REPRODUCIENDO: {pb['item']['name']}")
else:
    print("NO ESTÁ REPRODUCIENDO NADA.")
