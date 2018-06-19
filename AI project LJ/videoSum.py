import os
import cv2
from matplotlib import pyplot as plt
import numpy as np
from random import randint
from PIL import Image
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
    ListaCentroides = dict()
    path = INPUTPATH

    for image in os.listdir(path):
        input_path = os.path.join(path, image)

        #print(input_path)

        img = cv2.cv2.imread(input_path)
        imgSize = len(img)
        break


    # Creamos una imagen negra
    imgN = np.zeros([imgSize,imgSize,3], dtype=np.uint8)

    # Creamos una imagen blanca
    imgB = np.zeros([imgSize,imgSize,3], dtype=np.uint8)
    imgB.fill(255)

    #dataN[256, 256] = [255, 0, 0]
    # Con la librería Image pasamos los datos de la matriz a imagen
    #imgN = Image.fromarray(dataN, 'RGB')
    #imgN.show()

    color = ('b', 'g', 'r')
    #histr = dict()

    #for i,col in enumerate(color):
        #histr[col] = cv2.cv2.calcHist([imgN], [i], None, [H], [0,H])
        #print(histr)
        #plt.plot(histr[col], color = col)
        #plt.xlim([0,H])
    
    #ListaCentroides["Centroide negro"] = histr
    
    #plt.show()

    #histr = dict()

    #for j,colB in enumerate(color):
        #histr[colB] = cv2.cv2.calcHist([imgB], [j], None, [H], [0,H])
        #print(histr)
        #plt.plot(histr[colB], color = colB)
        #plt.xlim([0,H])
    
    #ListaCentroides["Centroide blanco"] = histr
    
    #plt.show()


    for index in range(K):
        red, green, blue = (randint(0,255), randint(0,255), randint(0,255)), (randint(0,255), randint(0,255), randint(0,255)), (randint(0,255), randint(0,255), randint(0,255))
        rgb = [red, green, blue]
        title = "Centroide aleatorio {}".format(index)

        # Creamos una imagen aleatoria
        randImg = np.zeros([imgSize,imgSize,3], dtype=np.uint8)
        #randImg.fill(randint(0,255))

        #for x in range(512):
            #for y in range(512):
                #randImg[x][y] = randint(0,255)

        #randImg = np.random.rand(512, 512, 3)
        for x in range(imgSize):
            for y in range(imgSize):
                randImg[x][y] = rgb[randint(0,2)]

    
    
        cv2.cv2.imshow('image', randImg)

        histr = dict()

        for k,colR in enumerate(color):
            histr[colR] = cv2.cv2.calcHist([randImg], [k], None, [H], [0,H])
            #print(histr)
            plt.plot(histr[colR], color = colR)
            plt.xlim([0,H])
        
        ListaCentroides[title] = histr
    
        plt.show()

    return ListaCentroides



def aplicaKmedias(ListaFrames, K, H, INPUTPATH):
    ListaFramesConClasificacion = dict()
    distKeyFrameDict = dict()
    centroidAllFramesDict = dict()
    centroidesFrames = dict()
    minimumTotal = 0
    
    centroidesIniciales = calcularCentrosIniciales(INPUTPATH, H, K)
    #print(centroidesIniciales)

    clavesMinimas = list()#[1]*len(ListaFrames.keys())
    valoresMinimos = list()#[1]*len(ListaFrames.keys())

   # for frame in ListaFrames.values():
       # for i in frame["r"]:
          #  print(int(i))


    #for centroide in centroidesIniciales.values():
        #for i in centroide["r"]:
            #print(int(i))

    numCentroide = 0
    index = 0
    for frame, keyFrame in zip(ListaFrames.values(), ListaFrames.keys()):
        minimum = 0
        
        indexCentros = 0
        
        
        distanciaMinima = math.inf
        for centroideInicial, keyCentroide in zip(centroidesIniciales.values(), centroidesIniciales.keys()):
            distTotal = 0
            for iB in frame["b"]:
                distB = 0
                for jB in centroideInicial["b"]:
                    distB += (int(iB)-int(jB))*(int(iB)-int(jB))
            distB = math.sqrt(float(distB))
            for iG in frame["g"]:
                distG = 0
                for jG in centroideInicial["g"]:
                    distG += (int(iG)-int(jG))*(int(iG)-int(jG))
            distG = math.sqrt(float(distG))
            for iR in frame["r"]:
                distR = 0
                for jR in centroideInicial["r"]:
                    distR += (int(iR)-int(jR))*(int(iR)-int(jR))
            distR = math.sqrt(float(distR))

            distTotal = distB + distG + distR
            print(distTotal)
            print("Index centros: {}".format(indexCentros))
            print("Index total: {}".format(index))
            if indexCentros == 0:
                #del clavesMinimas[numCentroide]
                #clavesMinimas.insert(numCentroide, keyFrame)
                clavesMinimas.append(keyFrame)
                #del valoresMinimos[numCentroide]
                #valoresMinimos.insert(numCentroide, keyCentroide)
                valoresMinimos.append(keyCentroide)

            if distTotal < distanciaMinima:
                distanciaMinima = distTotal
                #if valoresMinimos[index] == None:
                    #valoresMinimos.append(keyCentroide)
                del valoresMinimos[index]
                valoresMinimos.insert(index, keyCentroide)
                #valoresMinimos[index] = keyCentroide

            
            indexCentros += 1

            
            

            #print("=====================================================")
            
            

            distKeyFrameDict[keyFrame] = distTotal

            #for distancia in distKeyFrameDict.values():
                #if distancia == distTotal:
                    #centroidesFrames[distKeyFrameDict[index]] = distancia
                

            #listFramesLuis = [k for k,v in distKeyFrameDict.items() if v == distanciaMinima]

            #print(listFramesLuis)

            centroidAllFramesDict[keyCentroide] = distKeyFrameDict

        index += 1

            
        
        #print(minimum)
    minimumTotal = minimum
    #print(minimumTotal)
    #print(centroidAllFramesDict)
    print(clavesMinimas)
    print(valoresMinimos)


def CalcularFotogramasClave(INPUTPATH, T, K, H):
    ListaFrames = dict()
    if __name__ == '__main__':
        ListaFrames = recorre_imagenes(INPUTPATH, T, H)
        #print(ListaFrames)
    
    aplicaKmedias(ListaFrames, K, H, INPUTPATH)


CalcularFotogramasClave("C:\\Users\\Juanmi\\Desktop\\Pictures AI project",2,3,256)
#aplicaKmedias(list(), 3, 256)
#listaPrueba = calcularCentrosIniciales(256, 3)
