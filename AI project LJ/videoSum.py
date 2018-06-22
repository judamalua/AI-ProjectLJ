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
        if index != T:
            index += 1
        elif index == T:
            index = 1
            input_path = os.path.join(path, image)

            #print(input_path)

            img = cv2.cv2.imread(input_path)

            #cv2.cv2.imshow('image', img)

            color = ('b', 'g', 'r')
            histr = dict()

            for i,col in enumerate(color):
                histr[col] = cv2.cv2.calcHist([img], [i], None, [H], [0,H])
                #print(histr)
                #plt.plot(histr[col], color = col)
                #plt.xlim([0,H])
            
            ListaFrames[input_path] = histr
        
            #plt.show()

    #print(ListaFrames)
    return ListaFrames

def escribirImagenes(INPUTPATH, OUTPUTPATH, listaKeyFrames):
    path = INPUTPATH
    nombreImagenAImprimir = ""

    if len(os.listdir(OUTPUTPATH)) != 0:
        for imagenParaBorrar in os.listdir(OUTPUTPATH):
            deletePath = os.path.join(OUTPUTPATH, imagenParaBorrar)
            os.remove(deletePath)

    for image in os.listdir(path):
        input_path = os.path.join(path, image)

        for nombreFrame in listaKeyFrames:
            if input_path == nombreFrame:
                nombreImagenAImprimir = nombreFrame.split("\\")[-1]
                img = cv2.cv2.imread(input_path)
                cv2.cv2.imwrite(OUTPUTPATH + "/" + nombreImagenAImprimir, img)

    print("=================================================================================================")
    print("Resumen finalizado, el resultado se almacenó en \"{}\"".format(OUTPUTPATH))
    print("=================================================================================================")

def calcularCentrosIniciales(INPUTPATH, H, K):
    ListaCentros = dict()
    path = INPUTPATH
    ListaFramesTotales = dict()
    color = ('b', 'g', 'r')

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

        title = "Centro aleatorio {}".format(index)
        histr1 = list(ListaFramesTotales.values())[aleatorio1]
        histr2 = list(ListaFramesTotales.values())[aleatorio2]
        histr3 = list(ListaFramesTotales.values())[aleatorio3]

        listOfListsB = [histr1["b"], histr2["b"], histr3["b"]]
        listOfListsG = [histr1["g"], histr2["g"], histr3["g"]]
        listOfListsR = [histr1["r"], histr2["r"], histr3["r"]]

        sumaB = [sum(x)/3 for x in zip(*listOfListsB)]
        sumaG = [sum(y)/3 for y in zip(*listOfListsG)]
        sumaR = [sum(z)/3 for z in zip(*listOfListsR)]
        
        histrSuma["b"] = sumaB
        histrSuma["g"] = sumaG
        histrSuma["r"] = sumaR

        ##ListaCentros[title] = histr1

        ListaCentros[title] = histrSuma

        ##for k,colR in enumerate(color):
            #histr[colR] = cv2.cv2.calcHist([randImg], [k], None, [H], [0,H])
            ##print(histrSuma)
            ##plt.plot(histrSuma[colR], color = colR)
            ##plt.xlim([0,H])
        
        #ListaCentroides[title] = histr
    
        ##plt.show()

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
    
        # Creamos una lista vacía para cada 
        for keyCentro in centrosAlgoritmo.keys():
            ListaFramesConClasificacion[keyCentro] = list()

        for frame, keyFrame in zip(ListaFrames.values(), ListaFrames.keys()):
            nombreCentro = ""
        
            #print("==============================================")
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

                #print(distTotal)

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

        #print("==============================================================")
        #centrosAlgoritmo = actualizaCentros(ListaFrames, ListaFramesConClasificacion, centrosAlgoritmo)
        #print(centrosAlgoritmo)
        #print(ListaFramesConClasificacion)

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

                    # Tras todas las iteraciones añadimos el frame con menor distancia a listaKeyFrames
                    listaKeyFrames.append(nombreFrameDistMinima)

    return listaKeyFrames



        
def actualizaCentros(dictNombreFramesHistograma, dictNombreCentroNombreFrames, dictCentrosHistr):
    index = 0
    dictCentrosHistrActualizado = dict()
    
    
    for nombreCentro, histrCentro in dictCentrosHistr.items():
        histrSuma = dict()
        title = "Centro actualizado {}".format(index)
        
        if len(dictNombreCentroNombreFrames[nombreCentro]) == 0:
            dictCentrosHistrActualizado[title] = histrCentro
        else:
            listOfListsB = []
            listOfListsG = []
            listOfListsR = []

            for nombreCentroDentro in dictNombreCentroNombreFrames.keys():
                if nombreCentro == nombreCentroDentro:
                    for frameNombre in dictNombreCentroNombreFrames[nombreCentro]:
                        for frameNombreDentro, histogramaFrame in dictNombreFramesHistograma.items():
                            if frameNombre == frameNombreDentro:
                                listOfListsB.append(histogramaFrame["b"])
                                listOfListsG.append(histogramaFrame["g"])
                                listOfListsR.append(histogramaFrame["r"])
            
            sumaB = [sum(x)/len(dictNombreCentroNombreFrames[nombreCentro]) for x in zip(*listOfListsB)]
            sumaG = [sum(y)/len(dictNombreCentroNombreFrames[nombreCentro]) for y in zip(*listOfListsG)]
            sumaR = [sum(z)/len(dictNombreCentroNombreFrames[nombreCentro]) for z in zip(*listOfListsR)]

            histrSuma["b"] = sumaB
            histrSuma["g"] = sumaG
            histrSuma["r"] = sumaR
            
            dictCentrosHistrActualizado[title] = histrSuma

        index += 1
    
    return dictCentrosHistrActualizado


CalcularFotogramasClave("C:\\Users\\Juanmi\\Desktop\\Pictures AI project", 2, 20, 256, 15, "C:\\Users\\Juanmi\\Desktop\\Resultado IA")
#CalcularFotogramasClave("C:\\Users\\Juanmi\\Desktop\\video manu",10,20,256, 15, "C:\\Users\\Juanmi\\Desktop\\Resultado IA")
