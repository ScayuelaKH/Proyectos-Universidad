# Proyecto Visión Artificial

Esta es la versión final del proyecto de la asignatura de Visión Artificial. Nos enseñan a trabajar con las librerias de Python "numpy", "matlplotlib" y el uso de OpenCV.
Consiste en la resolución de una serie de ejercicios siendo cada uno independiente (en cierto grado) de los otros. Importante destacar que se realizó en una máquina con distribución de Linux, por lo que es necesaria una a la hora de ejecutar los programas. 

## Índice

* [Tecnologías usadas](#tecnologías-usadas)
* [Instalación](#instalación)

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


> Necesario el uso de cámara


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



### Color



### Filtros



### SIFT


