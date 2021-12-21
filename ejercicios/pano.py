# utilidad para devolver el número de correspondencias y la homografía entre dos imágenes

import numpy as np
import cv2   as cv
import glob

import matplotlib.pyplot as plt

def fig(w,h):
    plt.figure(figsize=(w,h))

def readrgb(file):
    return cv.cvtColor( cv.imread(file), cv.COLOR_BGR2RGB) 


sift = cv.xfeatures2d.SIFT_create()
bf = cv.BFMatcher()

def match(query, model):
    x1 = query
    x2 = model
    (k1, d1) = sift.detectAndCompute(x1, None)
    (k2, d2) = sift.detectAndCompute(x2, None)
    matches = bf.knnMatch(d1,d2,k=2)

    # ratio test
    good = []
    for m in matches:
        if len(m) == 2:
            best, second = m
            if best.distance < 0.75*second.distance:
                good.append(best)

    src_pts = np.array([ k2[m.trainIdx].pt for m in good ]).astype(np.float32).reshape(-1,2)
    dst_pts = np.array([ k1[m.queryIdx].pt for m in good ]).astype(np.float32).reshape(-1,2)

    H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 3)
    
    return sum(mask.flatten()>0), H

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

# buscamos la imagen con más matches significativos con el resto y la guardamos para usarla como base
def buscar_base(matches):
    lista_mejores = list()
    iterador = 0
    while(iterador != len(matches)):
        (m,a,b) = matches[iterador]
        if(m >= 20):
            lista_mejores.append(a)
            lista_mejores.append(b)
        iterador += 1
    return(max(set(lista_mejores), key=lista_mejores.count))
    
# sacamos los puntos maximos y minimos de las esquinas del marco comun
def comprobar_esquinas(esquinas,xmax,ymax,xmin,ymin):
# compruebo las esquinas de la imagen en el espacio de la base
    iterador = 0
    aux_x = list()
    aux_y = list()
    while(iterador < len(esquinas)):
        x1,y1 = esquinas[iterador]
        aux_x.append(x1)
        aux_y.append(y1)
        iterador += 1
# saco los puntos máximos y mínimos del marco comun
    _xmax = max(aux_x)
    _ymax = max(aux_y)
    _ymin = min(aux_y)
    _xmin = min(aux_x)

# actualizo los puntos maximos y minimos para el marco comun
    if(_xmax > xmax):
        xmax = _xmax
    if(_ymax > _ymax):
        ymax = _ymax
    if(_xmin < xmin):
        xmin = _xmin
    if(_ymin < ymin):
        ymin = _ymin  
        
    return xmax,ymax,xmin,ymin



pano = [readrgb(x) for x in sorted(glob.glob('./pano/profesor/ejemplo/*.jpg'))]
#pano = [readrgb(x) for x in sorted(glob.glob('./pano/pano*.jpg'))]

matches = sorted([(match(p,q)[0],i,j) for i,p in enumerate(pano) for j,q in enumerate(pano) if i< j],reverse=True)

# esta será la imagen base
base = buscar_base(matches)
# guardo las que usamos y las que no hemos usado aun
usadas = list()
no_usadas = list(range(len(pano)))

# guardo la anchura y altura de la imagen
h,w,_ = pano[base].shape

#    0                1
#  (0,0)            (0,h) 
#   x----------------x
#   |                |
#   |                |
#   |                |
#   |                |
#   x----------------x
#  (w,0)            (w,h)
#    2                3

# los puntos en el espacio de la imagen base
esquinas = ((0,0),(0,h),(w,0),(w,h))
esquina_base = (0,0)  

# los primeros puntos máximos y mínimos de las imagenes
xmax = w
ymax = h
xmin = 0
ymin = 0

# futuro marco comun
Hizq = None
Hder = None
izq = list()
der = list()

# almaceno las homografias para usarlas luego al cambiar la perspectiva
lista_homografias = list()
homografias_der = list()
homografias_izq = list()

# guardo la imagen base para poder usarla 
img_base = pano[base]
# la imagen que juntaré en el futuro
img_otra = None

# al empezar quito la imagen base de las no usadas
no_usadas.remove(base)
usadas.append(base)

iterador = 0
esquinas_aux = None
# compruebo todas las imagenes
while(len(pano) != len(usadas)):
# compruebo los matches
    (_,a,b) = matches[iterador]
# dependiendo de la posición en la que matchee mejor la base con la otra imagen la colocaremos
      
    if(a in usadas and b not in usadas):

        img_otra = pano[b]
        img_aux = pano[a]
        _,H = match(img_aux, img_otra)

        if(Hder is not None):
            Hder = Hder@H
        else:
            Hder = H
        
        der.append(b)
        
        # paso las coordenadas de las esquinas de las imagenes al marco comun
        esquinas_aux = htrans(Hder, esquinas)
        homografias_der.append(Hder)
        # actualizo los valores de las esquinas del marco comun
        xmax,ymax,xmin,ymin = comprobar_esquinas(esquinas_aux,xmax,ymax,xmin,ymin)
        matches.remove(matches[iterador])
        iterador = 0
        usadas.append(b)
        no_usadas.remove(b)
        
    elif(b in usadas and a not in usadas):
        img_otra = pano[a]
        img_aux = pano[b]
        _,H = match(img_aux,img_otra)
        
        if(Hizq is not None):
            Hizq = H@Hizq
        else:
            Hizq = H
        
        izq.append(a)
        
        esquinas_aux = htrans(Hizq, esquinas)
        homografias_izq.append(Hizq)
        xmax,ymax,xmin,ymin = comprobar_esquinas(esquinas_aux,xmax,ymax,xmin,ymin)
        matches.remove(matches[iterador])
        iterador = 0
        usadas.append(a)
        no_usadas.remove(a)
        
    
    else:
        iterador += 1
    
    if(iterador == (len(matches)-1)):
        iterador = 0

# pongo los valores de las esquinas en numeros enteros
xmax = int(xmax)
xmin = int(xmin)
ymax = int(ymax)
ymin = int(ymin)

# calculo el tamaño del marco comun
sz = (xmax-xmin, ymax-ymin)

# calculo el desplazamiento de las imagenes al centro del marco comun para que quepan stitcheadas
despx = esquina_base[0]-xmin
despy = esquina_base[1]-ymin


T = desp((despx, float(despy)))

based = cv.warpPerspective(pano[base],T,sz)
iterator = 1

# voy stitcheando las imagenes a la imagen base
Hfin = None
while(iterator != len(usadas)):
    if(usadas[iterator] in izq):
        Hfin = homografias_izq.pop(0)
    else:
        Hfin = homografias_der.pop(0)
    cv.warpPerspective(pano[usadas[iterator]],T@Hfin,sz,based,0,cv.BORDER_TRANSPARENT)
    iterator += 1
   
fig(10,6)
plt.imshow(based)
plt.show()

















    
