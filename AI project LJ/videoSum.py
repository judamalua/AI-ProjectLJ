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

def aplicaKmedias(ListaFrames, K, H, INPUTPATH):
    ListaFramesConClasificacion = dict()
    
    centrosIniciales = calcularCentrosIniciales(INPUTPATH, H, K)
    #print(centroidesIniciales)

    clavesMinimas = list()
    valoresMinimos = list()


    for keyCentro in centrosIniciales.keys():
        ListaFramesConClasificacion[keyCentro] = list()

    index = 0
    for frame, keyFrame in zip(ListaFrames.values(), ListaFrames.keys()):
        nombreCentro = ""
        indexCentros = 0
        #print(frame)
        
        #print("==============================================")
        distanciaMinima = math.inf
        for centroInicial, keyCentro in zip(centrosIniciales.values(), centrosIniciales.keys()):
            # Declaramos una variable para almacenar la distancia total de cada imagen a cada centro
            distTotal = 0
            # Declaramos tres variables para ir acumulando las distancias de cada canal de las imágenes
            distB, distG, distR = 0, 0, 0
            # Declaramos los índices para cada canal
            indiceB, indiceG, indiceR = 0, 0, 0

            # Para cada frame del canal 'b' calculamos la distancia con cada centro
            for iB in frame["b"]:
                distB += math.pow(int(iB) - int(centroInicial["b"][indiceB]), 2)
                indiceB += 1
            
            distBSqrt = math.sqrt(float(distB))

            # Para cada frame del canal 'g' calculamos la distancia con cada centro
            for iG in frame["g"]:
                distG += math.pow(int(iG) - int(centroInicial["g"][indiceG]), 2)
                indiceG += 1
            distGSqrt = math.sqrt(float(distG))

            # Para cada frame del canal 'r' calculamos la distancia con cada centro
            for iR in frame["r"]:
                distR += math.pow(int(iR) - int(centroInicial["r"][indiceR]), 2)
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
    print("==============================================================")
    #print(ListaFramesConClasificacion)

    jaja = actualizaCentros(ListaFrames, ListaFramesConClasificacion, centrosIniciales)
    
    
        
def actualizaCentros(dictNombreFramesHistograma, dictNombreCentroNombreFrame, dictCentrosHistr):
    index = 0
    dictCentrosHistrActualizado = dict()
    histrCentroActualizado = dict()
    title = "Centro actualizado {}".format(index)
    title2 = "Centro No actualizado {}".format(index)
    
    for nombreCentro, histrCentro in dictCentrosHistr.items():
        
        if len(dictNombreCentroNombreFrame[nombreCentro]) == 0:
            dictCentrosHistrActualizado[title2] = histrCentro
        else:

            #listOfListsB = []
            #listOfListsG = []
            #listOfListsR = []
            #for nombreFrame, histr in dictNombreFramesHistograma.items():
            
            #sumaB = [sum(x)/3 for x in zip(*listOfListsB)]
            #sumaG = [sum(y)/3 for y in zip(*listOfListsG)]
            #sumaR = [sum(z)/3 for z in zip(*listOfListsR)]

            nombresFrames = dictNombreCentroNombreFrame[nombreCentro]
            #print(nombresFrames)
            #print("======================================================")
            #print(dictNombreFramesHistograma[ola]["b"])
            acumTotal = dict()
            acumTotal["b"] = []
            acumTotal["g"] = []
            acumTotal["r"] = []
            
            for nombre in nombresFrames:
                acumB= list()
                acumG= list()
                acumR= list()
                acumB = dictNombreFramesHistograma[nombre]["b"]
                acumG = dictNombreFramesHistograma[nombre]["g"]
                acumR = dictNombreFramesHistograma[nombre]["r"]
                indexPositionB = 0
                indexPositionG = 0
                indexPositionR = 0
                for iB in acumTotal["b"]:
                    acumTotal["b"][iB]= iB + acumB[indexPositionB]/len(nombresFrames)
                    indexPositionB += 1
                for iG in acumTotal["g"]:
                    acumTotal["g"][iG]= iG + acumG[indexPositionG]/len(nombresFrames)
                    indexPositionG += 1
                for iR in acumTotal["r"]:
                    acumTotal["r"][iR]= iR = acumR[indexPositionR]/len(nombresFrames)
                    indexPositionR += 1

        
            #acumTotal["b"] /=len(nombresFrames)
            #acumTotal["g"] /=len(nombresFrames)
            #acumTotal["r"] /=len(nombresFrames)
            
            dictCentrosHistrActualizado[title] = acumTotal
            print(dictCentrosHistrActualizado)

            #histrCentroActualizado["b"] = np.sum(dictNombreFramesHistograma[dictNombreCentroNombreFrame[nombreCentro]]["b"])#/len(dictCentroNombreFrame[nombreCentro])
            #histrCentroActualizado["g"] = np.sum(dictNombreFramesHistograma[dictNombreCentroNombreFrame[nombreCentro]]["g"])#/len(dictCentroNombreFrame[nombreCentro])
            #histrCentroActualizado["r"] = np.sum(dictNombreFramesHistograma[dictNombreCentroNombreFrame[nombreCentro]]["r"])#/len(dictCentroNombreFrame[nombreCentro])
            #print(histrCentroActualizado)
               #dictCentrosHistrActualizado[title]["b"] +=
        index += 1
    
    

    return 0





def CalcularFotogramasClave(INPUTPATH, T, K, H):
    ListaFrames = dict()
    if __name__ == '__main__':
        ListaFrames = recorre_imagenes(INPUTPATH, T, H)
        #print(ListaFrames)
    
    aplicaKmedias(ListaFrames, K, H, INPUTPATH)


CalcularFotogramasClave("C:\\Users\\Juanmi\\Desktop\\Pictures AI project",5,5,180)
#CalcularFotogramasClave("C:\\Users\\Juanmi\\Desktop\\video manu",10,20,256)
#aplicaKmedias(list(), 3, 256)
#listaPrueba = calcularCentrosIniciales(256, 3)