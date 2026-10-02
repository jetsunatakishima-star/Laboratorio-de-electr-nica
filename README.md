# Laboratorio-de-electronic
# INFORME DEL SISTEMA DE GESTIÓN DE INVENTARIO DEL LABORATORIO DE ELECTRÓNICA

## 1. Introducción

En este proyecto se desarrolló un programa en Python para administrar el inventario de un laboratorio de electrónica. El sistema permite registrar, consultar y eliminar diferentes componentes electrónicos, además de guardar la información en un archivo de texto para que los datos no se pierdan al cerrar el programa.

Para realizar el programa se utilizó principalmente el concepto de **programación orientada a objetos (POO)**, utilizando clases, objetos, herencia y métodos. También se implementó un sistema de usuarios con diferentes roles, permitiendo que los estudiantes puedan consultar el inventario y que el encargado del laboratorio pueda administrar los componentes.

## 2. Objetivo general

Desarrollar un sistema en Python que permita gestionar de manera organizada el inventario de un laboratorio de electrónica mediante el uso de programación orientada a objetos y almacenamiento de información en un archivo de texto.

## 3. Objetivos específicos

* Crear clases para representar los diferentes componentes electrónicos.
* Utilizar herencia para organizar las diferentes clases de componentes.
* Permitir registrar nuevos componentes en el inventario.
* Permitir eliminar componentes utilizando su ID.
* Mostrar la información completa del inventario.
* Crear diferentes tipos de usuarios y asignarles funciones según su rol.
* Guardar la información en un archivo de texto.
* Cargar automáticamente la información guardada cuando se inicia el programa.

## 4. Desarrollo del programa

### 4.1 Importación y archivo de almacenamiento

Al comienzo del programa se utiliza:

`import os`

Esta librería permite trabajar con elementos del sistema operativo. En este caso se utiliza para comprobar si existe el archivo donde se almacena el inventario.

También se define:

`ARCHIVO_DB = "inventario.txt"`

Este archivo funciona como una pequeña base de datos en texto plano donde se guardan los componentes registrados.

## 5. Clase principal

La clase principal del programa se llama `ComponenteElectronico`.

Esta clase contiene los datos básicos que tienen todos los componentes:

* ID
* Nombre
* Cantidad
* Ubicación

Además, posee los métodos `obtener_detalles()` y `to_string()`.

El método `obtener_detalles()` permite mostrar la información del componente de una manera organizada.

El método `to_string()` convierte la información del objeto en una cadena de texto que posteriormente puede ser guardada en el archivo `inventario.txt`.

## 6. Clases de componentes electrónicos

A partir de la clase principal se crearon diferentes clases hijas. Esto permite utilizar **herencia**, ya que cada componente conserva las características generales de `ComponenteElectronico`, pero además tiene características propias.

Las clases creadas son:

### Resistencia

Guarda información como:

* Valor en ohmios.
* Tolerancia.

### Condensador

Guarda:

* Capacitancia.
* Voltaje máximo.

### Bobina

Guarda:

* Inductancia.
* Corriente máxima.

### Diodo

Guarda:

* Tipo de diodo.
* Corriente máxima.

### Transistor

Guarda:

* Tipo de transistor.
* Tipo de encapsulado.

### Circuito integrado

Guarda:

* Número de pines.
* Función principal.

### Microcontrolador

Guarda:

* Voltaje de operación.
* Velocidad de reloj.

### Sensor

Guarda:

* Magnitud que mide.
* Interfaz de comunicación.

### Instrumento de laboratorio

Guarda:

* Marca.
* Precisión o rango.

Cada una de estas clases tiene su propio método `obtener_detalles()` y `to_string()`, adaptados a las características del componente.

## 7. Sistema de usuarios

El programa también cuenta con una clase llamada `Usuario`, que funciona como clase base para los diferentes tipos de usuarios.

Se crearon dos tipos principales:

### Estudiante

El estudiante tiene:

* Nombre.
* Carnet.
* Carrera.

Su función principal es consultar el inventario completo del laboratorio. El menú le permite ver el inventario o cerrar sesión.

### Encargado del laboratorio

El encargado tiene:

* Nombre.
* Código o carnet.
* Cubículo.

Tiene más permisos que el estudiante. Puede registrar diferentes componentes, eliminar componentes por ID, consultar el inventario y cerrar sesión.

