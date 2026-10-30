import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from sistema import SistemaInventario
from usuarios import Estudiante, Encargado
from componentes import (
    Resistencia, Condensador, Bobina, Diodo, Transistor,
    CircuitoIntegrado, Microcontrolador, Sensor, InstrumentoLab,
)

# nombre en la BD -> (clase, nombre para mostrar, etiqueta campo 1, etiqueta campo 2)
TIPOS = {
    "Resistencia": (Resistencia, "Resistencia",
                    "Valor en ohmios (ej. 220Ω, 10kΩ)", "Tolerancia % (ej. 5)"),
    "Condensador": (Condensador, "Condensador",
                    "Capacitancia (ej. 100uF, 22pF)", "Voltaje máximo (ej. 50)"),
    "Bobina": (Bobina, "Bobina",
               "Inductancia (ej. 10mH)", "Corriente máx. (ej. 1)"),
    "Diodo": (Diodo, "Diodo",
              "Tipo (ej. LED, Zener, Rectificador)", "Corriente máx."),
    "Transistor": (Transistor, "Transistor",
                   "Tipo (BJT o MOSFET)", "Encapsulado (ej. TO-92, TO-220)"),
    "CircuitoIntegrado": (CircuitoIntegrado, "Circuito integrado",
                          "Número de pines (ej. 8, 14, 40)", "Función principal"),
    "Microcontrolador": (Microcontrolador, "Microcontrolador",
                         "Voltaje de operación (ej. 3.3 / 5)", "Velocidad de reloj (ej. 16MHz)"),
    "Sensor": (Sensor, "Sensor",
               "Magnitud que mide (ej. Temperatura)", "Interfaz (ej. I2C, Analógico)"),
    "InstrumentoLab": (InstrumentoLab, "Instrumento de medición",
                       "Marca (ej. Fluke, Rigol)", "Precisión o rango"),
}
NOMBRE_A_TIPO = {datos[1]: tipo for tipo, datos in TIPOS.items()}
TIPO_A_NOMBRE = {tipo: datos[1] for tipo, datos in TIPOS.items()}


# ---------------------------------------------------------------- LOGIN
class LoginFrame(ttk.Frame):
    ETIQUETAS = {
        "Estudiante": ("Nombre:", "Carnet:", "Carrera:"),
        "Encargado": ("Nombre:", "Código de empleado:", "Cubículo:"),
    }

    def __init__(self, app):
        super().__init__(app, padding=30)
        self.app = app
        self.rol = tk.StringVar(value="Estudiante")

        ttk.Label(self, text="Laboratorio de Electrónica",
                  font=("Segoe UI", 20, "bold")).pack(pady=(30, 4))
        ttk.Label(self, text="Sistema de gestión de inventario").pack(pady=(0, 24))

        caja = ttk.Frame(self)
        caja.pack()

        fila_rol = ttk.Frame(caja)
        fila_rol.grid(row=0, column=0, columnspan=2, pady=(0, 14))
        ttk.Label(fila_rol, text="Ingresar como:").pack(side="left", padx=(0, 10))
        for rol in self.ETIQUETAS:
            ttk.Radiobutton(fila_rol, text=rol, value=rol, variable=self.rol,
                            command=self._actualizar_etiquetas).pack(side="left", padx=8)

        self.etiquetas = []
        self.entradas = []
        for i in range(3):
            etiqueta = ttk.Label(caja)
            etiqueta.grid(row=i + 1, column=0, sticky="e", padx=(0, 8), pady=5)
            entrada = ttk.Entry(caja, width=34)
            entrada.grid(row=i + 1, column=1, pady=5)
            entrada.bind("<Return>", lambda e: self.ingresar())
            self.etiquetas.append(etiqueta)
            self.entradas.append(entrada)

        ttk.Button(caja, text="Ingresar", command=self.ingresar).grid(
            row=4, column=0, columnspan=2, pady=18)
        ttk.Button(caja, text="Salir", command=app.destroy).grid(
            row=5, column=0, columnspan=2)

        self._actualizar_etiquetas()
        self.entradas[0].focus_set()

    def _actualizar_etiquetas(self):
        for etiqueta, texto in zip(self.etiquetas, self.ETIQUETAS[self.rol.get()]):
            etiqueta.config(text=texto)

    def ingresar(self):
        nombre, carnet, extra = (e.get().strip() for e in self.entradas)
        if not (nombre and carnet and extra):
            messagebox.showwarning("Datos incompletos", "Complete todos los campos.")
            return

        if self.rol.get() == "Estudiante":
            usuario = Estudiante(nombre, carnet, extra)
        else:
            usuario = Encargado(nombre, carnet, extra)

        try:
            es_nuevo = self.app.sistema.guardar_usuario(usuario)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario:\n{e}")
            return

        self.app.mostrar_sesion(usuario, es_nuevo)


