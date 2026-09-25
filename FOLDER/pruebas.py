import os

# --- BASE DE DATOS EN TEXTO PLANO ---
ARCHIVO_DB = "inventario.txt"

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

    def to_string(self):
        return f"General,{self.id},{self.nombre},{self.cantidad},{self.ubicacion}"


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

    def to_string(self):
        return f"Resistencia,{self.id},{self.nombre},{self.cantidad},{self.ubicacion},{self.valor_ohmios},{self.tolerancia}"


class Condensador(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, capacitancia, voltaje_max):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.capacitancia = capacitancia
        self.voltaje_max = voltaje_max

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Condensador] Capacitancia: {self.capacitancia} | Voltaje Máx: {self.voltaje_max}V"

    def to_string(self):
        return f"Condensador,{self.id},{self.nombre},{self.cantidad},{self.ubicacion},{self.capacitancia},{self.voltaje_max}"


class Bobina(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, inductancia, corriente_max):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.inductancia = inductancia
        self.corriente_max = corriente_max

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Bobina] Inductancia: {self.inductancia} | Corriente Máx: {self.corriente_max}A"

    def to_string(self):
        return f"Bobina,{self.id},{self.nombre},{self.cantidad},{self.ubicacion},{self.inductancia},{self.corriente_max}"


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

    def to_string(self):
        return f"Diodo,{self.id},{self.nombre},{self.cantidad},{self.ubicacion},{self.tipo_diodo},{self.corriente_max}"


class Transistor(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, tipo_transistor, encapsulado):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.tipo_transistor = tipo_transistor  # BJT o MOSFET
        self.encapsulado = encapsulado

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} |  [Transistor] Tipo: {self.tipo_transistor} | Encapsulado: {self.encapsulado}"

    def to_string(self):
        return f"Transistor,{self.id},{self.nombre},{self.cantidad},{self.ubicacion},{self.tipo_transistor},{self.encapsulado}"


class CircuitoIntegrado(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, numero_pines, funcion):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.numero_pines = numero_pines
        self.funcion = funcion

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} |  [Circuito Integrado] Pines: {self.numero_pines} | Función: {self.funcion}"

    def to_string(self):
        return f"CircuitoIntegrado,{self.id},{self.nombre},{self.cantidad},{self.ubicacion},{self.numero_pines},{self.funcion}"


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

    def to_string(self):
        return f"Microcontrolador,{self.id},{self.nombre},{self.cantidad},{self.ubicacion},{self.voltaje_operacion},{self.velocidad_reloj}"


class Sensor(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, magnitud_medida, interfaz):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.magnitud_medida = magnitud_medida  

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} |  [Sensor] Mide: {self.magnitud_medida} | Interfaz: {self.interfaz}"

    def to_string(self):
        return f"Sensor,{self.id},{self.nombre},{self.cantidad},{self.ubicacion},{self.magnitud_medida},{self.interfaz}"


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
        return f"{base} |  [Instrumento] Marca: {self.marca} | Rango/Precisión: {self.precision_o_rango}"

    def to_string(self):
        return f"InstrumentoLab,{self.id},{self.nombre},{self.cantidad},{self.ubicacion},{self.marca},{self.precision_o_rango}"


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
# --- SECCIÓN: CONTROLADOR Y PERSISTENCIA ---
# =====================================================================
class SistemaInventario:
    def __init__(self):
        self.inventario = []
        self.cargar_desde_archivo()

    def agregar_item(self, item):
        self.inventario.append(item)
        self.guardar_en_archivo()
        print(f" ¡{item.nombre} registrado correctamente en el inventario!")

    def eliminar_item(self, id_item):
        encontrado = False
        for item in self.inventario:
            if item.id == id_item:
                self.inventario.remove(item)
                encontrado = True
                break
        
        if encontrado:
            self.guardar_en_archivo()
            print(f"Elemento con ID '{id_item}' eliminado correctamente.")
        else:
            print(f"No se encontró ningún elemento con el ID '{id_item}'.")

    def mostrar_inventario(self):
        if not self.inventario:
            print("\n📭 El inventario está vacío.")
            return
        
        print("\n--- INVENTARIO DETALLADO DEL LABORATORIO ---")
        for item in self.inventario:
            print(item.obtener_detalles())
        print("---------------------------------------------")

    def guardar_en_archivo(self):
        with open(ARCHIVO_DB, "w", encoding="utf-8") as f:
            for item in self.inventario:
                f.write(item.to_string() + "\n")

    def cargar_desde_archivo(self):
        if not os.path.exists(ARCHIVO_DB):
            return
        
        self.inventario = []
        with open(ARCHIVO_DB, "r", encoding="utf-8") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if not datos or datos[0] == "":
                    continue
                
                tipo = datos[0]
                # Reconstrucción de cada objeto según su clase exacta al leer el .txt
                if tipo == "Resistencia":
                    item = Resistencia(datos[1], datos[2], datos[3], datos[4], datos[5], datos[6])
                elif tipo == "Condensador":
                    item = Condensador(datos[1], datos[2], datos[3], datos[4], datos[5], datos[6])
                elif tipo == "Bobina":
                    item = Bobina(datos[1], datos[2], datos[3], datos[4], datos[5], datos[6])
                elif tipo == "Diodo":
                    item = Diodo(datos[1], datos[2], datos[3], datos[4], datos[5], datos[6])
                elif tipo == "Transistor":
                    item = Transistor(datos[1], datos[2], datos[3], datos[4], datos[5], datos[6])
                elif tipo == "CircuitoIntegrado":
                    item = CircuitoIntegrado(datos[1], datos[2], datos[3], datos[4], datos[5], datos[6])
                elif tipo == "Microcontrolador":
                    item = Microcontrolador(datos[1], datos[2], datos[3], datos[4], datos[5], datos[6])
                elif tipo == "Sensor":
                    item = Sensor(datos[1], datos[2], datos[3], datos[4], datos[5], datos[6])
                elif tipo == "InstrumentoLab":
                    item = InstrumentoLab(datos[1], datos[2], datos[3], datos[4], datos[5], datos[6])
                else:
                    item = ComponenteElectronico(datos[1], datos[2], datos[3], datos[4])
                
                self.inventario.append(item)


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
            print("Opción inválida.")

if __name__ == "__main__":
    main()