## 8. Sistema de inventario

La clase `SistemaInventario` es la encargada de controlar las operaciones principales del programa.

Al iniciar, crea una lista llamada `inventario` y posteriormente intenta cargar los datos almacenados en el archivo.

Entre sus principales funciones están:

### Agregar componentes

El método `agregar_item()` añade un nuevo objeto a la lista del inventario y posteriormente guarda la información en el archivo.

### Eliminar componentes

El método `eliminar_item()` busca un componente mediante su ID. Si lo encuentra, lo elimina del inventario y actualiza el archivo.

### Mostrar inventario

El método `mostrar_inventario()` recorre todos los objetos almacenados y muestra sus características utilizando el método `obtener_detalles()`.

## 9. Almacenamiento de información

Una parte importante del proyecto es que la información no solamente permanece mientras el programa está abierto.

El método `guardar_en_archivo()` abre el archivo `inventario.txt` y escribe la información de cada componente.

Por otra parte, `cargar_desde_archivo()` verifica si el archivo existe y, si existe, lee cada línea para reconstruir los objetos correspondientes.

El programa identifica el tipo de componente mediante la primera información almacenada en cada línea. Por ejemplo, si encuentra `"Resistencia"`, crea nuevamente un objeto de la clase `Resistencia`.

Esto permite que el inventario se conserve aunque el programa sea cerrado.

## 10. Ejecución principal

La función `main()` es la encargada de iniciar el sistema.

Cuando se ejecuta el programa aparecen tres opciones:

1. Ingresar como estudiante.
2. Ingresar como encargado de laboratorio.
3. Salir.

Dependiendo de la opción seleccionada, el programa crea un objeto de tipo `Estudiante` o `Encargado` y muestra el menú correspondiente.

Finalmente, la instrucción:

`if __name__ == "__main__":`

permite ejecutar la función `main()` cuando el archivo Python se ejecuta directamente.

## 11. Conceptos de programación utilizados

Durante el desarrollo del programa se utilizaron varios conceptos de programación orientada a objetos:

**Clases:**
Se utilizan para crear modelos de componentes y usuarios.

**Objetos:**
Representan elementos concretos del inventario, como una resistencia, un sensor o un microcontrolador.

**Herencia:**
Las clases específicas como `Resistencia`, `Diodo` o `Sensor` heredan las características de `ComponenteElectronico`.

**Encapsulamiento:**
La información de cada objeto se mantiene organizada dentro de sus respectivas clases y atributos.

**Métodos:**
Permiten realizar acciones como mostrar información, guardar datos, agregar componentes y eliminarlos.

**Polimorfismo:**
Las diferentes clases tienen métodos con el mismo nombre, como `obtener_detalles()`, pero cada clase muestra información adicional dependiendo del tipo de componente.

## 12. Funcionamiento general

El funcionamiento del programa puede resumirse de la siguiente manera:

**Inicio del programa → Cargar inventario → Seleccionar tipo de usuario → Mostrar menú → Realizar acción → Actualizar inventario → Guardar información → Continuar o cerrar sesión.**

De esta manera, el sistema permite llevar un control organizado de los componentes electrónicos disponibles en el laboratorio.

## 13. Resultados

Como resultado se obtuvo un sistema capaz de administrar diferentes tipos de componentes electrónicos. El programa permite registrar componentes con información específica, consultar el inventario, eliminar elementos y conservar los datos mediante un archivo de texto.

También se logró diferenciar las funciones de los estudiantes y del encargado del laboratorio mediante diferentes menús.

## 14. Conclusiones

El desarrollo de este proyecto permitió aplicar los conocimientos de programación orientada a objetos en una situación práctica relacionada con un laboratorio de electrónica.

Se aprendió a utilizar clases, objetos, herencia y métodos para organizar mejor un programa. Además, se implementó el almacenamiento de información en un archivo de texto, lo que permite conservar el inventario después de cerrar el programa.

El sistema facilita la organización de los componentes electrónicos y demuestra cómo Python puede utilizarse para crear programas que solucionen necesidades reales de organización y administración.

## 15. Recomendaciones

Como posibles mejoras para una futura versión se podrían agregar un sistema de inicio de sesión con contraseña, búsqueda de componentes por nombre o tipo, modificación de cantidades, control de préstamos y devoluciones, y una interfaz gráfica para hacer que el programa sea más fácil de utilizar.
