import os

# Carpeta donde están estos archivos .py
CARPETA = os.path.dirname(os.path.abspath(__file__))

# La base de datos vive en la subcarpeta "db" (se crea sola si no existe)
CARPETA_DB = os.path.join(CARPETA, "db")
os.makedirs(CARPETA_DB, exist_ok=True)

ARCHIVO_DB = os.path.join(CARPETA_DB, "inventario.db")