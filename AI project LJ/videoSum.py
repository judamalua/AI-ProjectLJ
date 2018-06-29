import os
import cv2
from matplotlib import pyplot as plt
import numpy as np
from random import randint
import math

# T: Indica el número de fotogramas a saltar
# K: Indica el número de centros a generar
# H: Indica el tamaño del histograma generado para cada canal
# N: Indica el número de iteraciones a ejecutar por el algoritmo si los centros siguen cambiando
def CalcularFotogramasClave(INPUTPATH, T, K, H, N, OUTPUTPATH):
    ListaFrames = dict()
    if __name__ == '__main__':
        ListaFrames = recorre_imagenes(INPUTPATH, T, H)

    aplicaKmedias(ListaFrames, K, H, N, INPUTPATH, OUTPUTPATH)


def recorre_imagenes(INPUTPATH, T, H):
    path = INPUTPATH
    index = T
    ListaFrames = dict()

    for image in os.listdir(path):
        # Si el índice no coincide con T le añadimos 1
        if index != T:
            index += 1

        # Si coincide, entonces ponemos el índice a 1
        elif index == T:
            index = 1

            # Formamos el input path de la imagen
            input_path = os.path.join(path, image)

            #print(input_path)

            # Leemos la imagen que se corresponde con el input path
            img = cv2.cv2.imread(input_path)

            #cv2.cv2.imshow('image', img)

            color = ('b', 'g', 'r')
            histr = dict()

            # Calculamos el histograma
            for i,col in enumerate(color):
                histr[col] = cv2.cv2.calcHist([img], [i], None, [H], [0,H])
                #print(histr)
                #plt.plot(histr[col], color = col)
                #plt.xlim([0,H])
            
            # Añadimos el histograma a un diccionario {nombre del frame -> histograma}
            ListaFrames[input_path] = histr
        
            #plt.show()

    #print(ListaFrames)
    return ListaFrames

def escribirImagenes(INPUTPATH, OUTPUTPATH, listaKeyFrames):
    path = INPUTPATH
    nombreImagenAImprimir = ""

    # Si ya hay imágenes en la ruta de salida las eliminamos
    if len(os.listdir(OUTPUTPATH)) != 0:
        for imagenParaBorrar in os.listdir(OUTPUTPATH):
            deletePath = os.path.join(OUTPUTPATH, imagenParaBorrar)
            os.remove(deletePath)

    for image in os.listdir(path):
        # Recorremos las imágenes del directorio y obtenemos sus nombres
        input_path = os.path.join(path, image)

        for nombreFrame in listaKeyFrames:
            # Si el nombre de la imagen que estamos tratando ahora mismo coincide con el nombre de una de las
            # imágenes en la lista de key frames
            if input_path == nombreFrame:
                # Tomamos el nombre de la imagen
                nombreImagenAImprimir = nombreFrame.split("\\")[-1] # Toma el último valor de la lista

                # Leemos la imagen
                img = cv2.cv2.imread(input_path)

                # Y finalmente la escribimos con el mismo nombre que tenía en la ruta indicada en OUTPUTPATH
                cv2.cv2.imwrite(OUTPUTPATH + "/" + nombreImagenAImprimir, img)

    print("=================================================================================================")
    print("Resumen finalizado, el resultado se almacenó en \"{}\"".format(OUTPUTPATH))
    print("=================================================================================================")

