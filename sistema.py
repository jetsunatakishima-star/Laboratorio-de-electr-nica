import sqlite3 as sql

from config import ARCHIVO_DB
from componentes import (
    ComponenteElectronico, Resistencia, Condensador, Bobina, Diodo,
    Transistor, CircuitoIntegrado, Microcontrolador, Sensor, InstrumentoLab,
)


class SistemaInventario:
    def __init__(self):
        self.inicializar_db()  # crea el archivo .db y la tabla al iniciar

    def inicializar_db(self):
        print(f"Base de datos en: {ARCHIVO_DB}")
        with sql.connect(ARCHIVO_DB) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS componentes (
                    id TEXT PRIMARY KEY,
                    tipo TEXT,
                    nombre TEXT,
                    cantidad INTEGER,
                    ubicacion TEXT,
                    attr1 TEXT,
                    attr2 TEXT
                )
            ''')

    def agregar_item(self, item):
        tipo, attr1, attr2 = item.get_db_data()
        try:
            with sql.connect(ARCHIVO_DB) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO componentes
                    (id, tipo, nombre, cantidad, ubicacion, attr1, attr2)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (item.id, tipo, item.nombre, item.cantidad,
                      item.ubicacion, attr1, attr2))
            print(f" ¡{item.nombre} registrado correctamente en la base de datos!")
        except sql.Error as e:
            print(f" Error al registrar en la base de datos: {e}")

    def eliminar_item(self, id_item):
        with sql.connect(ARCHIVO_DB) as conn:
            cursor = conn.execute("DELETE FROM componentes WHERE id = ?", (id_item,))
            eliminados = cursor.rowcount

        if eliminados > 0:
            print(f" Elemento con ID '{id_item}' eliminado correctamente.")
        else:
            print(f" No se encontró ningún elemento con el ID '{id_item}'.")

    def mostrar_inventario(self):
        with sql.connect(ARCHIVO_DB) as conn:
            filas = conn.execute(
                "SELECT id, tipo, nombre, cantidad, ubicacion, attr1, attr2 FROM componentes"
            ).fetchall()

        if not filas:
            print("\n El inventario está vacío.")
            return

        print("\n--- INVENTARIO DETALLADO DEL LABORATORIO (SQLITE) ---")
        for row in filas:
            item = self._crear_instancia(row)
            if item:
                print(item.obtener_detalles())
        print("-----------------------------------------------------")

    def _crear_instancia(self, row):
        id_item, tipo, nombre, cantidad, ubicacion, attr1, attr2 = row
        clases = {
            "Resistencia": Resistencia,
            "Condensador": Condensador,
            "Bobina": Bobina,
            "Diodo": Diodo,
            "Transistor": Transistor,
            "CircuitoIntegrado": CircuitoIntegrado,
            "Microcontrolador": Microcontrolador,
            "Sensor": Sensor,
            "InstrumentoLab": InstrumentoLab,
        }
        clase = clases.get(tipo)
        if clase:
            return clase(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        return ComponenteElectronico(id_item, nombre, cantidad, ubicacion)