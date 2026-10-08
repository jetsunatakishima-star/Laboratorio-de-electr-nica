import sqlite3

# --- BASE DE DATOS SQLITE ---
ARCHIVO_DB = "inventario.db"

# =====================================================================
# --- SECCIÓN: CLASE PADRE (Componente Electrónico General) ---
# =====================================================================
class ComponenteElectronico:
    def __init__(self, id_item, nombre, cantidad, ubicacion):
        self.id = id_item
        self.nombre = nombre
        self.cantidad = int(cantidad)
        self.ubicacion = ubicacion

    def obtener_detalles(self):
        return f"ID: {self.id} | {self.nombre} | Cantidad: {self.cantidad} | Ubicación: {self.ubicacion}"

    def get_db_data(self):
        return ("General", None, None)


# =====================================================================
# --- SECCIÓN: CLASES HIJAS (COMPONENTES PASIVOS) ---
# =====================================================================
class Resistencia(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, valor_ohmios, tolerancia):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.valor_ohmios = valor_ohmios
        self.tolerancia = tolerancia

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Resistencia] Valor: {self.valor_ohmios} | Tolerancia: {self.tolerancia}%"

    def get_db_data(self):
        return ("Resistencia", self.valor_ohmios, self.tolerancia)


class Condensador(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, capacitancia, voltaje_max):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.capacitancia = capacitancia
        self.voltaje_max = voltaje_max

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Condensador] Capacitancia: {self.capacitancia} | Voltaje Máx: {self.voltaje_max}V"

    def get_db_data(self):
        return ("Condensador", self.capacitancia, self.voltaje_max)


class Bobina(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, inductancia, corriente_max):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.inductancia = inductancia
        self.corriente_max = corriente_max

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Bobina] Inductancia: {self.inductancia} | Corriente Máx: {self.corriente_max}A"

    def get_db_data(self):
        return ("Bobina", self.inductancia, self.corriente_max)


# =====================================================================
# --- SECCIÓN: CLASES HIJAS (COMPONENTES ACTIVOS) ---
# =====================================================================
class Diodo(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, tipo_diodo, corriente_max):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.tipo_diodo = tipo_diodo
        self.corriente_max = corriente_max

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Diodo] Tipo: {self.tipo_diodo} | Corriente Máx: {self.corriente_max}A"

    def get_db_data(self):
        return ("Diodo", self.tipo_diodo, self.corriente_max)


class Transistor(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, tipo_transistor, encapsulado):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.tipo_transistor = tipo_transistor  # BJT o MOSFET
        self.encapsulado = encapsulado

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Transistor] Tipo: {self.tipo_transistor} | Encapsulado: {self.encapsulado}"

    def get_db_data(self):
        return ("Transistor", self.tipo_transistor, self.encapsulado)


class CircuitoIntegrado(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, numero_pines, funcion):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.numero_pines = numero_pines
        self.funcion = funcion

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Circuito Integrado] Pines: {self.numero_pines} | Función: {self.funcion}"

    def get_db_data(self):
        return ("CircuitoIntegrado", self.numero_pines, self.funcion)


# =====================================================================
# --- SECCIÓN: CLASES HIJAS (PLACAS Y SISTEMAS) ---
# =====================================================================
class Microcontrolador(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, voltaje_operacion, velocidad_reloj):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.voltaje_operacion = voltaje_operacion
        self.velocidad_reloj = velocidad_reloj

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Microcontrolador] Voltaje: {self.voltaje_operacion}V | Reloj: {self.velocidad_reloj}"

    def get_db_data(self):
        return ("Microcontrolador", self.voltaje_operacion, self.velocidad_reloj)


class Sensor(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, magnitud_medida, interfaz):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.magnitud_medida = magnitud_medida  
        self.interfaz = interfaz

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Sensor] Mide: {self.magnitud_medida} | Interfaz: {self.interfaz}"

    def get_db_data(self):
        return ("Sensor", self.magnitud_medida, self.interfaz)


# =====================================================================
# --- SECCIÓN: CLASES HIJAS (INSTRUMENTOS DE LABORATORIO) ---
# =====================================================================
class InstrumentoLab(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, marca, precision_o_rango):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.marca = marca
        self.precision_o_rango = precision_o_rango

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Instrumento] Marca: {self.marca} | Rango/Precisión: {self.precision_o_rango}"

    def get_db_data(self):
        return ("InstrumentoLab", self.marca, self.precision_o_rango)


