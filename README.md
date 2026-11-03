Explicación del sistema de inventario con interfaz gráfica
2 nov 2026 · @shima
1. Objetivo y resumen
El sistema gestiona el inventario de un laboratorio de electrónica: guarda componentes, usuarios y préstamos en SQLite3, y ahora se maneja desde una ventana hecha con Tkinter.
El proyecto se construyó por etapas:
• Persistencia en SQLite: los datos viven en db/inventario.db, con las tablas componentes, usuarios y prestamos.
• Registro de usuarios: cada ingreso queda guardado, con fecha del primer ingreso, del último y número total de ingresos.
• Préstamos: el estudiante puede pedir un equipo; si ya tiene uno sin devolver y pide otro, no se le presta nada.
• Interfaz gráfica: una ventana con pestañas distintas para el estudiante y el encargado. La versión de consola se conserva en main_consola.py.
2. Estructura del proyecto
El código está dividido en archivos con una sola responsabilidad cada uno. La ventana nunca escribe SQL: pide todo a SistemaInventario, que es el único que habla con la base de datos.
Archivo
Qué contiene
Papel en el sistema
main.py
Crea la ventana App y llama a mainloop()
Punto de entrada con interfaz gráfica
main_consola.py
El menú de texto original
Punto de entrada alterno (opcional)
interfaz.py
Clase App (ventana Tkinter) y funciones auxiliares
Capa de presentación
sistema.py
Clase SistemaInventario
Todo el acceso a SQLite: tablas, usuarios, componentes y préstamos
usuarios.py
Usuario, Estudiante, Encargado
Datos del usuario y menús de consola
componentes.py
ComponenteElectronico y 9 subclases
Datos de cada tipo de equipo
utilidades.py
pedir_entero
Validación de números en consola
config.py
ARCHIVO_DB
Ruta de la base de datos; crea la carpeta db si no existe
Las capas se leen de arriba hacia abajo: interfaz, sistema, SQLite.
3. Qué se hizo para la interfaz gráfica
La interfaz es una sola clase, App, que hereda de tkinter.Tk y muestra dos pantallas: el login y la ventana principal.
Login (mostrar_login y _ingresar). El usuario elige su rol y escribe nombre, carnet o código, y carrera o cubículo. La ventana valida que no haya campos vacíos, crea un Estudiante o un Encargado, llama a registrar_usuario y abre la pantalla principal.
Pantalla principal (mostrar_principal). Una cabecera con el nombre, el rol y si es su primer ingreso, y un Notebook con pestañas según el rol:
Pestaña
Quién la ve
Qué permite
Inventario
Estudiante y encargado
Tabla con buscador. El estudiante pide y devuelve equipos y ve su estado; el encargado edita y elimina
Registrar componente
Encargado
Formulario cuyos campos cambian según el tipo de componente
Usuarios registrados
Encargado
Tabla con rol, fechas de ingreso y total de ingresos
Préstamos
Encargado
Tabla de préstamos con los pendientes resaltados y un contador
Decisiones técnicas:
1. App no contiene SQL. Todo pasa por SistemaInventario, así la lógica es la misma en consola y en ventana.
2. La función ejecutar() captura el mensaje que los métodos antes solo imprimían y lo muestra en un cuadro de diálogo. Así no hubo que reescribir las reglas de préstamo.
3. El diccionario TIPOS guarda, para cada componente, su clase, su nombre visible y sus dos campos propios. Con él un solo formulario sirve para los 9 tipos.
4. refrescar_todo() vuelve a leer la base después de cada acción y conserva la fila seleccionada.
5. Cada fila usa el ID del componente como identificador interno, para que un ID como 007 no pierda sus ceros.
6. Antes de prestar, eliminar o reemplazar un ID existente, la ventana pide confirmación.
4. Cambios en sistema.py para la ventana
Los métodos de consola solo imprimían texto, y la ventana necesita datos. Por eso se agregaron dos tipos de cambios, sin tocar la lógica existente:
• Consultas que devuelven datos: obtener_inventario(), obtener_usuarios(), obtener_prestamos() y obtener_prestamo_activo(carnet). Las tablas de la ventana se llenan con ellas.
• Retornos útiles: agregar_item, eliminar_item, prestar_item y devolver_item devuelven True o False. registrar_usuario devuelve True si el usuario es nuevo, False si ya existía y None si hubo un error de SQLite.
Los métodos mostrar_* de la consola siguen igual, así que main_consola.py y main.py comparten la misma base de datos y las mismas reglas.
5. Relación con el diagrama de casos de uso
Cada óvalo del diagrama 01_casos_de_uso corresponde a algo que el usuario ve o hace en la ventana, y a un método concreto del código. Los casos que son una verificación interna no tienen botón: ocurren dentro de otro método.
 