def calcularCentrosIniciales(INPUTPATH, H, K):
    ListaCentros = dict()
    path = INPUTPATH
    ListaFramesTotales = dict()
    color = ('b', 'g', 'r')

    # Para calcular los centros iniciales primero recorremos todas las imágenes y almacenamos sus historamas
    # en ListaFramesTotales
    for image in os.listdir(path):
        input_path = os.path.join(path, image)

        #print(input_path)

        img = cv2.cv2.imread(input_path)

        #cv2.cv2.imshow('image', img)

        histr = dict()

        for i,col in enumerate(color):
            histr[col] = cv2.cv2.calcHist([img], [i], None, [H], [0,H])
            #print(histr)
            #plt.plot(histr[col], color = col)
            #plt.xlim([0,H])
            
        #plt.show()

        ListaFramesTotales[input_path] = histr
        
            
    # Para cada centro que se quiera generar
    for index in range(K):
        histr1 = dict()
        histr2 = dict()
        histrSuma = dict()
        aleatorio1 = randint(0, len(ListaFramesTotales.values()) - 1)
        aleatorio2 = randint(0, len(ListaFramesTotales.values()) - 1)
        aleatorio3 = randint(0, len(ListaFramesTotales.values()) - 1)
    
        sumaB = 0
        sumaG = 0
        sumaR = 0

        # Tomamos 3 histogramas aleatorios de la lista de frames totales
        title = "Centro aleatorio {}".format(index)
        histr1 = list(ListaFramesTotales.values())[aleatorio1]
        histr2 = list(ListaFramesTotales.values())[aleatorio2]
        histr3 = list(ListaFramesTotales.values())[aleatorio3]

        # Almacenamos cada canal en una lista de listas
        listOfListsB = [histr1["b"], histr2["b"], histr3["b"]]
        listOfListsG = [histr1["g"], histr2["g"], histr3["g"]]
        listOfListsR = [histr1["r"], histr2["r"], histr3["r"]]

        # Sumamos los valores de cada canal y lo dividimos entre 3 (Número de histogramas sumados)
        sumaB = [sum(x)/3 for x in zip(*listOfListsB)]
        sumaG = [sum(y)/3 for y in zip(*listOfListsG)]
        sumaR = [sum(z)/3 for z in zip(*listOfListsR)]
        
        # Los almacenamos en un nuevo histograma que será uno de los centros iniciales
        histrSuma["b"] = sumaB
        histrSuma["g"] = sumaG
        histrSuma["r"] = sumaR

        # Finalmente añadimos el histograma a la lista de centros
        ListaCentros[title] = histrSuma

    return ListaCentros

def aplicaKmedias(ListaFrames, K, H, N, INPUTPATH, OUTPUTPATH):
    primerCalculoCentros = True # Declaramos una variable que nos servirá para calcular los centros de manera aleatoria en la primera iteración
    

    for n in range(0, N):
        #print("Iteración: {}".format(n + 1))

        ListaFramesConClasificacion = dict()

        # Si es la primera vez que se calculan los centros los generamos con el método calcularCentrosIniciales
        if primerCalculoCentros == True:
            centrosAlgoritmo = calcularCentrosIniciales(INPUTPATH, H, K)

            # Ponemos esta variable a False para que no se vuelva a entrar en este bloque condicional
            primerCalculoCentros = False
    
        # Creamos una lista vacía para cada centro
        for keyCentro in centrosAlgoritmo.keys():
            ListaFramesConClasificacion[keyCentro] = list()

        for frame, keyFrame in zip(ListaFrames.values(), ListaFrames.keys()):
            nombreCentro = ""
        
            distanciaMinima = math.inf
            for centroHistr, keyCentro in zip(centrosAlgoritmo.values(), centrosAlgoritmo.keys()):
                # Declaramos una variable para almacenar la distancia total de cada imagen a cada centro
                distTotal = 0
                # Declaramos tres variables para ir acumulando las distancias de cada canal de las imágenes
                distB, distG, distR = 0, 0, 0
                # Declaramos los índices para cada canal
                indiceB, indiceG, indiceR = 0, 0, 0

                # Para cada frame del canal 'b' calculamos la distancia con cada centro
                for iB in frame["b"]:
                    distB += math.pow(int(iB) - int(centroHistr["b"][indiceB]), 2)
                    indiceB += 1
            
                distBSqrt = math.sqrt(float(distB))

                # Para cada frame del canal 'g' calculamos la distancia con cada centro
                for iG in frame["g"]:
                    distG += math.pow(int(iG) - int(centroHistr["g"][indiceG]), 2)
                    indiceG += 1
                distGSqrt = math.sqrt(float(distG))

                # Para cada frame del canal 'r' calculamos la distancia con cada centro
                for iR in frame["r"]:
                    distR += math.pow(int(iR) - int(centroHistr["r"][indiceR]), 2)
                    indiceR += 1
                distRSqrt = math.sqrt(float(distR))

                # Para calcular la distancia total, sumamos las distancias de cada canal y dividimos entre 3 (número de canales)
                distTotal = (distBSqrt + distGSqrt + distRSqrt)/3


                # Si la distancia total es menor que la distancia mínima actual, esta distancia total será
                # la nueva distancia mínima
                if distTotal < distanciaMinima:
                    distanciaMinima = distTotal

                    # El nuevo centro con distancia mínima es el centro cuya distancia ha cumplido esta condición
                    nombreCentro = keyCentro

            # Añadimos a la lista de frames mas cercanos al centro "nombreCentro" el frame que estamos tratando
            ListaFramesConClasificacion[nombreCentro].append(keyFrame)
    
    
        # Estas líneas nos permiten ver los cambios de los centros en cada iteración, 
        # descomentar para comprobar, dejar comentado en otro caso
        #indicePrueba = 0
        #for prueba in ListaFramesConClasificacion.values():
            #print("Longitud centro {}: {}".format(indicePrueba, len(prueba)))
            #indicePrueba += 1
        
        # Calculamos los nuevos centros y guardamos los anteriores para comprobar si son iguales
        centrosAlgoritmoAnteriores = centrosAlgoritmo
        centrosAlgoritmo = actualizaCentros(ListaFrames, ListaFramesConClasificacion, centrosAlgoritmo)
        
        # Comprobamos si los centros calculados y los anteriores son iguales histograma a histograma
        centrosSonIguales = True
        for centroActual, centroAnterior in zip(centrosAlgoritmo.values(), centrosAlgoritmoAnteriores.values()):
            if centroActual != centroAnterior:
                centrosSonIguales = False
                break

        # Si los centros son iguales dejamos de iterar
        if centrosSonIguales == True:
            break

    listaKeyFrames = calculaCentroidesClases(ListaFrames, ListaFramesConClasificacion, centrosAlgoritmo)
    #print("Frames resumidos: {}".format(len(listaKeyFrames)))
    #print(listaKeyFrames)

    escribirImagenes(INPUTPATH, OUTPUTPATH, listaKeyFrames)
    