# =====================================================================
# --- SECCIÓN: USUARIOS (ROLES) ---
# =====================================================================
class Usuario:
    def __init__(self, nombre, carnet):
        self.nombre = nombre
        self.carnet = carnet

    def mostrar_menu_rol(self, sistema):
        pass


class Estudiante(Usuario):
    def __init__(self, nombre, carnet, carrera):
        super().__init__(nombre, carnet)
        self.carrera = carrera

    def mostrar_menu_rol(self, sistema):
        while True:
            print(f"\n MÓDULO ESTUDIANTE: {self.nombre} ({self.carrera})")
            print("1. Ver Inventario Completo del Laboratorio")
            print("2. Cerrar Sesión")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                sistema.mostrar_inventario()
            elif opcion == "2":
                break
            else:
                print(" Opción no válida.")


class Encargado(Usuario):
    def __init__(self, nombre, carnet, cubiculo):
        super().__init__(nombre, carnet)
        self.cubiculo = cubiculo

    def mostrar_menu_rol(self, sistema):
        while True:
            print(f"\n MÓDULO ENCARGADO: {self.nombre} (Cubículo: {self.cubiculo})")
            print("--- AGREGAR COMPONENTE ESPECÍFICO ---")
            print("1. Registrar Resistencia")
            print("2. Registrar Condensador")
            print("3. Registrar Bobina")
            print("4. Registrar Diodo")
            print("5. Registrar Transistor")
            print("6. Registrar Circuito Integrado (IC)")
            print("7. Registrar Microcontrolador")
            print("8. Registrar Sensor")
            print("9. Registrar Instrumento de Medición (Multímetro/Osciloscopio)")
            print("10. Eliminar Componente por ID")
            print("11. Ver Inventario Completo")
            print("12. Cerrar Sesión")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                sistema.agregar_item(Resistencia(
                    input("ID: "), input("Nombre: "), input("Cantidad: "), input("Ubicación: "),
                    input("Valor en Ohmios (ej. 220Ω, 10kΩ): "), input("Tolerancia (ej. 5%): ")
                ))
            elif opcion == "2":
                sistema.agregar_item(Condensador(
                    input("ID: "), input("Nombre: "), input("Cantidad: "), input("Ubicación: "),
                    input("Capacitancia (ej. 100uF, 22pF): "), input("Voltaje Máximo (ej. 50V): ")
                ))
            elif opcion == "3":
                sistema.agregar_item(Bobina(
                    input("ID: "), input("Nombre: "), input("Cantidad: "), input("Ubicación: "),
                    input("Inductancia (ej. 10mH): "), input("Corriente Máx (ej. 1A): ")
                ))
            elif opcion == "4":
                sistema.agregar_item(Diodo(
                    input("ID: "), input("Nombre: "), input("Cantidad: "), input("Ubicación: "),
                    input("Tipo de Diodo (ej. LED, Zener, Rectificador): "), input("Corriente Máx: ")
                ))
            elif opcion == "5":
                sistema.agregar_item(Transistor(
                    input("ID: "), input("Nombre: "), input("Cantidad: "), input("Ubicación: "),
                    input("Tipo (ej. BJT o MOSFET): "), input("Encapsulado (ej. TO-92, TO-220): ")
                ))
            elif opcion == "6":
                sistema.agregar_item(CircuitoIntegrado(
                    input("ID: "), input("Nombre: "), input("Cantidad: "), input("Ubicación: "),
                    input("Número de pines (ej. 8, 14, 40): "), input("Función principal (ej. Compuerta AND, Amplificador): ")
                ))
            elif opcion == "7":
                sistema.agregar_item(Microcontrolador(
                    input("ID: "), input("Nombre: "), input("Cantidad: "), input("Ubicación: "),
                    input("Voltaje de operación (ej. 3.3V / 5V): "), input("Velocidad de reloj (ej. 16MHz): ")
                ))
            elif opcion == "8":
                sistema.agregar_item(Sensor(
                    input("ID: "), input("Nombre: "), input("Cantidad: "), input("Ubicación: "),
                    input("Magnitud que mide (ej. Temperatura, Distancia): "), input("Interfaz de comunicación (ej. I2C, Analógico): ")
                ))
            elif opcion == "9":
                sistema.agregar_item(InstrumentoLab(
                    input("ID: "), input("Nombre: "), input("Cantidad: "), input("Ubicación: "),
                    input("Marca (ej. Fluke, Rigol): "), input("Precisión o Rango: ")
                ))
            elif opcion == "10":
                sistema.eliminar_item(input("Ingrese el ID del componente a eliminar: "))
            elif opcion == "11":
                sistema.mostrar_inventario()
            elif opcion == "12":
                break
            else:
                print(" Opción no válida.")


