import zipfile
import os

print("Empaquetando Jarvis (Modo Ultra Rápido)...")
with zipfile.ZipFile('Jarvis_Pendrive.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('.'):
        # Ignorar carpetas extremadamente pesadas y cachés
        if 'venv' in dirs: dirs.remove('venv')
        if '__pycache__' in dirs: dirs.remove('__pycache__')
        if '.git' in dirs: dirs.remove('.git')
        
        for file in files:
            if file.endswith('.zip') or file == 'empaquetador_rapido.py': 
                continue
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, '.'))
            
print("¡Archivo Jarvis_Pendrive.zip creado con éxito en tan solo unos segundos!")
