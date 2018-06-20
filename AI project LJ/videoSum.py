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
    ListaFramesTotales = dict()

    ##for image in os.listdir(path):
        ##input_path = os.path.join(path, image)

        ##print(input_path)

        ##img = cv2.cv2.imread(input_path)
        ##imgSize = len(img)
        ##break
    for image in os.listdir(path):
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
            
        ListaFramesTotales[input_path] = histr
        
            #plt.show()

    # Creamos una imagen negra
    ##imgN = np.zeros([imgSize,imgSize,3], dtype=np.uint8)

    # Creamos una imagen blanca
    ##imgB = np.zeros([imgSize,imgSize,3], dtype=np.uint8)
    ##imgB.fill(255)

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
        histr1 = dict()
        histr2 = dict()
        histrSuma = dict()
        aleatorio1 = randint(0, len(ListaFramesTotales.values()) - 1)
        aleatorio2 = randint(0, len(ListaFramesTotales.values()) - 1)
        aleatorio3 = randint(0, len(ListaFramesTotales.values()) - 1)
        #print(aleatorio1)
        #print("=========================")
        #print(aleatorio2)
        #print("=========================")
        #print(aleatorio3)
        #print("=========================")

        #imgSuma = np.zeros([imgSize,imgSize,3], dtype=np.uint8)
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

        sumaB = [sum(x)/3 for x in zip(*listOfListsB)]#np.sum(histr1["b"], histr2["b"])
        #sumaB /= 2
        sumaG = [sum(y)/3 for y in zip(*listOfListsG)]#np.sum(histr1["g"], histr2["g"])
        #sumaG /= 2
        sumaR = [sum(z)/3 for z in zip(*listOfListsR)]#np.sum(histr1["r"], histr2["r"])
        #sumaR /= 2
        
        histrSuma["b"] = sumaB
        histrSuma["g"] = sumaG
        histrSuma["r"] = sumaR

        ##ListaCentroides[title] = histr1

        ListaCentroides[title] = histrSuma

        ##for k,colR in enumerate(color):
            #histr[colR] = cv2.cv2.calcHist([randImg], [k], None, [H], [0,H])
            ##print(histrSuma)
            ##plt.plot(histrSuma[colR], color = colR)
            ##plt.xlim([0,H])
        
        #ListaCentroides[title] = histr
    
        ##plt.show()
        

    ##for index in range(K):
        ##red, green, blue = (randint(0,255), randint(0,255), randint(0,255)), (randint(0,255), randint(0,255), randint(0,255)), (randint(0,255), randint(0,255), randint(0,255))
        ##rgb = [red, green, blue]
        ##title = "Centroide aleatorio {}".format(index)

        # Creamos una imagen aleatoria
        ##randImg = np.zeros([imgSize,imgSize,3], dtype=np.uint8)
        #randImg.fill(randint(0,255))

        #for x in range(512):
            #for y in range(512):
                #randImg[x][y] = randint(0,255)

        #randImg = np.random.rand(512, 512, 3)
        ##for x in range(imgSize):
            ##for y in range(imgSize):
                ##randImg[x][y] = rgb[randint(0,2)]

    
    
        #cv2.cv2.imshow('image', randImg)

        ##histr = dict()

        ##for k,colR in enumerate(color):
            ##histr[colR] = cv2.cv2.calcHist([randImg], [k], None, [H], [0,H])
            #print(histr)
            #plt.plot(histr[colR], color = colR)
            #plt.xlim([0,H])
        
        ##ListaCentroides[title] = histr
    
        #plt.show()

    return ListaCentroides



def aplicaKmedias(ListaFrames, K, H, INPUTPATH):
    ListaFramesConClasificacion = dict()
    distKeyFrameDict = dict()
    centroidAllFramesDict = dict()
    centroidesFrames = dict()
    minimumTotal = 0
    color = ('b', 'g', 'r')
    
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

    for keyCentro in centroidesIniciales.keys():
        ListaFramesConClasificacion[keyCentro] = list()

    numCentroide = 0
    index = 0
    for frame, keyFrame in zip(ListaFrames.values(), ListaFrames.keys()):
        minimum = 0
        nombreCentro = ""
        indexCentros = 0
        #print(frame)
        
        #print("==============================================")
        distanciaMinima = math.inf
        for centroideInicial, keyCentroide in zip(centroidesIniciales.values(), centroidesIniciales.keys()):
            distTotal = 0
            distB = 0
            distG = 0
            distR = 0
            
            #for dist, col in enumerate(color):
                #distTotal += sum(math.sqrt(math.pow([x - y for (x, y) in zip(frame[col], centroideInicial[col])], 2)))

            # Para cada frame del canal 'b' calculamos la distancia con cada centro
            for iB in frame["b"]:
                for jB in centroideInicial["b"]:
                    distB += math.pow((int(iB) - int(jB)), 2)
            distBSqrt = math.sqrt(float(distB))

            # Para cada frame del canal 'g' calculamos la distancia con cada centro
            for iG in frame["g"]:
                for jG in centroideInicial["g"]:
                    distG += math.pow((int(iG) - int(jG)), 2)
            distGSqrt = math.sqrt(float(distG))

            # Para cada frame del canal 'r' calculamos la distancia con cada centro
            for iR in frame["r"]:
                for jR in centroideInicial["r"]:
                    distR += math.pow((int(iR) - int(jR)), 2)
            distRSqrt = math.sqrt(float(distR))

            distTotal = (distBSqrt + distGSqrt + distRSqrt)/3

            #print(distTotal)
            #print("Index centros: {}".format(indexCentros))
            #print("Index total: {}".format(index))
            if indexCentros == 0:
                clavesMinimas.append(keyFrame)
                valoresMinimos.append(keyCentroide)

            if distTotal < distanciaMinima:
                distanciaMinima = distTotal
                del valoresMinimos[index]
                valoresMinimos.insert(index, keyCentroide)
                nombreCentro = keyCentroide

            
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

            
        ListaFramesConClasificacion[nombreCentro].append(keyFrame)
        #print(ListaFramesConClasificacion)
        #print(minimum)
    
    
    minimumTotal = minimum
    #print(minimumTotal)
    #print(centroidAllFramesDict)
    print(clavesMinimas)
    print(valoresMinimos)
    print("==============================================================")
    #print(ListaFramesConClasificacion)

    indiceCentros = 0
    
    
        





def CalcularFotogramasClave(INPUTPATH, T, K, H):
    ListaFrames = dict()
    if __name__ == '__main__':
        ListaFrames = recorre_imagenes(INPUTPATH, T, H)
        #print(ListaFrames)
    
    aplicaKmedias(ListaFrames, K, H, INPUTPATH)


CalcularFotogramasClave("C:\\Users\\Juanmi\\Desktop\\Pictures AI project",5,15,140)
#CalcularFotogramasClave("C:\\Users\\Juanmi\\Desktop\\video manu",10,20,256)
#aplicaKmedias(list(), 3, 256)
#listaPrueba = calcularCentrosIniciales(256, 3)