def calculaCentroidesClases(dictNombreFramesHistograma, dictNombreCentroNombreFrames, dictCentrosHistr):
    listaKeyFrames = list() # Declaramos la lista a devolver
    nombreFrameDistMinima = ""  # Declaramos una variable para almacenar el nombre del frame con la distancia mínima a su centro

    # Iteramos los nombres de los centros
    for nombreCentro in dictNombreCentroNombreFrames.keys():
        # Iteramos los nombres de los centros y sus histogramas
        for nombreCentroDentro, histrCentro in dictCentrosHistr.items():
            # Si el nombre del centro del segundo bucle es igual al del primero tomamos sus frames asociados
            # y calculamos el que tiene menor distancia
            if nombreCentro == nombreCentroDentro:
                distMinima = math.inf   # Declaramos una variable para almacenar la distancia mínima

                # Comprobamos que el centro en cuestión tiene frames asociados
                if len(dictNombreCentroNombreFrames[nombreCentroDentro]) != 0:
                    # Para cada uno de los frames asociados al nombre del centro anteriormente
                    # calculado obtenemos la distancia y nos quedamos con la mínima
                    for nombreFrame in dictNombreCentroNombreFrames[nombreCentroDentro]:
                        # Tomamos el histograma del frame que estamos tratando actualmente
                        histrFrame = dictNombreFramesHistograma[nombreFrame]

                        # Declaramos una variable para almacenar la distancia total de cada imagen a cada centro
                        distTotal = 0

                        # Declaramos tres variables para ir acumulando las distancias de cada canal de las imágenes
                        distB, distG, distR = 0, 0, 0

                        # Declaramos los índices para cada canal
                        indiceB, indiceG, indiceR = 0, 0, 0

                        # Para cada frame del canal 'b' calculamos la distancia con cada centro
                        for iB in histrFrame["b"]:
                            distB += math.pow(int(iB) - int(histrCentro["b"][indiceB]), 2)
                            indiceB += 1
            
                        distBSqrt = math.sqrt(float(distB))

                        # Para cada frame del canal 'g' calculamos la distancia con cada centro
                        for iG in histrFrame["g"]:
                            distG += math.pow(int(iG) - int(histrCentro["g"][indiceG]), 2)
                            indiceG += 1
                        distGSqrt = math.sqrt(float(distG))

                        # Para cada frame del canal 'r' calculamos la distancia con cada centro
                        for iR in histrFrame["r"]:
                            distR += math.pow(int(iR) - int(histrCentro["r"][indiceR]), 2)
                            indiceR += 1
                        distRSqrt = math.sqrt(float(distR))

                        # Calculamos la distancia total
                        distTotal = (distBSqrt + distGSqrt + distRSqrt)/3

                        # Si la distancia del frame al centro es menor que la distancia mínima
                        if distTotal < distMinima:
                            distMinima = distTotal # Actualizamos la distancia mínima
                            nombreFrameDistMinima = nombreFrame # Tomamos el frame actual como el frame con menor distancia al centro

                    # Tras terminar todas las iteraciones añadimos el frame con menor distancia a listaKeyFrames
                    listaKeyFrames.append(nombreFrameDistMinima)

    return listaKeyFrames



        
