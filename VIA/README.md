# Proyecto Visión Artificial

Esta es la versión final del proyecto de la asignatura de Visión Artificial. Nos enseñan a trabajar con las librerias de Python "numpy", "matlplotlib" y el uso de OpenCV.
Consiste en la resolución de una serie de ejercicios siendo cada uno independiente (en cierto grado) de los otros. Importante destacar que se realizó en una máquina con distribución de Linux, por lo que es necesaria una a la hora de ejecutar los programas. 

## Índice

* [Tecnologías usadas](#tecnologías-usadas)
* [Instalación](#instalación)
* [Programas](#programas)
* [Medición de ángulos](#medición-de-ángulos)
* [Actividad](#actividad)
* [Color](#color)
* [Filtros](#filtros)
* [SIFT](#sift)

## Tecnologías usadas

* Python 3.7
* Miniconda
* OpenCV
* Jupyter Notebooks

## Instalación

Se necesita usar una máquina con Linux, en mi caso usé Ubuntu20.04, instalarle python 3 y también miniconda. Tras la instalación se deberá crear un entorno de conda, la forma más rápida es descargar un miniconda especial haciendo:
```
wget https://robot.inf.um.es/material/va/via-local.zip
unzip via-local.zip
cd via-local
conda create --name via --file visionreqlocal.txt
conda activate via
bash install-pip.sh
```
Al terminar la instalación se puede comenzar a probar los programas, pero no todos, algunos de ellos no necesitan hacer uso de cámara mientras que hay otros que sí. 
Para circunvalar este problema podemos hacer uso de la cámara de nuestro móvil mediante, por ejemplo, la aplicación **IP webcam** o alguna parecida. Normalmente para hacer uso de esta es necesario pasarle como parámetro la IP al programa, pero para evitar tener que repetirlo todo el rato se hace uso de un fichero de texto llamado **alias.txt** dentro de este proyecto donde podremos ponerle un alias a la IP, siendo este predeterminado "**phone**". 

## Programas

Estos son las resoluciones de los ejercicios que se nos pedían, a la hora de probarlos hay que destacar ciertos detalles para poder probarlos en su integridad:
* En algunos es necesaria la entrada del usuario para controlar lo que sucede, para ello se ha implementado un menú de ayuda al cual se puede acceder oprimiendo la tecla "**h**".
* En algunos es necesario usar una cámara, para ello se puede ejecutar el programa poniendo como parámetro "**--dev=phone**".
En los casos en los que fuese necesario se informaría de su necesidad de uso.

### Medición de ángulos


> Necesario el uso de cámara, aunque también aplicable a imágenes que tengamos guardadas


*Resumen:* Con este programa calibraremos nuestra cámara para poder crear una aplicación de medir grados dados dos puntos en la imagen. Para ello necesitaremos saber cual es la **distancia focal** de nuestra cámara y luego realizar una calibración aproximada 

> Pasos opcionales si ya conocemos la distancia focal de nuestra cámara.
> 
>> * Para empezar es necesario hacer una calibración precisa de la cámara usando un patrón de "**chessboard**", se ha de abrir la imágen **pattern.png** que se encuentra dentro de la carpeta "**calibrate**" y con la cámara que se quiere calibrar sacarle fotos desde distintos ángulos. En el caso de ejemplo bajé la resolución a la mitad para poder trabajar de manera más cómoda aunque no es obligatorio hacerlo. Una vez se tienen las fotos se han de guardar en la carpeta "**calibrate**", además de borrar las que ya había (si no se había hecho anteriormente). 
>>
>> ![image](https://user-images.githubusercontent.com/33126016/147234570-e48d5baa-2f5f-40ca-9958-66dc2f9babc5.png "Ejemplo de resultado de calibración")
>>
>>   * El siguiente paso es ejecutar el programa "**calibrate.py**" pasandole como argumento las imágenes de la carpeta (menos la del patrón), para poder así obtener la "**distancia focal** de nuestra cámara, lo podemos encontrar como el primer valor de la matriz de cámara, y el **error cuadrático medio**. Este último cuanto menor sea mejor cálculo de la distancia focal habremos realizado y mejor podremos calcular los ángulos.
 
* Probamos a medir ángulos, pero antes se debe abrir el programa "**medidor_grados.py**" con un editor de texto cualquiera y modificar el valor de la variable "**f**" por el de nuestra distancia focal. Tras ello ejecutar (dentro de nuestro entorno de anaconda previamente creado) el programa con el parámetro de la cámara y pinchar en la ventana creada los dos puntos entre los que queremos sacar el ángulo.
![image](https://user-images.githubusercontent.com/33126016/147234432-a1f19c05-95a3-4593-a18c-bda8eb377d7c.png "Ejemplo de medida de grados")

### Actividad

> Necesario el uso de cámara

> Incluido con menú de ayuda

*Resumen:* Podremos tener nuestra propia cámara de seguridad, al ejecutar el programa seleccionaremos una zona a monitorizar y si se detecta movimiento se grabará lo que ocurra.

Ejecutamos el programa "**actividad.py**", se nos abrirá una ventana con la vista de la cámara, en ella podremos seleccionar una zona pinchando y arrastrando con el ratón. Una vez seleccionada, para empezar a monitorizar pulsar la tecla "**c**", y si en algún momento se quiere cambiar la zona de monitoreo se puede pulsar la tecla "**x**" para reiniciar todo el proceso. Se comenzará a grabar si se detecta un cambio significativo en la zona seleccionada y no se parará hasta que vuelva al estado original. Al terminar el programa se guardará el video grabado en la misma carpeta.

### Color

> Necesario el uso de cámara, aunque también aplicable a imágenes que tengamos guardadas

> Incluido con menú de ayuda

*Resumen:* Crearemos un clasificador de objetos basándonos en la similitud de los colores de las zonas seleccionadas. 

Ejecutamos el programa "**color.py**", se nos abrirá una ventana con la vista de la cámara, en ella podremos seleccionar una zona pinchando y arrastrando con el ratón. Si ese lo queremos guardar como modelo para comparar con otras zonas pulsar la tecla "**g**", los iremos guardando y mostrando en una ventana denominada "modelos", y si en cambio queremos deseleccionar la zona y escoger otra pulsar la tecla "**x**". También podremos ver el **histograma** de colores de la zona pulsando la tecla "**r**", si además tenemos ya guardado algún modelo que se le parezca los mostraremos en otra ventana llamada "detectados". En la ventana de la cámara podremos encontrar arriba a la izquierda la similitud de los modelos con la zona detectada (pulsar **r** para actualizar en cada caso) en el mismo orden que en su respectiva ventana, y siempre que supere un threshold del 85% lo mostraremos como detectado.

![image](https://user-images.githubusercontent.com/33126016/147240862-2f62a393-0b4c-4acf-996f-9613592cefe6.png "Ejemplo con las tres ventanas")

### Filtros

> Necesario el uso de cámara, aunque también aplicable a imágenes que tengamos guardadas

> Incluido con menú de ayuda

*Resumen:* Podremos aplicar filtros a una zona que seleccionemos de la imágen, además de poder regular sus efectos usando barras deslizantes.

Ejecutamos el programa "**filtros.py**", se nos abrirá una ventana con la vista de la cámara, en ella podremos seleccionar una zona pinchando y arrastrando con el ratón. Teniendo la zona seleccionada podremos aplicarle una selección de filtros según que teclas se pulsen y posteriormente controlar el efecto que tienen usando las barras deslizantes que aparecen en la parte inferior de la ventana:

* **Median Filter:** aplicado al pulsar la tecla **m**, con este conseguimos suavizar la imagen, lo podemos desactivar volviendo a pulsar la tecla.

![image](https://user-images.githubusercontent.com/33126016/147269369-7d6db650-d37a-4bb7-8f9f-c4ebeb3f39f6.png "Efecto aplicando el efecto Median filter")

* **Gaussian Filter:** aplicado al pulsar la tecla **g**, con este conseguimos desenfocar la imagen, lo podemos desactivar volviendo a pulsar la tecla.

![image](https://user-images.githubusercontent.com/33126016/147269407-c6998622-5b17-472b-aa96-4f8aa7539ec1.png "Efecto aplicando el efecto Gaussian filter")

* **Blanco/Negro:** aplicado al pulsar la tecla **r**, cambia los colores a una escala de blancos y negros, este solo puede activarse o desactivarse.

![image](https://user-images.githubusercontent.com/33126016/147269344-6b5aefb8-cc7e-4fca-b982-99f3cd2a595d.png "Ejemplo aplicando el efecto de blanco/negro")

Los efectos se pueden superponer entre sí, y pulsando la tecla **x** deseleccionaremos la zona y quitaremos los filtros aplicados.

![image](https://user-images.githubusercontent.com/33126016/147269718-6274efdf-6e89-4da0-b1e7-0d622ca9e1c7.png "Ejemplo donde se han aplicado varios filtros")


### SIFT

> Necesario el uso de cámara, aunque también aplicable a imágenes que tengamos guardadas

*Resumen:* Aplicación de reconocimiento de objetos basada en número de coincidencias de "keypoints".

Con este programa necesitamos tener unas imágenes que vamos a proporcionar como modelo, tras lo cual al usar la cámara irá cogiendo lo que vé y calcula los aciertos que encuentra con los modelos que tiene de base. En la ventana podremos observar a la izquierda la imágen del modelo que más se parece con lo que se le enseña por cámara (que aparece al lado derecho). 

![image](https://user-images.githubusercontent.com/33126016/147271095-bcfcba00-8bbf-4a54-a5d8-e70b9e4197fc.png "Ejemplo del programa reconociendo la imagen")

Se puede probar con ejemplos caseros colocando aquellas imágenes a usar en la carpeta "**sift/modelos**". 
Ojo, en este programa no es tan sencillo usar la cámara del móvil, por defecto tratará de usar la propia cámara integrada por el ordenador, se puede cambiar modificando un par de líneas de código:

```
cap = cv.VideoCapture(0)
#El paso siguiente es necesario para capturar una camara ip en una red local domestica
#cap = cv.VideoCapture("url del móvil")
#en el caso de usar camara usb o integrada usar el otro y comentar este
```
