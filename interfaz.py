import contextlib
import io
import tkinter as tk
from tkinter import ttk, messagebox

from sistema import SistemaInventario
from usuarios import Estudiante, Encargado
from componentes import (
    Resistencia, Condensador, Bobina, Diodo, Transistor,
    CircuitoIntegrado, Microcontrolador, Sensor, InstrumentoLab,
)

# Clave (la misma que guarda la base de datos) ->
#   (clase, nombre visible, (campo 1, ejemplo), (campo 2, ejemplo))
TIPOS = {
    "Resistencia":       (Resistencia, "Resistencia", ("Valor", "220Ω, 10kΩ"), ("Tolerancia %", "5")),
    "Condensador":       (Condensador, "Condensador", ("Capacitancia", "100uF, 22pF"), ("Voltaje máx (V)", "50")),
    "Bobina":            (Bobina, "Bobina", ("Inductancia", "10mH"), ("Corriente máx (A)", "1")),
    "Diodo":             (Diodo, "Diodo", ("Tipo", "LED, Zener, Rectificador"), ("Corriente máx (A)", "1")),
    "Transistor":        (Transistor, "Transistor", ("Tipo", "BJT o MOSFET"), ("Encapsulado", "TO-92, TO-220")),
    "CircuitoIntegrado": (CircuitoIntegrado, "Circuito integrado (IC)", ("Número de pines", "8, 14, 40"), ("Función", "Compuerta AND")),
    "Microcontrolador":  (Microcontrolador, "Microcontrolador", ("Voltaje (V)", "3.3 / 5"), ("Reloj", "16MHz")),
    "Sensor":            (Sensor, "Sensor", ("Magnitud que mide", "Temperatura"), ("Interfaz", "I2C, Analógico")),
    "InstrumentoLab":    (InstrumentoLab, "Instrumento de laboratorio", ("Marca", "Fluke, Rigol"), ("Precisión / rango", "±0.5%")),
}
NOMBRE_A_CLAVE = {datos[1]: clave for clave, datos in TIPOS.items()}

COLOR_CABECERA = "#1f3a5f"
COLOR_FILA_PAR = "#eef3f9"
COLOR_PENDIENTE = "#b45309"


def nombre_visible(clave):
    return TIPOS[clave][1] if clave in TIPOS else clave


def describir(clave, attr1, attr2):
    """Texto con las características propias de cada tipo de componente."""
    if clave not in TIPOS:
        return ""
    (etq1, _), (etq2, _) = TIPOS[clave][2], TIPOS[clave][3]
    return f"{etq1}: {attr1 or '-'}   |   {etq2}: {attr2 or '-'}"


