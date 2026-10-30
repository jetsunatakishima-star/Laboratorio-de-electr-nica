Informe técnico: sistema de gestión del Laboratorio de Electrónica 

# Informe técnico: sistema de gestión del Laboratorio de Electrónica 

## 1. Resumen 

El programa es una aplicación en Python, orientada a objetos y con persistencia en SQLite, que gestiona el inventario de componentes electrónicos de un laboratorio. Tiene dos interfaces que comparten el mismo núcleo: una gráfica con Tkinter ( `main.py` ) y una de consola ( `main consola.py` ). Hay dos roles: el **Estudiante** , que solo consulta el inventario, y el **Encargado** , que además agrega y elimina componentes y revisa los usuarios registrados. Todo se guarda en el archivo `db/inventario.db` , que se crea solo al iniciar. 

## 2. Estructura del proyecto 

|Archivo|Responsabilidad|
|---|---|
|`config.py`|Define la ruta de la base de datos y crea la carpeta<br>`db`si no existe.|
|`componentes.py`|Jerarquía de clases de componentes electrónicos<br>(clase base y 9 subclases).|
|`usuarios.py`|Clases<br>`Usuario`,<br>`Estudiante`y<br>`Encargado`, con<br>los menús de la versión de consola.|
|`sistema.py`|Clase<br>`SistemaInventario`: único punto de acceso<br>a SQLite (usuarios y componentes).|
|`utilidades.py`|Función<br>`pedir_entero`, que valida números<br>enteros en consola.|
|`gui.py`|Interfaz gráfica: ventana, login, pestañas de<br>inventario, alta y usuarios.|
|`main.py`|Punto de entrada de la interfaz gráfica.|
|`main consola.py`|Punto de entrada de la versión de consola.|



Page 1 of 10 

Informe técnico: sistema de gestión del Laboratorio de Electrónica 

## 3. Cómo funciona el programa 

### 3.1 Arranque 

`main.py` llama a `iniciar()` de `gui.py` , que crea la ventana `App` . Al construirse, `App` crea un `SistemaInventario` ; este ejecuta `inicializar_db()` , que crea las tablas `componentes` y `usuarios` si no existen. Después `App` muestra el `LoginFrame` . 

### 3.2 Inicio de sesión 

El usuario elige su rol y llena tres campos: nombre, carnet (o código de empleado) y carrera (o cubículo). `LoginFrame.ingresar()` valida que no haya campos vacíos, crea un `Estudiante` o un `Encargado` y llama a `guardar_usuario()` . Si la pareja (rol, carnet) no existe, se inserta con la fecha de primer ingreso. Si ya existe, se actualiza el nombre, el último ingreso y se suma 1 al contador de ingresos. Luego `App.mostrar_sesion()` abre el `SesionFrame` y saluda según sea la primera vez o un regreso. 

### 3.3 Sesión y pestañas 

`SesionFrame` arma un `Notebook` con pestañas según el rol: 

- **Estudiante:** solo la pestaña _Inventario_ . 

- **Encargado:** _Inventario_ (con botón de eliminar), _Agregar componente_ y _Usuarios registrados_ . 

Cada vez que se cambia de pestaña se llama a `refrescar()` , de modo que los datos siempre están al día. 

### 3.4 Consultar el inventario 

`InventarioTab.refrescar()` pide a `SistemaInventario.listar_componentes()` los objetos del inventario, aplica el filtro por tipo y el texto de búsqueda, y llena el `Treeview` . La búsqueda se actualiza mientras se escribe. 

### 3.5 Agregar un componente (solo Encargado) 

1. Se elige el tipo en la lista desplegable; las etiquetas de los dos últimos campos cambian según el tipo. 

2. Al pulsar _Guardar_ , `AgregarTab.guardar()` valida que los campos estén completos y que la cantidad sea un entero no negativo. 

3. Si el ID ya existe ( `existe_item` ), pregunta si se desea reemplazar. 

4. Se crea la instancia de la subclase correspondiente y se guarda con `guardar_item()` , que usa `INSERT OR REPLACE` . 

Page 2 of 10 

Informe técnico: sistema de gestión del Laboratorio de Electrónica 