Caso de uso
Actor
En la ventana
En el código
Ingresar al sistema
Usuario
Pantalla de login, botón Ingresar
App._ingresar()
Registrar o actualizar usuario
(interno)
Automático al ingresar
SistemaInventario.registrar_usuario()
Ver inventario
Usuario
Pestaña Inventario
refrescar_inventario() que usa obtener_inventario()
Buscar equipo en el inventario
Usuario
Cuadro Buscar
var_buscar llama a refrescar_inventario() en cada tecla
Cerrar sesión
Usuario
Botón Cerrar sesión
App.mostrar_login()
Pedir equipo prestado
Estudiante
Botón Pedir prestado el equipo seleccionado
App.pedir_prestado() que llama a prestar_item()
Verificar que no tenga un equipo sin devolver
(interno)
Dentro del préstamo
_prestamo_activo()
Verificar disponibilidad del equipo
(interno)
Dentro del préstamo
Revisa que cantidad sea mayor que 0
Rechazar préstamo
(interno)
Mensaje No se prestó nada
prestar_item() devuelve False
Devolver equipo
Estudiante
Botón Devolver equipo
App.devolver_equipo() que llama a devolver_item()
Ver mi préstamo actual
Estudiante
Texto naranja bajo la tabla
refrescar_estado_prestamo() que usa obtener_prestamo_activo()
Registrar componente
Encargado
Pestaña Registrar componente
guardar_componente() que llama a agregar_item()
Editar componente
Encargado
Editar seleccionado o doble clic
cargar_en_formulario() y luego guardar_componente()
Eliminar componente
Encargado
Botón Eliminar seleccionado
eliminar_seleccionado() que llama a eliminar_item()
Verificar que no haya unidades prestadas
(interno)
Dentro de la eliminación
Consulta de préstamos pendientes en eliminar_item()
Ver usuarios registrados
Encargado
Pestaña Usuarios registrados
refrescar_usuarios() que usa obtener_usuarios()
Ver préstamos de equipos
Encargado
Pestaña Préstamos
refrescar_prestamos() que usa obtener_prestamos()
Cómo se leen las relaciones del diagrama en el código:
• Generalización de actores. Estudiante y Encargado son tipos de Usuario, igual que en el código, donde las dos clases heredan de Usuario. La ventana decide qué pestañas mostrar con isinstance(self.usuario, Encargado).
• include (siempre ocurre). Ingresar incluye registrar al usuario. Pedir un equipo incluye las dos verificaciones. Eliminar incluye revisar que no haya unidades prestadas. Editar incluye registrar, porque reutiliza el mismo formulario y guarda con INSERT OR REPLACE.
• extend (solo a veces). Rechazar el préstamo ocurre únicamente si el estudiante ya tiene un equipo pendiente, el ID no existe o no hay unidades. Buscar amplía Ver inventario, pero el inventario se ve igual sin buscar.
6. Relación con el diagrama de clases
El diagrama 06_clases agrupa las clases por archivo. La interfaz gráfica agregó la clase App y un grupo de funciones auxiliares; el resto de las clases ya existían.
 
