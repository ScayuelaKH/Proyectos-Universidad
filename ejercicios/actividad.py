#!/usr/bin/env python

# ejemplo de selección de ROI

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

from umucv.util import ROI, putText, Video
from umucv.stream import autoStream
from umucv.util import Help

help = Help(
"""
VENTANA AYUDA
Seleccionar una zona con el botón izquierdo del ratón

c: capturar trozo a grabar

x: borrar trozo

h: mostrar/ocultar ayuda
""")
cv.namedWindow("input") #nombre ventana
cv.moveWindow('input', 0, 0) #la coloco en (0,0)

region = ROI("input") #variable donde guarda el ROI que se crea

video = Video(fps=20) #variable que se encarga del video
video.ON = True 

grabando = False #booleano para comprobar si debemos o no grabar
media = -1

og = None
for key, frame in autoStream(): #bucle de cada frame
    
    help.show_if(key, ord('h'))
    
    if region.roi: #si hemos seleccionado un roi
        [x1,y1,x2,y2] = region.roi #guardamos coordenadas del dibujo
        trozo = frame[y1:y2+1, x1:x2+1] #sacamos la region seleccionada
        
        
        if key == ord('c'): #si pulsamos c
            og = cv.cvtColor(trozo,cv.COLOR_BGR2GRAY)
            grabando = True
        
           
        if key == ord('x'):
            region.roi = [] #borramos la seleccion
                           
        if(grabando != False):
            if key == ord('x'):
                grabando = False
                media = -1
                region.roi = [] #borramos la seleccion
                continue #salimos para poder seleccionar otra zona

            # pasamos a gris la zona
            gray = cv.cvtColor(trozo,cv.COLOR_BGR2GRAY)
            # suavizamos los colores
            gray = cv.GaussianBlur(gray,(25,25),0)
            # calculamos la mascara con la diferencia del background con cada frame
            delta = cv.absdiff(og, gray)
            threshold = cv.threshold(delta, 35, 255, cv.THRESH_BINARY)[1]
            # pasamos la mascara a blancos y negros
            
            # si no tenemos el valor de la media "normal" lo asignamos
            if(media == -1):
                media = np.ceil(np.mean(threshold))
            cv.imshow('Threshold', threshold)
            #print(np.mean(threshold) > media)
            # si hay cambios en el ambiente se grabarán
            if(np.mean(threshold) > media):
                video.write(frame)


        #dibuja el rectangulo en cada frame
        cv.rectangle(frame, (x1,y1), (x2,y2), color=(0,255,255), thickness=2)
        putText(frame, f'{x2-x1+1}x{y2-y1+1}', orig=(x1,y1-8))
    #pone el tamaño en pixels de este en ocho unidades más arriba del y
    #ponemos el tamaño de la captura
    h,w,_ = frame.shape
    putText(frame, f'{w}x{h}')
    cv.imshow('input',frame)
    #lo mostramos

#es necesario destruir las ventanas y liberar el video al acabar el bucle
cv.destroyAllWindows()
video.release()