def actualizaCentros(dictNombreFramesHistograma, dictNombreCentroNombreFrames, dictCentrosHistr):
    index = 0
    dictCentrosHistrActualizado = dict()
    
    # Iteramos sobre los nombres de los centros y sus histogramas
    for nombreCentro, histrCentro in dictCentrosHistr.items():
        histrSuma = dict()
        title = "Centro actualizado {}".format(index)
        
        # Si el centro no tiene ningún frame asociado, entonces se queda tal cual estaba
        if len(dictNombreCentroNombreFrames[nombreCentro]) == 0:
            dictCentrosHistrActualizado[title] = histrCentro
        else:
            listOfListsB = []
            listOfListsG = []
            listOfListsR = []

            # Si el centro tenía frames asociados, iteramos sobre los nombres de los centros
            for nombreCentroDentro in dictNombreCentroNombreFrames.keys():

                #Si estamos tratando el mismo centro
                if nombreCentro == nombreCentroDentro:

                    # Iteramos sobre los frames asociados a ese centro
                    for frameNombre in dictNombreCentroNombreFrames[nombreCentro]:

                        # Iteramos sobre los nombres de los frames
                        for frameNombreDentro, histogramaFrame in dictNombreFramesHistograma.items():

                            # Si estamos tratando el mismo frame
                            if frameNombre == frameNombreDentro:
                                # Añadimos sus canales a la lista de listas de cada canal
                                listOfListsB.append(histogramaFrame["b"])
                                listOfListsG.append(histogramaFrame["g"])
                                listOfListsR.append(histogramaFrame["r"])
            
            # Hacemos la suma de cada lista de listas dividiendo entre el número de frames asociados 
            # al centro que estamos tratando en este momento
            sumaB = [sum(x)/len(dictNombreCentroNombreFrames[nombreCentro]) for x in zip(*listOfListsB)]
            sumaG = [sum(y)/len(dictNombreCentroNombreFrames[nombreCentro]) for y in zip(*listOfListsG)]
            sumaR = [sum(z)/len(dictNombreCentroNombreFrames[nombreCentro]) for z in zip(*listOfListsR)]

            # Guardamos las sumas en un histograma
            histrSuma["b"] = sumaB
            histrSuma["g"] = sumaG
            histrSuma["r"] = sumaR
            
            # Y almacenamos el centro actualizado con su nuevo histograma
            dictCentrosHistrActualizado[title] = histrSuma

        # Aumentamos el índice que nos sirve para poner los nombres a los centros
        index += 1
    
    # Y finalmente devolvemos los centros actualizados
    return dictCentrosHistrActualizado


CalcularFotogramasClave("C:\\Users\\Juanmi\\Desktop\\Pictures AI project", 2, 15, 255, 30, "C:\\Users\\Juanmi\\Dropbox\\Carpeta trabajos tercero\\Resultados IA jl\\Resultados")