Clase
Archivo
Responsabilidad
Relaciones en el diagrama
ComponenteElectronico y 9 subclases
componentes.py
Guardan los datos de cada equipo y se describen con obtener_detalles()
Herencia: cada tipo (Resistencia, Sensor, etc.) hereda de ComponenteElectronico
Usuario, Estudiante, Encargado
usuarios.py
Datos del usuario y menús de consola
Estudiante y Encargado heredan de Usuario
SistemaInventario
sistema.py
Todo el acceso a SQLite
Crea instancias de componentes, usa config.py y lee y escribe las 3 tablas
App
interfaz.py
La ventana
Hereda de tkinter.Tk; compone un SistemaInventario; agrega un Usuario (la sesión actual); crea Estudiante o Encargado al ingresar y componentes al guardar
Funciones de interfaz
interfaz.py
TIPOS, nombre_visible, describir, ejecutar
App las usa
main.py y main_consola.py
Entradas
Arrancan el programa
main.py crea App; main_consola.py crea SistemaInventario y los usuarios
Qué significa cada tipo de flecha:
• Herencia (flecha con triángulo vacío). Una clase hereda atributos y métodos de otra: los 9 componentes de ComponenteElectronico, y Estudiante y Encargado de Usuario.
• Composición (rombo relleno), App a SistemaInventario. La ventana crea su propio sistema al iniciar y lo guarda en self.sistema. Si la ventana se cierra, el sistema desaparece con ella.
• Agregación (rombo vacío), App a Usuario. La ventana apunta al usuario de la sesión actual (self.usuario, de 0 a 1). Ese objeto se crea en el login y se reemplaza al cerrar sesión.
• Dependencia (flecha punteada). Una clase usa a otra sin guardarla: App crea Estudiante y Encargado solo al ingresar, y crea un componente solo al guardar.
Las tablas de la base de datos aparecen al final del diagrama:
• componentes: un equipo por fila, con attr1 y attr2 para sus dos características propias.
• usuarios: un usuario por rol y carnet, con fechas y contador de ingresos.
• prestamos: un préstamo por fila; fecha_devolucion vacía significa pendiente.
prestamos se relaciona con componentes por id_item y con usuarios por carnet. Es una relación lógica: la base no declara claves foráneas, así que la coherencia la cuida SistemaInventario.
7. Relación con los diagramas de secuencia
Los cuatro diagramas de secuencia siguen el mismo camino: el usuario actúa sobre la ventana, App llama a SistemaInventario a través de ejecutar(), este consulta o modifica SQLite, y App muestra el resultado y refresca las tablas con refrescar_todo().
Diagrama
Evento en la ventana
Métodos que intervienen
02_secuencia_ingreso
Botón Ingresar
_ingresar(), registrar_usuario(), mostrar_principal()
03_secuencia_prestamo
Botón Pedir prestado
pedir_prestado(), prestar_item(), _prestamo_activo()
04_secuencia_devolucion
Botón Devolver equipo
devolver_equipo(), devolver_item()
05_secuencia_registro_componente
Botón Guardar componente
guardar_componente(), agregar_item(), get_db_data()
Las ramas alt de cada diagrama son los if del código. En el préstamo, por ejemplo, la primera rama es la regla que impide pedir un segundo equipo.
8. Reglas del préstamo y dónde se aplican
La regla central es que un estudiante con un equipo sin devolver no recibe otro. Se aplica en SistemaInventario, no en la ventana, por lo que vale igual en consola y en interfaz gráfica.
Regla
Dónde se aplica
Qué pasa
Un solo equipo a la vez
prestar_item() consulta _prestamo_activo()
Si ya tiene uno, no se presta nada, el inventario no cambia y se muestra "Devuelva ese equipo antes de pedir otro"
No se presta sin unidades
prestar_item() revisa cantidad
Si no hay unidades, se avisa y no se crea el préstamo
Prestar descuenta una unidad
prestar_item()
cantidad baja en 1 y se crea una fila en prestamos
Devolver suma una unidad
devolver_item()
Se llena fecha_devolucion y cantidad sube en 1
El préstamo sigue aunque cierre sesión
Se busca por carnet
Al volver a entrar con el mismo carnet, sigue bloqueado hasta devolver
No se elimina un equipo prestado
eliminar_item()
Se avisa y no se borra mientras haya unidades sin devolver
La columna Disponibles de la tabla muestra cantidad, es decir, lo que queda en el laboratorio sin contar lo prestado.
9. Cómo ejecutarlo, limitaciones y mejoras
Para ejecutarlo: deja todos los archivos .py en la misma carpeta y corre python main.py. La carpeta db y el archivo inventario.db se crean solos la primera vez. Tkinter viene incluido con Python en Windows, así que no hay que instalar nada. Para usar la versión de consola, corre python main_consola.py.
Limitaciones actuales:
• No hay contraseña. El sistema identifica al estudiante por su carnet, así que alguien podría escribir el carnet de otro para saltarse el bloqueo del préstamo.
• Cada estudiante puede tener un solo equipo a la vez.
• Al editar un componente, la cantidad que se escribe reemplaza a la guardada, incluso si hay unidades prestadas.
• La base no declara claves foráneas entre prestamos, componentes y usuarios.
Mejoras posibles: inicio de sesión con contraseña, un límite de días por préstamo con aviso de atraso, un historial por estudiante y claves foráneas en la base de datos.