#### 5. Se limpia el formulario y se refresca el inventario. 

### 3.6 Eliminar componentes (solo Encargado) 

En la pestaña de inventario se seleccionan una o varias filas y se pulsa _Eliminar seleccionados_ . Tras una confirmación, se llama a `borrar_item(id)` por cada fila. 

### 3.7 Persistencia polimórfica 

Todos los componentes se guardan en una sola tabla. Cada subclase implementa `get_db_data()` , que devuelve una tupla `(tipo, attr1, attr2)` con su nombre de tipo y sus dos atributos propios. Al leer, `_crear_instancia()` busca el tipo en el diccionario `CLASES` y reconstruye el objeto de la subclase correcta. Así se guardan y recuperan 9 tipos distintos sin necesidad de 9 tablas. 

|Tipo|attr1|attr2|
|---|---|---|
|Resistencia|valor_ohmios|tolerancia|
|Condensador|capacitancia|voltaje_max|
|Bobina|inductancia|corriente_max|
|Diodo|tipo_diodo|corriente_max|
|Transistor|tipo_transistor|encapsulado|
|CircuitoIntegrado|numero_pines|funcion|
|Microcontrolador|voltaje_operacion|velocidad_reloj|
|Sensor|magnitud_medida|interfaz|
|InstrumentoLab|marca|precision_o_rango|



## 4. Base de datos 

SQLite, archivo `db/inventario.db` . Cada operación abre una conexión con el gestor de contexto `_conexion()` , que confirma los cambios y siempre cierra la conexión al terminar. 

**Tabla** **`componentes` :** `id` (clave primaria, texto), `tipo` , `nombre` , `cantidad` (entero), `ubicacion` , `attr1` , `attr2` . 

**Tabla** **`usuarios` :** `id` (autoincremental), `rol` , `nombre` , `carnet` , `extra` (carrera o cubículo), `primer_ingreso` , `ultimo_ingreso` , `total_ingresos` . Tiene restricción `UNIQUE (rol, carnet)` . 

Page 3 of 10 

Informe técnico: sistema de gestión del Laboratorio de Electrónica 

## 5. Diagrama de casos de uso 

Muestra qué puede hacer cada rol. El Encargado hace todo lo del Estudiante y además administra el inventario y consulta los usuarios. 

```
flowchart LR
  EST([Estudiante])
  ENC([Encargado])
  subgraph SIS[Sistema de gestión del laboratorio]
    UC1([Iniciar sesión])
    UC2([Ver inventario])
    UC3([Buscar y filtrar])
    UC4([Agregar componente])
    UC5([Eliminar componentes])
    UC6([Ver usuarios registrados])
  end
  EST --- UC1
  EST --- UC2
  EST --- UC3
  ENC --- UC1
  ENC --- UC2
  ENC --- UC3
  ENC --- UC4
  ENC --- UC5
  ENC --- UC6
  UC3 -. extend .-> UC2
```

## 6. Diagrama de clases del modelo 

La clase base `ComponenteElectronico` define los datos comunes y dos métodos que las subclases sobrescriben: `obtener_detalles()` (texto legible) y `get_db_data()` (datos para la base). `Usuario` es la base de `Estudiante` y `Encargado` . `SistemaInventario` crea y guarda los objetos del modelo. 

```
classDiagram
  direction TB
  class ComponenteElectronico {
    +id
    +nombre
    +cantidad int
    +ubicacion
    +obtener_detalles() str
    +get_db_data() tuple
  }
  class Resistencia {
```

Page 4 of 10 

Informe técnico: sistema de gestión del Laboratorio de Electrónica 

```
    +valor_ohmios
    +tolerancia
  }
  class Condensador {
    +capacitancia
    +voltaje_max
  }
  class Bobina {
    +inductancia
    +corriente_max
  }
  class Diodo {
    +tipo_diodo
    +corriente_max
  }
  class Transistor {
    +tipo_transistor
    +encapsulado
  }
  class CircuitoIntegrado {
    +numero_pines
    +funcion
  }
  class Microcontrolador {
    +voltaje_operacion
    +velocidad_reloj
  }
  class Sensor {
    +magnitud_medida
    +interfaz
  }
  class InstrumentoLab {
    +marca
    +precision_o_rango
  }
  class Usuario {
    +rol
    +nombre
    +carnet
    +extra() str
    +mostrar_menu_rol(sistema)
  }
  class Estudiante {
    +carrera
  }
  class Encargado {
```

