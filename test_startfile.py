import os
import sys
import time

track_uri = "spotify:track:0bYg9bo50gSsH3LtXe2SQn" # All I Want for Christmas Is You, just an example

print(f"Lanzando uri: {track_uri}")
try:
    os.startfile(track_uri)
    print("Enviado. Esperando 5 segundos a ver si reproduce...")
    time.sleep(5)
    print("Test completado.")
except Exception as e:
    print(f"Error: {e}")
