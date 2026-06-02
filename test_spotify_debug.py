import sys
import os

# Añadir el path al sys para poder importar tools_spotify
sys.path.append(r"e:\Proyecto-IALOCAL")

from tools_spotify import controlar_playback

print("--- TEST SPOTIFY ---")
resultado = controlar_playback("buscar_y_reproducir", "Himno Nacional Argentino")
print("RESULTADO DE LA TOOL:", resultado)
print("--------------------")