Page 5 of 10 

Informe técnico: sistema de gestión del Laboratorio de Electrónica 

```
    +cubiculo
  }
  class SistemaInventario {
    +inicializar_db()
    +guardar_usuario(usuario) bool
    +listar_usuarios() list
    +existe_item(id) bool
    +guardar_item(item)
    +borrar_item(id) bool
    +listar_componentes() list
    -_crear_instancia(fila)
    -_conexion()
  }
  ComponenteElectronico <|-- Resistencia
  ComponenteElectronico <|-- Condensador
  ComponenteElectronico <|-- Bobina
  ComponenteElectronico <|-- Diodo
  ComponenteElectronico <|-- Transistor
  ComponenteElectronico <|-- CircuitoIntegrado
  ComponenteElectronico <|-- Microcontrolador
  ComponenteElectronico <|-- Sensor
  ComponenteElectronico <|-- InstrumentoLab
  Usuario <|-- Estudiante
  Usuario <|-- Encargado
  SistemaInventario ..> ComponenteElectronico : persiste y crea
  SistemaInventario ..> Usuario : registra
  Estudiante ..> SistemaInventario : consulta
  Encargado ..> SistemaInventario : administra
```

## 7. Diagrama de clases de la interfaz gráfica 

`App` es la ventana principal y contiene al `SistemaInventario` . Alterna entre `LoginFrame` y `SesionFrame` ; este último compone las pestañas según el rol. Todas las pestañas leen y escriben a través de `SistemaInventario` . `AgregarTab` recibe como callback el método `refrescar` de `InventarioTab` para actualizarlo tras guardar. 

```
classDiagram
  direction TB
  class Tk {
    <<tkinter>>
  }
  class Frame {
    <<ttk.Frame>>
  }
  class App {
```

Page 6 of 10 

Informe técnico: sistema de gestión del Laboratorio de Electrónica 

```
    +sistema
    +frame_actual
    +mostrar_login()
    +mostrar_sesion(usuario, es_nuevo)
  }
  class LoginFrame {
    +rol
    +entradas
    +ingresar()
  }
  class SesionFrame {
    +notebook
  }
  class InventarioTab {
    +busqueda
    +filtro
    +tree
    +refrescar()
    +eliminar()
  }
  class AgregarTab {
    +tipo
    +entradas
    +al_guardar
    +limpiar()
    +guardar()
  }
  class UsuariosTab {
    +tree
    +refrescar()
  }
  class SistemaInventario
  class Usuario
  class ComponenteElectronico
  Tk <|-- App
  Frame <|-- LoginFrame
  Frame <|-- SesionFrame
  Frame <|-- InventarioTab
  Frame <|-- AgregarTab
  Frame <|-- UsuariosTab
  App *-- SistemaInventario
  App o-- LoginFrame : muestra
  App o-- SesionFrame : muestra
  SesionFrame *-- InventarioTab
  SesionFrame *-- AgregarTab : solo Encargado
  SesionFrame *-- UsuariosTab : solo Encargado
```

Page 7 of 10 

Informe técnico: sistema de gestión del Laboratorio de Electrónica 

```
  AgregarTab ..> InventarioTab : al_guardar refresca
  LoginFrame ..> Usuario : crea
  SesionFrame ..> Usuario : recibe
  InventarioTab ..> SistemaInventario
  AgregarTab ..> SistemaInventario
  UsuariosTab ..> SistemaInventario
  AgregarTab ..> ComponenteElectronico : instancia subclase
```

## 8. Diagrama de secuencia 

Recorre el flujo completo del Encargado en la interfaz gráfica: inicia sesión y registra un componente. 

