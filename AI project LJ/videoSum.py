import os
import cv2
from matplotlib import pyplot as plt
import numpy as np
from random import randint
import math

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

            print(input_path)

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

def aplicaKmedias(ListaFrames, K, H, N, INPUTPATH):
    
    primeraIteracion = True
    

    for n in range(0, N):
        print("Iteración: {}".format(n + 1))

        if primeraIteracion == True:
            centrosAlgoritmo = calcularCentrosIniciales(INPUTPATH, H, K)
            ListaFramesConClasificacion = dict()
            primeraIteracion = False
        else:
            centrosAlgoritmoAnteriores = centrosAlgoritmo
            centrosAlgoritmo = actualizaCentros(ListaFrames, ListaFramesConClasificacion, centrosAlgoritmo)
            
            if centrosAlgoritmo.values() == centrosAlgoritmoAnteriores.values():
                break

            ListaFramesConClasificacion = dict()
            

        clavesMinimas = list()
        valoresMinimos = list()


        for keyCentro in centrosAlgoritmo.keys():
            ListaFramesConClasificacion[keyCentro] = list()

        index = 0
        for frame, keyFrame in zip(ListaFrames.values(), ListaFrames.keys()):
            nombreCentro = ""
            indexCentros = 0
            #print(frame)
        
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

                distTotal = (distBSqrt + distGSqrt + distRSqrt)/3

                #print(distTotal)

                if indexCentros == 0:
                    clavesMinimas.append(keyFrame)
                    valoresMinimos.append(keyCentro)

                if distTotal < distanciaMinima:
                    distanciaMinima = distTotal
                    del valoresMinimos[index]
                    valoresMinimos.insert(index, keyCentro)
                    nombreCentro = keyCentro

            
                indexCentros += 1


            index += 1

            
            ListaFramesConClasificacion[nombreCentro].append(keyFrame)
            #print(minimum)
    

    
        #print(minimumTotal)
        #print(clavesMinimas)
        #print(valoresMinimos)
        #print("==============================================================")
        #print(ListaFramesConClasificacion)

        #print(centrosIniciales)
        #print("==============================================================")
        #centrosAlgoritmo = actualizaCentros(ListaFrames, ListaFramesConClasificacion, centrosAlgoritmo)
        #print(centrosAlgoritmo)
        print(ListaFramesConClasificacion)
    listaKeyFrames = calculaCentroidesClases(ListaFrames, ListaFramesConClasificacion, centrosAlgoritmo)
    #print(listaKeyFrames)
    
def calculaCentroidesClases(dictNombreFramesHistograma, dictNombreCentroNombreFrames, dictCentrosHistr):
    listaKeyFrames = list() 

    for nombreCentro in dictNombreCentroNombreFrames.keys():
        for nombreFrame in dictNombreCentroNombreFrames[nombreCentro]:
            index = 0
            for nombreFrameDentro, histrFrame in dictNombreFramesHistograma.items():
                if nombreFrame == nombreFrameDentro:
                    indexCentros = 0
                    distMinima = math.inf
                    for centroHistr, nombreCentroDentro in zip(dictCentrosHistr.values(), dictCentrosHistr.keys()):
                        if nombreCentro == nombreCentroDentro:
                            # Declaramos una variable para almacenar la distancia total de cada imagen a cada centro
                            distTotal = 0
                            # Declaramos tres variables para ir acumulando las distancias de cada canal de las imágenes
                            distB, distG, distR = 0, 0, 0
                            # Declaramos los índices para cada canal
                            indiceB, indiceG, indiceR = 0, 0, 0

                            # Para cada frame del canal 'b' calculamos la distancia con cada centro
                            for iB in histrFrame["b"]:
                                distB += math.pow(int(iB) - int(centroHistr["b"][indiceB]), 2)
                                indiceB += 1
            
                            distBSqrt = math.sqrt(float(distB))

                            # Para cada frame del canal 'g' calculamos la distancia con cada centro
                            for iG in histrFrame["g"]:
                                distG += math.pow(int(iG) - int(centroHistr["g"][indiceG]), 2)
                                indiceG += 1
                            distGSqrt = math.sqrt(float(distG))

                            # Para cada frame del canal 'r' calculamos la distancia con cada centro
                            for iR in histrFrame["r"]:
                                distR += math.pow(int(iR) - int(centroHistr["r"][indiceR]), 2)
                                indiceR += 1
                            distRSqrt = math.sqrt(float(distR))

                            distTotal = (distBSqrt + distGSqrt + distRSqrt)/3

                            if indexCentros == 0:
                                listaKeyFrames.append(nombreFrame)

                            if distTotal < distMinima:
                                distMinima = distTotal
                                del listaKeyFrames[index]
                                listaKeyFrames.insert(index, nombreFrame)
                    
                            indexCentros += 1
                    index += 1

    return listaKeyFrames



        
def actualizaCentros(dictNombreFramesHistograma, dictNombreCentroNombreFrames, dictCentrosHistr):
    index = 0
    dictCentrosHistrActualizado = dict()
    
    
    for nombreCentro, histrCentro in dictCentrosHistr.items():
        histrSuma = dict()
        #acum = {"b": [0]*longitudHistr, "g": [0]*longitudHistr, "r": [0]*longitudHistr}
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








            
            #for nombreCentroDentro in dictNombreCentroNombreFrames.keys():
            
                #indiceB, indiceG, indiceR = 0, 0, 0


                #if nombreCentroDentro == nombreCentro:

                    #for nombreFrameDentro, histogramaFrame in dictNombreFramesHistograma.items():
                    #if nombreCentroDentro == nombreCentro:
                        #print(nombreCentroDentro + ", " + nombreCentro)
                        #for iB in histogramaFrame["b"]:
                            #if indiceB < longitudHistr:
                                #acum["b"][indiceB] += int(iB)/len(dictNombreCentroNombreFrames[nombreCentro])
                                #indiceB += 1
                        #for iG in histogramaFrame["g"]:
                            #if indiceG < longitudHistr:
                                #acum["g"][indiceG] += int(iG)/len(dictNombreCentroNombreFrames[nombreCentro])
                                #indiceG += 1
                        #for iR in histogramaFrame["r"]:
                            #if indiceR < longitudHistr:
                                #acum["r"][indiceR] += int(iR)/len(dictNombreCentroNombreFrames[nombreCentro])
                                #indiceR += 1

                    #dictCentrosHistrActualizado[title] = acum

        index += 1
    
    return dictCentrosHistrActualizado





def CalcularFotogramasClave(INPUTPATH, T, K, H, N):
    ListaFrames = dict()
    if __name__ == '__main__':
        ListaFrames = recorre_imagenes(INPUTPATH, T, H)
        #print(ListaFrames)
    
    aplicaKmedias(ListaFrames, K, H, N, INPUTPATH)


CalcularFotogramasClave("C:\\Users\\Juanmi\\Desktop\\Pictures AI project", 15, 5, 256, 4)
#CalcularFotogramasClave("C:\\Users\\Juanmi\\Desktop\\video manu",10,20,256)
#aplicaKmedias(list(), 3, 256)
#listaPrueba = calcularCentrosIniciales(256, 3)