def ejecutar(funcion, *args):
    """Ejecuta un método de SistemaInventario y devuelve (resultado, mensaje que habría impreso)."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        resultado = funcion(*args)
    return resultado, buffer.getvalue().strip()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión - Laboratorio de Electrónica")
        self.geometry("1040x680")
        self.minsize(900, 580)

        self.sistema = SistemaInventario()
        self.usuario = None

        self._configurar_estilos()
        self.contenedor = ttk.Frame(self)
        self.contenedor.pack(fill="both", expand=True)
        self.mostrar_login()

    # ------------------------------------------------------------------
    # Estilos y utilidades
    # ------------------------------------------------------------------
    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 20, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 10), foreground="#555555")
        estilo.configure("Cab.TFrame", background=COLOR_CABECERA)
        estilo.configure("CabTitulo.TLabel", background=COLOR_CABECERA,
                         foreground="white", font=("Segoe UI", 13, "bold"))
        estilo.configure("CabTexto.TLabel", background=COLOR_CABECERA,
                         foreground="#c9d6e8", font=("Segoe UI", 10))
        estilo.configure("Estado.TLabel", font=("Segoe UI", 10, "bold"))
        estilo.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        estilo.configure("TButton", padding=6)
        estilo.configure("Accion.TButton", font=("Segoe UI", 10, "bold"))

    def _limpiar(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def _crear_tabla(self, padre, columnas):
        """columnas: lista de (clave, encabezado, ancho). Devuelve el Treeview."""
        marco = ttk.Frame(padre)
        marco.pack(fill="both", expand=True)
        tabla = ttk.Treeview(marco, columns=[c[0] for c in columnas],
                             show="headings", selectmode="browse")
        for clave, encabezado, ancho in columnas:
            tabla.heading(clave, text=encabezado)
            tabla.column(clave, width=ancho, anchor="w")
        barra = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)
        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        tabla.tag_configure("par", background=COLOR_FILA_PAR)
        tabla.tag_configure("pendiente", foreground=COLOR_PENDIENTE)
        return tabla

    @staticmethod
    def _llenar_tabla(tabla, filas, ids=None, etiquetas=None):
        """ids: identificador de cada fila (así los ceros a la izquierda no se pierden)."""
        seleccionadas = tabla.selection() if ids else ()
        tabla.delete(*tabla.get_children())
        for i, valores in enumerate(filas):
            tags = ["par"] if i % 2 == 0 else []
            if etiquetas and etiquetas[i]:
                tags.append(etiquetas[i])
            opciones = {"iid": str(ids[i])} if ids else {}
            tabla.insert("", "end", values=valores, tags=tuple(tags), **opciones)
        # conserva la fila seleccionada si sigue existiendo
        for iid in seleccionadas:
            if tabla.exists(iid):
                tabla.selection_set(iid)

    # ------------------------------------------------------------------
    # Pantalla de inicio de sesión
    # ------------------------------------------------------------------
    def mostrar_login(self):
        self._limpiar()
        self.usuario = None

        marco = ttk.Frame(self.contenedor, padding=30)
        marco.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(marco, text="Laboratorio de Electrónica",
                  style="Titulo.TLabel").grid(row=0, column=0, columnspan=2)
        ttk.Label(marco, text="Ingrese sus datos para continuar",
                  style="Subtitulo.TLabel").grid(row=1, column=0, columnspan=2, pady=(2, 20))

        self.var_rol = tk.StringVar(value="Estudiante")
        self.var_nombre = tk.StringVar()
        self.var_carnet = tk.StringVar()
        self.var_extra = tk.StringVar()

        ttk.Label(marco, text="Ingresar como:").grid(row=2, column=0, sticky="w", pady=6)
        combo_rol = ttk.Combobox(marco, textvariable=self.var_rol, state="readonly",
                                 values=["Estudiante", "Encargado"], width=28)
        combo_rol.grid(row=2, column=1, pady=6, padx=(12, 0))
        combo_rol.bind("<<ComboboxSelected>>", lambda e: self._actualizar_etiquetas_login())

        ttk.Label(marco, text="Nombre:").grid(row=3, column=0, sticky="w", pady=6)
        entrada_nombre = ttk.Entry(marco, textvariable=self.var_nombre, width=31)
        entrada_nombre.grid(row=3, column=1, pady=6, padx=(12, 0))

        self.lbl_carnet = ttk.Label(marco)
        self.lbl_carnet.grid(row=4, column=0, sticky="w", pady=6)
        ttk.Entry(marco, textvariable=self.var_carnet, width=31).grid(row=4, column=1, pady=6, padx=(12, 0))

        self.lbl_extra = ttk.Label(marco)
        self.lbl_extra.grid(row=5, column=0, sticky="w", pady=6)
        ttk.Entry(marco, textvariable=self.var_extra, width=31).grid(row=5, column=1, pady=6, padx=(12, 0))

        ttk.Button(marco, text="Ingresar", style="Accion.TButton",
                   command=self._ingresar).grid(row=6, column=0, columnspan=2, pady=(20, 0), sticky="ew")

        self._actualizar_etiquetas_login()
        entrada_nombre.focus_set()
        self.bind("<Return>", lambda e: self._ingresar())

    def _actualizar_etiquetas_login(self):
        if self.var_rol.get() == "Estudiante":
            self.lbl_carnet.config(text="Carnet:")
            self.lbl_extra.config(text="Carrera:")
        else:
            self.lbl_carnet.config(text="Código de empleado:")
            self.lbl_extra.config(text="Cubículo:")

    def _ingresar(self):
        if self.usuario is not None:          # ya hay una sesión abierta
            return
        nombre = self.var_nombre.get().strip()
        carnet = self.var_carnet.get().strip()
        extra = self.var_extra.get().strip()

        if not (nombre and carnet and extra):
            messagebox.showwarning("Datos incompletos", "Complete todos los campos para ingresar.")
            return

        clase = Estudiante if self.var_rol.get() == "Estudiante" else Encargado
        usuario = clase(nombre, carnet, extra)
        nuevo, _ = ejecutar(self.sistema.registrar_usuario, usuario)
        if nuevo is None:
            messagebox.showerror("Error", "No se pudo registrar al usuario en la base de datos.")
            return

        self.usuario = usuario
        self.unbind("<Return>")
        self.mostrar_principal(nuevo)

    # ------------------------------------------------------------------
    # Pantalla principal
    # ------------------------------------------------------------------
    def mostrar_principal(self, es_nuevo):
        self._limpiar()
        es_encargado = isinstance(self.usuario, Encargado)

        cabecera = ttk.Frame(self.contenedor, style="Cab.TFrame", padding=(16, 10))
        cabecera.pack(fill="x")
        textos = ttk.Frame(cabecera, style="Cab.TFrame")
        textos.pack(side="left")
        ttk.Label(textos, text=self.usuario.nombre, style="CabTitulo.TLabel").pack(anchor="w")
        saludo = "Primer ingreso registrado" if es_nuevo else "Bienvenido de nuevo"
        ttk.Label(textos, text=f"{self.usuario.rol} · {self.usuario.extra} · {saludo}",
                  style="CabTexto.TLabel").pack(anchor="w")
        ttk.Button(cabecera, text="Cerrar sesión", command=self.mostrar_login).pack(side="right")

        self.notebook = ttk.Notebook(self.contenedor)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self._crear_tab_inventario(es_encargado)
        if es_encargado:
            self._crear_tab_formulario()
            self._crear_tab_usuarios()
            self._crear_tab_prestamos()

        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.refrescar_todo())
        self.refrescar_todo()

    # ---------------- Pestaña: inventario ----------------
    def _crear_tab_inventario(self, es_encargado):
        tab = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(tab, text="Inventario")

        barra = ttk.Frame(tab)
        barra.pack(fill="x", pady=(0, 8))
        ttk.Label(barra, text="Buscar:").pack(side="left")
        self.var_buscar = tk.StringVar()
        self.var_buscar.trace_add("write", lambda *args: self.refrescar_inventario())
        ttk.Entry(barra, textvariable=self.var_buscar, width=32).pack(side="left", padx=8)
        self.lbl_total = ttk.Label(barra, style="Subtitulo.TLabel")
        self.lbl_total.pack(side="right")

        self.tabla_inv = self._crear_tabla(tab, [
            ("id", "ID", 80),
            ("tipo", "Tipo", 190),
            ("nombre", "Nombre", 180),
            ("cantidad", "Disponibles", 85),
            ("ubicacion", "Ubicación", 110),
            ("detalle", "Características", 330),
        ])

        pie = ttk.Frame(tab)
        pie.pack(fill="x", pady=(8, 0))
        if es_encargado:
            ttk.Button(pie, text="Editar seleccionado",
                       command=self.cargar_en_formulario).pack(side="left")
            ttk.Button(pie, text="Eliminar seleccionado",
                       command=self.eliminar_seleccionado).pack(side="left", padx=8)
            self.tabla_inv.bind("<Double-1>", lambda e: self.cargar_en_formulario())
        else:
            ttk.Button(pie, text="Pedir prestado el equipo seleccionado", style="Accion.TButton",
                       command=self.pedir_prestado).pack(side="left")
            self.btn_devolver = ttk.Button(pie, text="Devolver equipo", command=self.devolver_equipo)
            self.btn_devolver.pack(side="right")
            self.lbl_prestamo = ttk.Label(pie, style="Estado.TLabel")
            self.lbl_prestamo.pack(side="right", padx=12)

    def refrescar_inventario(self):
        if not hasattr(self, "tabla_inv") or not self.tabla_inv.winfo_exists():
            return
        filtro = self.var_buscar.get().strip().lower()
        filas, ids = [], []
        for id_item, tipo, nombre, cantidad, ubicacion, a1, a2 in self.sistema.obtener_inventario():
            fila = (id_item, nombre_visible(tipo), nombre, cantidad, ubicacion, describir(tipo, a1, a2))
            if not filtro or filtro in " ".join(str(v) for v in fila).lower():
                filas.append(fila)
                ids.append(id_item)
        self._llenar_tabla(self.tabla_inv, filas, ids)
        self.lbl_total.config(text=f"{len(filas)} componente(s)")

    def _seleccion(self):
        """Devuelve (id, nombre) de la fila seleccionada o None."""
        seleccion = self.tabla_inv.selection()
        if not seleccion:
            messagebox.showinfo("Seleccione un componente", "Primero seleccione una fila de la tabla.")
            return None
        return seleccion[0], str(self.tabla_inv.item(seleccion[0], "values")[2])

    # ---- acciones del estudiante ----
    def pedir_prestado(self):
        seleccion = self._seleccion()
        if seleccion is None:
            return
        id_item, nombre = seleccion
        if not messagebox.askyesno("Confirmar préstamo",
                                   f"¿Pedir prestado '{nombre}' (ID {id_item})?"):
            return
        ok, mensaje = ejecutar(self.sistema.prestar_item, self.usuario, id_item)
        if ok:
            messagebox.showinfo("Préstamo realizado", mensaje)
        else:
            messagebox.showwarning("No se prestó nada", mensaje)
        self.refrescar_todo()

    def devolver_equipo(self):
        ok, mensaje = ejecutar(self.sistema.devolver_item, self.usuario)
        if ok:
            messagebox.showinfo("Devolución registrada", mensaje)
        else:
            messagebox.showinfo("Sin equipos pendientes", mensaje)
        self.refrescar_todo()

    def refrescar_estado_prestamo(self):
        if not hasattr(self, "lbl_prestamo") or not self.lbl_prestamo.winfo_exists():
            return
        activo = self.sistema.obtener_prestamo_activo(self.usuario.carnet)
        if activo:
            id_item, nombre, desde = activo
            self.lbl_prestamo.config(
                text=f"Tiene prestado: {nombre} (ID {id_item}) desde {desde}",
                foreground=COLOR_PENDIENTE)
            self.btn_devolver.state(["!disabled"])
        else:
            self.lbl_prestamo.config(text="No tiene equipos prestados", foreground="#2f6b2f")
            self.btn_devolver.state(["disabled"])

    # ---- acciones del encargado ----
    def eliminar_seleccionado(self):
        seleccion = self._seleccion()
        if seleccion is None:
            return
        id_item, _ = seleccion
        if not messagebox.askyesno("Confirmar eliminación",
                                   f"¿Eliminar el componente con ID '{id_item}'?"):
            return
        ok, mensaje = ejecutar(self.sistema.eliminar_item, id_item)
        if not ok:
            messagebox.showwarning("No se eliminó", mensaje)
        self.refrescar_todo()

    # ---------------- Pestaña: registrar / editar ----------------
    def _crear_tab_formulario(self):
        self.tab_form = ttk.Frame(self.notebook, padding=24)
        self.notebook.add(self.tab_form, text="Registrar componente")
        self.tab_form.columnconfigure(1, weight=1)

        self.var_tipo = tk.StringVar(value=TIPOS["Resistencia"][1])
        self.campos = {k: tk.StringVar() for k in ("id", "nombre", "cantidad", "ubicacion", "attr1", "attr2")}

        ttk.Label(self.tab_form, text="Tipo de componente:").grid(row=0, column=0, sticky="w", pady=8)
        combo = ttk.Combobox(self.tab_form, textvariable=self.var_tipo, state="readonly",
                             values=[datos[1] for datos in TIPOS.values()], width=34)
        combo.grid(row=0, column=1, sticky="w", pady=8, padx=(16, 0))
        combo.bind("<<ComboboxSelected>>", lambda e: self._actualizar_etiquetas_form())

        filas = [("ID:", "id"), ("Nombre:", "nombre"), ("Cantidad:", "cantidad"), ("Ubicación:", "ubicacion")]
        for i, (texto, clave) in enumerate(filas, start=1):
            ttk.Label(self.tab_form, text=texto).grid(row=i, column=0, sticky="w", pady=8)
            ttk.Entry(self.tab_form, textvariable=self.campos[clave], width=40).grid(
                row=i, column=1, sticky="w", pady=8, padx=(16, 0))

        self.lbl_attr1 = ttk.Label(self.tab_form)
        self.lbl_attr1.grid(row=5, column=0, sticky="w", pady=8)
        ttk.Entry(self.tab_form, textvariable=self.campos["attr1"], width=40).grid(
            row=5, column=1, sticky="w", pady=8, padx=(16, 0))

        self.lbl_attr2 = ttk.Label(self.tab_form)
        self.lbl_attr2.grid(row=6, column=0, sticky="w", pady=8)
        ttk.Entry(self.tab_form, textvariable=self.campos["attr2"], width=40).grid(
            row=6, column=1, sticky="w", pady=8, padx=(16, 0))

        botones = ttk.Frame(self.tab_form)
        botones.grid(row=7, column=0, columnspan=2, sticky="w", pady=(20, 0))
        ttk.Button(botones, text="Guardar componente", style="Accion.TButton",
                   command=self.guardar_componente).pack(side="left")
        ttk.Button(botones, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=10)

        self._actualizar_etiquetas_form()

    def _clave_tipo(self):
        return NOMBRE_A_CLAVE[self.var_tipo.get()]

    def _actualizar_etiquetas_form(self):
        (etq1, ej1), (etq2, ej2) = TIPOS[self._clave_tipo()][2], TIPOS[self._clave_tipo()][3]
        self.lbl_attr1.config(text=f"{etq1} (ej. {ej1}):")
        self.lbl_attr2.config(text=f"{etq2} (ej. {ej2}):")

    def limpiar_formulario(self):
        for variable in self.campos.values():
            variable.set("")

    def guardar_componente(self):
        id_item = self.campos["id"].get().strip()
        nombre = self.campos["nombre"].get().strip()
        ubicacion = self.campos["ubicacion"].get().strip()
        attr1 = self.campos["attr1"].get().strip()
        attr2 = self.campos["attr2"].get().strip()

        if not (id_item and nombre and ubicacion and attr1 and attr2):
            messagebox.showwarning("Datos incompletos", "Complete todos los campos del formulario.")
            return
        try:
            cantidad = int(self.campos["cantidad"].get().strip())
            if cantidad < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Cantidad no válida", "La cantidad debe ser un número entero (0 o mayor).")
            return

        existentes = {str(fila[0]) for fila in self.sistema.obtener_inventario()}
        if id_item in existentes and not messagebox.askyesno(
                "ID existente", f"Ya existe un componente con el ID '{id_item}'.\n¿Desea reemplazarlo?"):
            return

        clase = TIPOS[self._clave_tipo()][0]
        componente = clase(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        ok, _ = ejecutar(self.sistema.agregar_item, componente)
        if ok:
            messagebox.showinfo("Guardado", f"'{nombre}' se guardó correctamente.")
            self.limpiar_formulario()
            self.refrescar_todo()
        else:
            messagebox.showerror("Error", "No se pudo guardar el componente en la base de datos.")

    def cargar_en_formulario(self):
        seleccion = self._seleccion()
        if seleccion is None:
            return
        id_item, _ = seleccion
        for fila in self.sistema.obtener_inventario():
            if str(fila[0]) == id_item:
                _, tipo, nombre, cantidad, ubicacion, a1, a2 = fila
                break
        else:
            return
        if tipo not in TIPOS:
            messagebox.showinfo("No editable", "Este componente es de tipo general y no se puede editar aquí.")
            return

        self.var_tipo.set(nombre_visible(tipo))
        self._actualizar_etiquetas_form()
        self.campos["id"].set(id_item)
        self.campos["nombre"].set(nombre)
        self.campos["cantidad"].set(str(cantidad))
        self.campos["ubicacion"].set(ubicacion)
        self.campos["attr1"].set(a1 or "")
        self.campos["attr2"].set(a2 or "")
        self.notebook.select(self.tab_form)

    # ---------------- Pestaña: usuarios ----------------
    def _crear_tab_usuarios(self):
        tab = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(tab, text="Usuarios registrados")
        self.tabla_usr = self._crear_tabla(tab, [
            ("rol", "Rol", 90),
            ("nombre", "Nombre", 170),
            ("carnet", "Carnet / Código", 120),
            ("extra", "Carrera / Cubículo", 150),
            ("primero", "Primer ingreso", 150),
            ("ultimo", "Último ingreso", 150),
            ("total", "Ingresos", 70),
        ])

    def refrescar_usuarios(self):
        if hasattr(self, "tabla_usr") and self.tabla_usr.winfo_exists():
            self._llenar_tabla(self.tabla_usr, self.sistema.obtener_usuarios())

    # ---------------- Pestaña: préstamos ----------------
    def _crear_tab_prestamos(self):
        tab = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(tab, text="Préstamos")
        self.lbl_pendientes = ttk.Label(tab, style="Subtitulo.TLabel")
        self.lbl_pendientes.pack(anchor="e", pady=(0, 8))
        self.tabla_prest = self._crear_tabla(tab, [
            ("estudiante", "Estudiante", 150),
            ("carnet", "Carnet", 90),
            ("equipo", "Equipo", 190),
            ("id", "ID equipo", 80),
            ("prestado", "Prestado", 150),
            ("estado", "Estado", 230),
        ])

    def refrescar_prestamos(self):
        if not hasattr(self, "tabla_prest") or not self.tabla_prest.winfo_exists():
            return
        filas, etiquetas = [], []
        for estudiante, carnet, equipo, id_item, desde, hasta in self.sistema.obtener_prestamos():
            estado = f"Devuelto {hasta}" if hasta else "PENDIENTE DE DEVOLVER"
            filas.append((estudiante, carnet, equipo, id_item, desde, estado))
            etiquetas.append(None if hasta else "pendiente")
        self._llenar_tabla(self.tabla_prest, filas, etiquetas=etiquetas)
        pendientes = sum(1 for e in etiquetas if e)
        self.lbl_pendientes.config(text=f"{pendientes} equipo(s) pendiente(s) de devolver")

    # ---------------- Refresco general ----------------
    def refrescar_todo(self):
        self.refrescar_inventario()
        self.refrescar_estado_prestamo()
        self.refrescar_usuarios()
        self.refrescar_prestamos()


def main():
    App().mainloop()


if __name__ == "__main__":
    main()