```
sequenceDiagram
  actor E as Encargado
  participant L as LoginFrame
  participant A as App
  participant S as SistemaInventario
  participant T as AgregarTab
  participant C as Componente
  participant DB as SQLite
  E->>L: nombre, código y cubículo
  L->>L: ingresar() valida campos
  L->>S: guardar_usuario(Encargado)
  S->>DB: SELECT y INSERT o UPDATE
  DB-->>S: resultado
  S-->>L: es_nuevo
  L->>A: mostrar_sesion(usuario, es_nuevo)
  A-->>E: SesionFrame y saludo
  E->>T: llena el formulario y pulsa Guardar
  T->>T: valida campos y cantidad
  T->>S: existe_item(id)
  S->>DB: SELECT
  DB-->>S: fila o nada
  alt el ID ya existe
    T-->>E: pregunta si desea reemplazar
    E->>T: confirma
  end
  T->>C: crea instancia de la subclase
  T->>S: guardar_item(item)
  S->>C: get_db_data()
  C-->>S: tipo, attr1, attr2
  S->>DB: INSERT OR REPLACE
  T-->>E: mensaje de éxito
  T->>T: limpiar() y refrescar inventario
```

Page 8 of 10 

Informe técnico: sistema de gestión del Laboratorio de Electrónica 

## 9. Relación entre los módulos 

Las flechas indican «importa a». `sistema.py` es el centro: ninguna interfaz toca la base de datos directamente. 

```
flowchart TD
  MAIN[main.py] --> GUI[gui.py]
  MAINC[main consola.py] --> SIS[sistema.py]
  MAINC --> USU[usuarios.py]
  GUI --> SIS
  GUI --> USU
  GUI --> COMP[componentes.py]
  USU --> UTIL[utilidades.py]
  USU --> COMP
  SIS --> COMP
  SIS --> CFG[config.py]
```

La versión de consola reutiliza los mismos objetos: los menús viven en `Estudiante.mostrar_menu_rol()` y `Encargado.mostrar_menu_rol()` , y usan los métodos de consola de `SistemaInventario` ( `agregar_item` , `eliminar_item` , `mostrar_inventario` , `mostrar_usuarios` ), que envuelven a los métodos de la GUI ( `guardar_item` , `borrar_item` , `listar_componentes` , `listar_usuarios` ). 

## 10. Conceptos de programación orientada a objetos aplicados 

- **Herencia:** las 9 clases de componentes heredan de `ComponenteElectronico` ; `Estudiante` y `Encargado` heredan de `Usuario` . 

- **Polimorfismo:** `obtener_detalles()` , `get_db_data()` y `mostrar_menu_rol()` se comportan distinto según la subclase, y el resto del código los llama sin conocer el tipo concreto. 

- **Encapsulamiento:** el acceso a SQLite está aislado en `SistemaInventario` ; `extra` es una propiedad de solo lectura en los usuarios. 

- **Composición:** `App` tiene un `SistemaInventario` ; `SesionFrame` contiene sus pestañas. 

- **Gestor de contexto:** `_conexion()` garantiza que la conexión se cierre aunque ocurra un error. 

Page 9 of 10 

Informe técnico: sistema de gestión del Laboratorio de Electrónica 

## 11. Observaciones y posibles mejoras 

- **Sin autenticación real:** cualquiera puede ingresar como Encargado escribiendo cualquier nombre y código. Convendría agregar contraseña o una lista de encargados autorizados. 

- **Especificaciones frágiles en la GUI:** `InventarioTab` obtiene las especificaciones cortando el texto de `obtener_detalles()` por `" | "` . Si un valor contiene ese separador, la columna se descuadra. Sería más robusto exponer un método que devuelva los datos ya separados. 

- **Esquema genérico:** `attr1` y `attr2` se guardan como texto, así que no se puede filtrar ni ordenar por valores numéricos como el voltaje o la tolerancia. 

- **Consola sin aviso de duplicados:** a diferencia de la GUI, la versión de consola reemplaza en silencio un componente con ID repetido ( `INSERT OR REPLACE` ). 

- **Sin edición directa:** para modificar un componente hay que volver a registrarlo con el mismo ID. 

- **Sin préstamos:** el sistema solo lleva existencias; no registra quién retira o devuelve un componente. 

- **Nombre del archivo de consola:** `main consola.py` tiene un espacio, lo que dificulta ejecutarlo o importarlo; además los comentarios lo mencionan como `main_consola.py` . 

Page 10 of 10 

