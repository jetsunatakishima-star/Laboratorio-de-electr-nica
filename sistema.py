import sqlite3 as sql
from contextlib import contextmanager
from datetime import datetime

from config import ARCHIVO_DB
from componentes import (
    ComponenteElectronico, Resistencia, Condensador, Bobina, Diodo,
    Transistor, CircuitoIntegrado, Microcontrolador, Sensor, InstrumentoLab,
)

CLASES = {
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


class SistemaInventario:
    def __init__(self):
        self.inicializar_db()  # crea el archivo .db y las tablas al iniciar

    @contextmanager
    def _conexion(self):
        """Abre una conexión, confirma los cambios y la CIERRA al terminar."""
        conn = sql.connect(ARCHIVO_DB)
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def inicializar_db(self):
        with self._conexion() as conn:
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
            conn.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rol TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    carnet TEXT NOT NULL,
                    extra TEXT,
                    primer_ingreso TEXT,
                    ultimo_ingreso TEXT,
                    total_ingresos INTEGER DEFAULT 1,
                    UNIQUE (rol, carnet)
                )
            ''')

    # ================= USUARIOS =================
    def guardar_usuario(self, usuario):
        """Guarda al usuario si es nuevo o actualiza su último ingreso.
        Devuelve True si era nuevo y False si ya existía.
        Lanza sqlite3.Error si algo falla en la base de datos."""
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._conexion() as conn:
            existe = conn.execute(
                "SELECT 1 FROM usuarios WHERE rol = ? AND carnet = ?",
                (usuario.rol, usuario.carnet)
            ).fetchone()

            if existe:
                conn.execute('''
                    UPDATE usuarios
                    SET nombre = ?, extra = ?, ultimo_ingreso = ?,
                        total_ingresos = total_ingresos + 1
                    WHERE rol = ? AND carnet = ?
                ''', (usuario.nombre, usuario.extra, ahora,
                      usuario.rol, usuario.carnet))
                return False

            conn.execute('''
                INSERT INTO usuarios
                (rol, nombre, carnet, extra, primer_ingreso, ultimo_ingreso)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (usuario.rol, usuario.nombre, usuario.carnet,
                  usuario.extra, ahora, ahora))
            return True

    def listar_usuarios(self):
        """Devuelve una lista de tuplas:
        (rol, nombre, carnet, extra, primer_ingreso, ultimo_ingreso, total_ingresos)."""
        with self._conexion() as conn:
            return conn.execute('''
                SELECT rol, nombre, carnet, extra, primer_ingreso,
                       ultimo_ingreso, total_ingresos
                FROM usuarios ORDER BY ultimo_ingreso DESC
            ''').fetchall()

    # --- versiones de consola (se mantienen para main_consola.py) ---
    def registrar_usuario(self, usuario):
        try:
            if self.guardar_usuario(usuario):
                print(f" Usuario {usuario.nombre} registrado por primera vez.")
            else:
                print(f" Bienvenido de nuevo, {usuario.nombre}.")
        except sql.Error as e:
            print(f" Error al registrar el usuario: {e}")

    def mostrar_usuarios(self):
        filas = self.listar_usuarios()
        if not filas:
            print("\n No hay usuarios registrados todavía.")
            return

        print("\n--- USUARIOS REGISTRADOS (SQLITE) ---")
        for rol, nombre, carnet, extra, primero, ultimo, total in filas:
            print(f"[{rol}] {nombre} | ID: {carnet} | {extra} | "
                  f"Primer ingreso: {primero} | Último: {ultimo} | Ingresos: {total}")
        print("-------------------------------------")

    # ================= COMPONENTES =================
    def existe_item(self, id_item):
        with self._conexion() as conn:
            return conn.execute(
                "SELECT 1 FROM componentes WHERE id = ?", (id_item,)
            ).fetchone() is not None

    def guardar_item(self, item):
        """Inserta o reemplaza un componente. Lanza sqlite3.Error si falla."""
        tipo, attr1, attr2 = item.get_db_data()
        with self._conexion() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO componentes
                (id, tipo, nombre, cantidad, ubicacion, attr1, attr2)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (item.id, tipo, item.nombre, item.cantidad,
                  item.ubicacion, attr1, attr2))

    def borrar_item(self, id_item):
        """Elimina un componente. Devuelve True si existía."""
        with self._conexion() as conn:
            cursor = conn.execute("DELETE FROM componentes WHERE id = ?", (id_item,))
            return cursor.rowcount > 0

    def listar_componentes(self):
        """Devuelve una lista de objetos ComponenteElectronico (o subclases)."""
        with self._conexion() as conn:
            filas = conn.execute(
                "SELECT id, tipo, nombre, cantidad, ubicacion, attr1, attr2 FROM componentes"
            ).fetchall()
        return [self._crear_instancia(fila) for fila in filas]

    # --- versiones de consola (se mantienen para main_consola.py) ---
    def agregar_item(self, item):
        try:
            self.guardar_item(item)
            print(f" ¡{item.nombre} registrado correctamente en la base de datos!")
        except sql.Error as e:
            print(f" Error al registrar en la base de datos: {e}")

    def eliminar_item(self, id_item):
        if self.borrar_item(id_item):
            print(f" Elemento con ID '{id_item}' eliminado correctamente.")
        else:
            print(f" No se encontró ningún elemento con el ID '{id_item}'.")

    def mostrar_inventario(self):
        items = self.listar_componentes()
        if not items:
            print("\n El inventario está vacío.")
            return

        print("\n--- INVENTARIO DETALLADO DEL LABORATORIO (SQLITE) ---")
        for item in items:
            print(item.obtener_detalles())
        print("-----------------------------------------------------")

    def _crear_instancia(self, row):
        id_item, tipo, nombre, cantidad, ubicacion, attr1, attr2 = row
        clase = CLASES.get(tipo)
        if clase:
            return clase(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        return ComponenteElectronico(id_item, nombre, cantidad, ubicacion)