# ---------------------------------------------------------------- INVENTARIO
class InventarioTab(ttk.Frame):
    COLUMNAS = (
        ("id", "ID", 90), ("tipo", "Tipo", 130), ("nombre", "Nombre", 180),
        ("cantidad", "Cantidad", 70), ("ubicacion", "Ubicación", 120),
        ("specs", "Especificaciones", 320),
    )

    def __init__(self, master, sistema, puede_eliminar=False):
        super().__init__(master, padding=10)
        self.sistema = sistema

        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(0, 8))

        ttk.Label(barra, text="Buscar:").pack(side="left")
        self.busqueda = tk.StringVar()
        ttk.Entry(barra, textvariable=self.busqueda, width=26).pack(side="left", padx=6)

        ttk.Label(barra, text="Tipo:").pack(side="left", padx=(12, 0))
        self.filtro = tk.StringVar(value="Todos")
        combo = ttk.Combobox(barra, textvariable=self.filtro, state="readonly", width=22,
                             values=["Todos"] + list(NOMBRE_A_TIPO))
        combo.pack(side="left", padx=6)

        ttk.Button(barra, text="Actualizar", command=self.refrescar).pack(side="right")
        if puede_eliminar:
            ttk.Button(barra, text="Eliminar seleccionados",
                       command=self.eliminar).pack(side="right", padx=6)

        marco = ttk.Frame(self)
        marco.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(marco, columns=[c[0] for c in self.COLUMNAS],
                                 show="headings", selectmode="extended")
        for clave, titulo, ancho in self.COLUMNAS:
            self.tree.heading(clave, text=titulo)
            self.tree.column(clave, width=ancho, anchor="center" if clave == "cantidad" else "w")
        scroll = ttk.Scrollbar(marco, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.lbl_total = ttk.Label(self, text="")
        self.lbl_total.pack(anchor="w", pady=(8, 0))

        self.busqueda.trace_add("write", lambda *a: self.refrescar())
        combo.bind("<<ComboboxSelected>>", lambda e: self.refrescar())
        self.refrescar()

    def refrescar(self):
        texto = self.busqueda.get().strip().lower()
        filtro = self.filtro.get()
        tipo_filtro = None if filtro == "Todos" else NOMBRE_A_TIPO[filtro]

        self.tree.delete(*self.tree.get_children())
        mostrados = 0
        for item in self.sistema.listar_componentes():
            tipo = item.get_db_data()[0]
            if tipo_filtro and tipo != tipo_filtro:
                continue
            # obtener_detalles() = 4 campos base | [Tipo] campo1 | campo2
            specs = " | ".join(item.obtener_detalles().split(" | ")[4:])
            fila = (item.id, TIPO_A_NOMBRE.get(tipo, tipo), item.nombre,
                    item.cantidad, item.ubicacion, specs)
            if texto and texto not in " ".join(str(v) for v in fila).lower():
                continue
            # iid = id del componente (evita que Tk convierta "001" en 1)
            self.tree.insert("", "end", iid=item.id, values=fila)
            mostrados += 1
        self.lbl_total.config(text=f"{mostrados} elemento(s)")

    def eliminar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Eliminar", "Seleccione al menos un componente.")
            return
        if not messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Eliminar {len(seleccion)} componente(s)? Esta acción no se puede deshacer."):
            return
        for id_item in seleccion:
            self.sistema.borrar_item(id_item)
        self.refrescar()


# ---------------------------------------------------------------- AGREGAR
class AgregarTab(ttk.Frame):
    def __init__(self, master, sistema, al_guardar):
        super().__init__(master, padding=20)
        self.sistema = sistema
        self.al_guardar = al_guardar

        self.tipo = tk.StringVar(value=TIPO_A_NOMBRE["Resistencia"])
        ttk.Label(self, text="Tipo de componente:").grid(row=0, column=0, sticky="e", padx=(0, 8), pady=6)
        combo = ttk.Combobox(self, textvariable=self.tipo, state="readonly", width=30,
                             values=list(NOMBRE_A_TIPO))
        combo.grid(row=0, column=1, sticky="w", pady=6)
        combo.bind("<<ComboboxSelected>>", lambda e: self._actualizar_etiquetas())

        fijas = ["ID:", "Nombre:", "Cantidad:", "Ubicación:"]
        self.etiquetas = []
        self.entradas = []
        for i in range(6):
            etiqueta = ttk.Label(self, text=fijas[i] if i < 4 else "")
            etiqueta.grid(row=i + 1, column=0, sticky="e", padx=(0, 8), pady=6)
            entrada = ttk.Entry(self, width=36)
            entrada.grid(row=i + 1, column=1, sticky="w", pady=6)
            self.etiquetas.append(etiqueta)
            self.entradas.append(entrada)

        botones = ttk.Frame(self)
        botones.grid(row=7, column=0, columnspan=2, pady=16)
        ttk.Button(botones, text="Guardar componente", command=self.guardar).pack(side="left", padx=6)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=6)

        self._actualizar_etiquetas()

    def _actualizar_etiquetas(self):
        _, _, etiqueta1, etiqueta2 = TIPOS[NOMBRE_A_TIPO[self.tipo.get()]]
        self.etiquetas[4].config(text=etiqueta1 + ":")
        self.etiquetas[5].config(text=etiqueta2 + ":")

    def limpiar(self):
        for entrada in self.entradas:
            entrada.delete(0, "end")
        self.entradas[0].focus_set()

    def guardar(self):
        id_item, nombre, cantidad, ubicacion, attr1, attr2 = (e.get().strip() for e in self.entradas)

        if not all((id_item, nombre, cantidad, ubicacion, attr1, attr2)):
            messagebox.showwarning("Datos incompletos", "Complete todos los campos.")
            return
        try:
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Cantidad inválida", "La cantidad debe ser un número entero.")
            return
        if cantidad < 0:
            messagebox.showerror("Cantidad inválida", "La cantidad no puede ser negativa.")
            return

        if self.sistema.existe_item(id_item):
            if not messagebox.askyesno(
                    "ID existente",
                    f"Ya existe un componente con ID '{id_item}'.\n¿Desea reemplazarlo?"):
                return

        clase = TIPOS[NOMBRE_A_TIPO[self.tipo.get()]][0]
        item = clase(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        try:
            self.sistema.guardar_item(item)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo guardar en la base de datos:\n{e}")
            return

        messagebox.showinfo("Listo", f"{nombre} registrado correctamente.")
        self.limpiar()
        self.al_guardar()


# ---------------------------------------------------------------- USUARIOS
class UsuariosTab(ttk.Frame):
    COLUMNAS = (
        ("rol", "Rol", 90), ("nombre", "Nombre", 170), ("carnet", "Carnet / Código", 120),
        ("extra", "Carrera / Cubículo", 150), ("primero", "Primer ingreso", 140),
        ("ultimo", "Último ingreso", 140), ("total", "Ingresos", 70),
    )

    def __init__(self, master, sistema):
        super().__init__(master, padding=10)
        self.sistema = sistema

        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(0, 8))
        ttk.Button(barra, text="Actualizar", command=self.refrescar).pack(side="right")

        marco = ttk.Frame(self)
        marco.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(marco, columns=[c[0] for c in self.COLUMNAS], show="headings")
        for clave, titulo, ancho in self.COLUMNAS:
            self.tree.heading(clave, text=titulo)
            self.tree.column(clave, width=ancho, anchor="center" if clave == "total" else "w")
        scroll = ttk.Scrollbar(marco, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.refrescar()

    def refrescar(self):
        self.tree.delete(*self.tree.get_children())
        for fila in self.sistema.listar_usuarios():
            self.tree.insert("", "end", values=fila)


# ---------------------------------------------------------------- SESIÓN
class SesionFrame(ttk.Frame):
    def __init__(self, app, usuario):
        super().__init__(app, padding=10)
        es_encargado = isinstance(usuario, Encargado)

        cabecera = ttk.Frame(self)
        cabecera.pack(fill="x", pady=(0, 8))
        ttk.Label(cabecera, text=f"{usuario.rol}: {usuario.nombre}  ({usuario.extra})",
                  font=("Segoe UI", 12, "bold")).pack(side="left")
        ttk.Button(cabecera, text="Cerrar sesión", command=app.mostrar_login).pack(side="right")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        tab_inventario = InventarioTab(self.notebook, app.sistema, puede_eliminar=es_encargado)
        self.notebook.add(tab_inventario, text="Inventario")

        if es_encargado:
            self.notebook.add(AgregarTab(self.notebook, app.sistema, tab_inventario.refrescar),
                              text="Agregar componente")
            self.notebook.add(UsuariosTab(self.notebook, app.sistema),
                              text="Usuarios registrados")

        self.notebook.bind("<<NotebookTabChanged>>", self._al_cambiar_pestana)

    def _al_cambiar_pestana(self, _evento):
        pestana = self.notebook.nametowidget(self.notebook.select())
        if hasattr(pestana, "refrescar"):
            pestana.refrescar()


# ---------------------------------------------------------------- APLICACIÓN
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión - Lab de Electrónica")
        self.geometry("1000x620")
        self.minsize(860, 480)
        self.sistema = SistemaInventario()
        self.frame_actual = None
        self.mostrar_login()

    def _cambiar_a(self, frame):
        if self.frame_actual is not None:
            self.frame_actual.destroy()
        self.frame_actual = frame
        self.frame_actual.pack(fill="both", expand=True)

    def mostrar_login(self):
        self._cambiar_a(LoginFrame(self))

    def mostrar_sesion(self, usuario, es_nuevo):
        self._cambiar_a(SesionFrame(self, usuario))
        saludo = (f"Usuario {usuario.nombre} registrado por primera vez."
                  if es_nuevo else f"Bienvenido de nuevo, {usuario.nombre}.")
        messagebox.showinfo("Sesión iniciada", saludo)


def iniciar():
    App().mainloop()


if __name__ == "__main__":
    iniciar()