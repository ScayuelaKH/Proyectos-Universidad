#!/usr/bin/env python

# ejemplo de selección de ROI

import numpy as np
import cv2 as cv

from umucv.util import ROI, putText
from umucv.stream import autoStream
from umucv.util import Help


cv.namedWindow("input")
cv.moveWindow('input', 0, 0)


region = ROI("input")

help = Help(
"""
VENTANA AYUDA
Esta aplicacion te permite seleccionar
una region de la imagen a la cual
aplicarle uno de los filtros disponibles.
Una vez seleccionada has de pulsar los botones
siguientes para aplicarle el filtro y 
posteriormente usar las barras de debajo
para aumentar/disminuir su efecto si es que
se pudiese.

g: Gaussian Blur

m: Median Blur

r: Blanco/Negro

SPC: pausa
x: deseleccionar zona
h: mostrar/ocultar ayuda
""")


def nada(v):
    pass
    
cv.createTrackbar("GaussianBlur", "input", 1, 255, nada)
cv.createTrackbar("MedianBlur", "input", 1, 255, nada)


gaussian = False
median = False
gray = False
sel = False
H = None

for key, frame in autoStream():
    
    help.show_if(key, ord('h'))

    if region.roi:

        [x1,y1,x2,y2] = region.roi
        trozo = frame[y1:y2+1, x1:x2+1]    
        
        if(not sel):
            cv.rectangle(frame, (x1,y1), (x2,y2), color=(0,255,255), thickness=2)
        
        if key == ord('x'):
            median = False
            gaussian = False
            gray = False
            sel = False
            region.roi = []
        
        if key == ord('g'):
            sel = True
            gaussian = True
        
        if key == ord('m'):
            sel = True
            median = True
        
            
        if key == ord('r'):
            gray = not gray
    
        
        if gaussian:
            H = cv.getTrackbarPos('GaussianBlur','input')
            if(H == 0):
                H = 1
            frame[y1:y2+1, x1:x2+1] = cv.GaussianBlur(trozo,(0,0),H)

        if median:
            H = cv.getTrackbarPos('MedianBlur','input')
            if(H == 0):
                H = 1
            elif((H % 2) == 0):
                H -= 1
            frame[y1:y2+1, x1:x2+1] = cv.medianBlur(trozo,H)
            
        if gray:
            porcion = cv.bitwise_not(cv.cvtColor(trozo,cv.COLOR_RGB2GRAY))
            result = cv.merge([porcion, porcion, porcion])
            frame[y1:y2+1, x1:x2+1] = result
        
    cv.imshow('input',frame)

