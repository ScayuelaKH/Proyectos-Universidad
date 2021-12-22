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
* En algunos es necesario usar una cámara, para ello se puede ejecutar el programa poniendo como argumento "**--dev=phone**".
En los casos en los que fuese necesario se informaría de su necesidad de uso.

### Calibración


> Necesario el uso de cámara


*Resumen:* Con este programa calibraremos nuestra cámara para poder crear una aplicación de medir grados dados dos puntos en la imagen.

* Para empezar es necesario hacer una calibración precisa de la cámara usando un patrón de "**chessboard**", se ha de abrir la imágen **pattern.png** que se encuentra dentro de la carpeta "**calibrate**" y con la cámara que se quiere calibrar sacarle fotos desde distintos ángulos.


### Actividad



### Color



### Filtros



### SIFT


