#!/usr/bin/env python

# eliminamos muchas coincidencias erróneas mediante el "ratio test"

import cv2 as cv
import time
import glob
import matplotlib.pyplot as plt

from umucv.stream import autoStream
from umucv.util import putText


def readmodels(file):
    return cv.imread(file)

# para calcular coincidencias de keypoints entre imagenes    
matcher = cv.BFMatcher()

# modelos de prueba
models = [readmodels(file) for file in sorted(glob.glob('sift/modelos/*.*'))]


#cap = cv.VideoCapture(0)

# El paso siguiente es necesario para capturar una camara ip en una red local domestica
# en el caso de usar camara usb o integrada usar el otro y comentar este

cap = cv.VideoCapture("https://192.168.1.44:8080/video")


sift = cv.xfeatures2d.SIFT_create(nfeatures=500)

# los puntos SIFT de los modelos
dms = [sift.detectAndCompute(x,None) for x in models]


# ratio test
# nos quedamos solo con las coincidencias que son mucho mejores que
# que la segunda, si un punto se parece más o menos lo mismo
# a dos puntos diferentes del modelo lo eliminamos.
def comparador(descriptores, keypoints, frame):
    modelo = 0
    good = []
    mejor = []
    for m in range(len(models)):
        # las coincidencias que ocurren
        matches = matcher.knnMatch(descriptores,dms[m][1],k=2)
        
        # solo guardaremos las mejores coincidencias
        good = []
        for match in matches:
            if len(match) == 2:
                best, second = match
                if best.distance < 0.75*second.distance:
                    good.append(best)
                
        # busqueda del mejor modelo
        if len(good) > len(mejor):
            modelo = m
            mejor = good
    
    #print('modelo: {}, imagen: {}'.format(len(dms[modelo][1]), len(descriptores)))
    #print('el modelo es el: ',modelo)
    #print('coincidencias: {} ({:.1f}%)'.format(len(mejor),100*len(mejor)/len(descriptores)))
    
        
    imgm = cv.drawMatches(frame, keypoints, models[modelo], dms[modelo][0], mejor,
                          flags=0,
                          matchColor=(128,255,128),
                          singlePointColor = (128,128,128),
                          outImg=None)
    
    return (mejor, imgm)

while True:

    key = cv.waitKey(1) & 0xFF
    if key == 27: break

    ret, frame = cap.read()
    # cambiar la resolución de la imagen para ser una cuarta parte de la original
    # necesario para evitar que se ralentice mucho la imagen
    frame = cv.resize(frame, (0,0), None, .5, .5)

    t0 = time.time()
    
    # Calculamos los k y d de la imagen actual
    keypoints, descriptors = sift.detectAndCompute(frame, mask=None)
    
    t1 = time.time()
    
    putText(frame, f'{len(keypoints)} pts  {1000*(t1-t0):.0f} ms')

    imgm = frame
    if(len(descriptors)>0):
        t2 = time.time()
        # solicitamos las dos mejores coincidencias de cada punto, no solo la mejor
        (good, imgm) = comparador(descriptors, keypoints, frame)
        #matches = matcher.knnMatch(descriptors, d0, k=2)
        t3 = time.time()


          
    cv.imshow("SIFT",imgm)


