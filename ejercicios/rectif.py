#!/usr/bin/env python

import cv2 as cv
from umucv.stream import autoStream
from collections import deque
import numpy as np
from umucv.util import putText
import os.path
from umucv.util import Help

help = Help(
"""
VENTANA AYUDA
Selecciona cuatro puntos para poder rectificar la imagen
(si te equivocas poniendo uno presion el boton de la rueda del
raton para modificar su posicion)

r: cuando tienes colocados los cuatro puntos rectifica la imagen

g: al rectificar la imagen guardas los puntos en un '.txt'

x: borrar los puntos


h: mostrar/ocultar ayuda
""")
# convierte un conjunto de puntos ordinarios (almacenados como filas de la matriz de entrada)
# en coordenas homogéneas (añadimos una columna de 1)
def homog(x):
    ax = np.array(x)
    uc = np.ones(ax.shape[:-1]+(1,))
    return np.append(ax,uc,axis=-1)

# convierte en coordenadas tradicionales
def inhomog(x):
    ax = np.array(x)
    return ax[..., :-1] / ax[...,[-1]]

# estas dos funciones funcionan en espacios de cualquier dimensión.

# aplica una transformación homogénea h a un conjunto
# de puntos ordinarios, almacenados como filas
def htrans(h,x):
    return inhomog(homog(x) @ h.T)
    
def desp(d):
    dx,dy = d
    return np.array([
            [1,0,dx],
            [0,1,dy],
            [0,0,1]])

# guardo los puntos seleccionados en un '.txt' nuevo
def guardar_puntos(puntos_H):
    dupl = ''
    while os.path.isfile('Puntos_Rectif'+dupl+'.txt') and puntos_H is None:
        if dupl == '':
            dupl = str(0)
        else: dupl = str(int(dupl)+1)
        
    if puntos_H is None:
        archivo = 'Puntos_Rectif'+dupl+'.txt'
        puntos_H = open(archivo,"w")
    else:
        puntos_H.seek(0)
        puntos_H.truncate()
        
    it = 0
    puntos_H.write('Puntos cogidos:\n')
    puntos_H.write('[')    
    while it != len(points):
        linea = [str(a) for a in points[it]]
        aux = '('+linea[0]+', '+linea[1]+')'
        if it != len(points)-1:
            aux += ',\n'
        puntos_H.write(aux)
        it += 1
    puntos_H.write(']\n\n')
    puntos_H.write('Width: '+str(width_real)+'\n')
    puntos_H.write('Height: '+str(height_real)+'\n')
    return puntos_H

# para calcular el desplazamiento de la imagen en la homografia
def calcularDesplazamiento(size):
    desplazamiento = None
    if size is None:
        iterador = 0
        lista_x = list()
        lista_y = list()
        while iterador != len(aux):
            x,y = aux[iterador]
            lista_x.append(int(x))
            lista_y.append(int(y))
            iterador += 1
        xmax = max(lista_x)
        ymax = max(lista_y)
        xmin = min(lista_x)
        ymin = min(lista_y)
        size = (xmax-xmin,ymax-ymin)
        despx = x0-xmin
        despy = y0-ymin
        desplazamiento = desp((despx, float(despy)))
    return desplazamiento

def fun(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        points.append((x,y))
    if event == cv.EVENT_MBUTTONDOWN:
        points.pop()
        points.append((x,y))

def medidor(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        medir.append((x,y))
    
        

        
cv.namedWindow("rectificado")
cv.namedWindow("webcam")

cv.setMouseCallback("webcam", fun)
cv.setMouseCallback("rectificado",medidor)

#-----------------#
# comentar la otra y completar esta con los puntos guardados a probar
# poniendolos ante de la coma

#points = deque([(459, 255),
#(628, 307),
#(505, 558),
#(326, 461)],maxlen=4)

points = deque(maxlen=4)


medir = deque(maxlen=2)

d1 = d2 = 0
x0 = y0 = 0

#height_real = width_real = 0

# modificar con las medidas de anchura y altura de la vida real en milimetros
height_real = 56
width_real = 84

size = None
rec = None
puntos_H = None
aux = 0
# si he puesto los puntos de antemano rectifico la imagen directamente
if(len(points) != 0):
    seleccionar = True
else: seleccionar = False

# matriz de la posicion real
real = np.array([
    [  0.,  0.],
    [  0.,  0.+height_real],
    [  0.+width_real,  0.+height_real],
    [  0.+width_real,  0.]]) 
    
    
for key, frame in autoStream():

    x,y,_ = frame.shape
    esquinas = ((0,0),(0,y),(x,0),(x,y))
    
    if key == ord('x'):
        points.clear()
        seleccionar = False
        rec = None
        size = None

    # confirmo la seleccion de los cuatro puntos
    if key == ord('r'):
        seleccionar = True
    
    # procedemos a rectificar la imagen
    if seleccionar and len(points) == 4:
        if key == ord('g'):
            puntos_H = guardar_puntos(puntos_H)

        lista = np.asarray(points)
        H,_ = cv.findHomography(lista, real)
        aux = htrans(H,esquinas)
        desplazamiento = calcularDesplazamiento(size)

        rec = cv.warpPerspective(frame, desplazamiento@H, size)
    
    # una vez rectificada la imagen podemos medir en ella
    if rec is not None:
        for m in medir:
            cv.circle(rec, m, 3, (0,0,255), -1)
        if(len(medir) == 2):
            cv.line(rec, medir[0],medir[1],(0,0,255))

            c = np.mean(medir, axis=0).astype(int)
            d = np.linalg.norm(np.asarray(medir[0])-medir[1])
            
            putText(rec,f'{d:.1f} mm',c)
        cv.imshow('rectificado',rec)

    for p in points:
        cv.circle(frame, p,3,(0,0,255),-1)

    cv.imshow('webcam',frame)
if puntos_H is not None:
    puntos_H.close()
cv.destroyAllWindows()

