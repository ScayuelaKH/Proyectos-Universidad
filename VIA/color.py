#!/usr/bin/env python

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from umucv.util import ROI, putText
from umucv.stream import autoStream
from umucv.util import Help

help = Help(
"""
VENTANA AYUDA
Seleccionar una zona con el botón izquierdo del raton.
Teniendo al menos un modelo guardado, si seleccionamos
otro trozo y mostramos el histograma, lo compararemos
con el de los modelos, y en caso de que se parezca alguno
mucho lo mostraremos en la ventana de zonas detectadas.

r: mostrar histogramas de zona seleccionada

g: capturar trozo para guardar como modelo

x: borrar trozo

h: mostrar/ocultar ayuda
""")

def normalizarHistogramas(m, histSize, histRange, accumulate):
    
    hist_bgr = cv.split(m)
    hist_b = cv.calcHist(hist_bgr, [0], None, [histSize], histRange, accumulate=accumulate)
    hist_g = cv.calcHist(hist_bgr, [1], None, [histSize], histRange, accumulate=accumulate)
    hist_r = cv.calcHist(hist_bgr, [2], None, [histSize], histRange, accumulate=accumulate) 
    
    hist_b = cv.normalize(hist_b, hist_b, 0, height, cv.NORM_MINMAX).flatten()
    hist_g = cv.normalize(hist_g, hist_g, 0, height, cv.NORM_MINMAX).flatten()
    hist_r = cv.normalize(hist_r, hist_r, 0, height, cv.NORM_MINMAX).flatten()
    
    return hist_b,hist_g,hist_r
    
def pintarHistograma(trozo, bin_w, height, hist_b, hist_g, hist_r, colores, i):
    cv.line(trozo, (bin_w*(i-1), height-int(hist_b[i-1])),(bin_w*(i),height-int(hist_b[i])),colores[0],2)
    
    cv.line(trozo, (bin_w*(i-1), height-int(hist_g[i-1])),(bin_w*(i),height-int(hist_g[i])),colores[1],2)
    
    cv.line(trozo, (bin_w*(i-1), height-int(hist_r[i-1])),(bin_w*(i),height-int(hist_r[i])),colores[2],2)

cv.namedWindow("input")
cv.moveWindow('input', 0, 0)

colores = [(255,0,0),(0,255,0),(0,0,255)]
seleccionado = False
region = ROI("input")

models = list()
canals = list()
red = list()
green = list()
blue = list()

img_negra = None
detectados = list()
sol = list()
tam = 1
revisado = True 
height = width = 0

detectado = False
threshold = 0.85
img = None
img2 = None
for ret, frame in autoStream():  

# selecciono la zona
    if region.roi:   
    
        [x1,y1,x2,y2] = region.roi
        cv.rectangle(frame, (x1,y1), (x2,y2), color=(0,255,255), thickness=2)

        trozo = frame[y1:y2+1, x1:x2+1] 
        
        # guardo modelos
        if ret == ord('g'):
            models.append(trozo.copy())
            # el primero que guardo lo uso como referencia para el tamaño del resto
            # creo la imagen negra que pondré en la ventana de detectados si no hay ninguno
            if len(models) == 1:
                img = models[0]
                height, width, _ = trozo.shape
                height = int(height)
                width = int(width)
                img_negra = np.zeros((height, width, 3), dtype=np.uint8)
       
        # selecciono con 'r' la zona roi que comparar con los modelos
        # si hay modelos los comparo con el trozo seleccionado
        # y muestro la diferencia numerica arriba a la izq
        # si esta es mayor a un 'threshold' muestro la imagen que lo cumple
        # en la ventana detectados     
        if ret == ord('r'):
            seleccionado = True
            revisado = False
            blue.clear()
            red.clear()
            green.clear()
            sol.clear()
            detectados.clear()
        
        # deselecciono la zona a comparar
        if ret == ord('x'):
            region.roi = []
            seleccionado = False
            # borro los histogramas calculados
            blue.clear()
            red.clear()
            green.clear()
            sol.clear()
            detectados.clear()
# muestro los histogramas de colores de la zona seleccionada
        if seleccionado:  
        
            histSize = 256
            
            histRange = (0, histSize)
            
            accumulate = False
            
            
            hist_b,hist_g,hist_r = normalizarHistogramas(trozo, histSize, histRange, accumulate)
            
            bin_w = int(round(width/histSize))
            for i in range(1, histSize):
                pintarHistograma(trozo, bin_w, height, hist_b, hist_g, hist_r, colores, i)
            
            if len(models) != 0:
                # comparo los histogramas de los modelos con el del trozo seleccionado
                for m in models:
                    hist_b1,hist_g1,hist_r1 = normalizarHistogramas(m, histSize, histRange, accumulate)
                    
                    blue.append(cv.compareHist(hist_b, hist_b1, cv.HISTCMP_CORREL))
                
                    green.append(cv.compareHist(hist_b, hist_b1, cv.HISTCMP_CORREL))
                
                    red.append(cv.compareHist(hist_b, hist_b1, cv.HISTCMP_CORREL))
        
            if not revisado:
                for i,_ in enumerate(models):
                    # el valor maximo de la diferencia entre histograma de modelos con el trozo seleccionado
                    result = round(np.amax([np.amax(red[i]),np.amax(blue[i]),np.amax(green[i])]),3)
                    # los voy guardando y los muestro por pantalla
                    sol.append(result)
                    # si supera el threshold lo muestro por detectados
                    if result > threshold:
                        detectados.append(i)
                        if len(detectados) == 1:
                            img2 = cv.resize(models[i],(width,height))
                            cv.imshow('detectados',img2)
                        elif len(detectados) > 1:
                            img_aux2 = cv.resize(models[i],(width,height))
                            img2 = cv.hconcat([img2,img_aux2])
                            cv.imshow('detectados',img2)
                    detectado = True
                revisado = True
                
# si tengo modelos almacenados, los muestro concatenados
# solo concateno imagenes nuevas, lo controlo mediante tam
    if len(models) >= tam:
# todas las imagenes se reescalan a un mismo tamaño para concatenarlas
        if len(models) > tam:
            img_aux = cv.resize(models[tam],(width,height))
            img = cv.hconcat([img,img_aux])
            tam += 1
        
        cv.imshow('modulos', img)
    
        if len(detectados) == 0:
            cv.imshow('detectados',img_negra)
        
            detectado = False
    putText(frame, f'{sol}')
    cv.imshow('input',frame)
    
    
    
cv.destroyAllWindows()