# =====================================================================
# --- SECCIÓN: CONTROLADOR Y PERSISTENCIA (SQLITE) ---
# =====================================================================
class SistemaInventario:
    def __init__(self):
        self.inicializar_db()

    def inicializar_db(self):
        conn = sqlite3.connect(ARCHIVO_DB)
        cursor = conn.cursor()
        cursor.execute('''
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
        conn.commit()
        conn.close()

    def agregar_item(self, item):
        conn = sqlite3.connect(ARCHIVO_DB)
        cursor = conn.cursor()
        tipo, attr1, attr2 = item.get_db_data()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO componentes (id, tipo, nombre, cantidad, ubicacion, attr1, attr2)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (item.id, tipo, item.nombre, item.cantidad, item.ubicacion, attr1, attr2))
            conn.commit()
            print(f" ¡{item.nombre} registrado correctamente en la base de datos!")
        except sqlite3.Error as e:
            print(f" Error al registrar en la base de datos: {e}")
        finally:
            conn.close()

    def eliminar_item(self, id_item):
        conn = sqlite3.connect(ARCHIVO_DB)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM componentes WHERE id = ?", (id_item,))
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f" Elemento con ID '{id_item}' eliminado correctamente.")
        else:
            print(f" No se encontró ningún elemento con el ID '{id_item}'.")
        conn.close()

    def mostrar_inventario(self):
        conn = sqlite3.connect(ARCHIVO_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo, nombre, cantidad, ubicacion, attr1, attr2 FROM componentes")
        filas = cursor.fetchall()
        conn.close()

        if not filas:
            print("\n📭 El inventario está vacío.")
            return
        
        print("\n--- INVENTARIO DETALLADO DEL LABORATORIO (SQLITE) ---")
        for row in filas:
            item = self._crear_instancia(row)
            if item:
                print(item.obtener_detalles())
        print("-----------------------------------------------------")

    def _crear_instancia(self, row):
        id_item, tipo, nombre, cantidad, ubicacion, attr1, attr2 = row
        if tipo == "Resistencia":
            return Resistencia(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        elif tipo == "Condensador":
            return Condensador(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        elif tipo == "Bobina":
            return Bobina(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        elif tipo == "Diodo":
            return Diodo(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        elif tipo == "Transistor":
            return Transistor(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        elif tipo == "CircuitoIntegrado":
            return CircuitoIntegrado(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        elif tipo == "Microcontrolador":
            return Microcontrolador(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        elif tipo == "Sensor":
            return Sensor(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        elif tipo == "InstrumentoLab":
            return InstrumentoLab(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        else:
            return ComponenteElectronico(id_item, nombre, cantidad, ubicacion)


# =====================================================================
# --- EJECUCIÓN PRINCIPAL ---
# =====================================================================
def main():
    sistema = SistemaInventario()
    
    while True:
        print("\n=== SISTEMA DE GESTIÓN - LAB DE ELECTRÓNICA ===")
        print("1. Ingresar como Estudiante")
        print("2. Ingresar como Encargado de Laboratorio")
        print("3. Salir")
        
        rol = input("Seleccione una opción: ")
        
        if rol == "1":
            usuario = Estudiante(input("Nombre: "), input("Carnet: "), input("Carrera: "))
            usuario.mostrar_menu_rol(sistema)
        elif rol == "2":
            usuario = Encargado(input("Nombre: "), input("Código empleado: "), input("Cubículo: "))
            usuario.mostrar_menu_rol(sistema)
        elif rol == "3":
            print(" Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print(" Opción inválida.")

if __name__ == "__main__":
    main()
    
