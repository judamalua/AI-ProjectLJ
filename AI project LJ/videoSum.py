import os
import cv2
from matplotlib import pyplot as plt
import numpy as np
from random import randint
from PIL import Image

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

            cv2.cv2.imshow('image', img)

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

def calcularCentroidesIniciales(H, K):
    ListaCentroides = dict()

    # Creamos una imagen negra
    imgN = np.zeros([512,512,3], dtype=np.uint8)

    # Creamos una imagen blanca
    imgB = np.zeros([512,512,3], dtype=np.uint8)
    imgB.fill(255)

    #dataN[256, 256] = [255, 0, 0]
    # Con la librería Image pasamos los datos de la matriz a imagen
    #imgN = Image.fromarray(dataN, 'RGB')
    #imgN.show()

    color = ('b', 'g', 'r')
    histr = dict()

    for i,col in enumerate(color):
        histr[col] = cv2.cv2.calcHist([imgN], [i], None, [H], [0,H])
        print(histr)
        plt.plot(histr[col], color = col)
        plt.xlim([0,H])
        ListaCentroides["Centroide negro"] = histr
    
    plt.show()

    for j,colB in enumerate(color):
        histr[colB] = cv2.cv2.calcHist([imgB], [j], None, [H], [0,H])
        print(histr)
        plt.plot(histr[colB], color = colB)
        plt.xlim([0,H])
        ListaCentroides["Centroide blanco"] = histr
    
    plt.show()


    for index in range(K - 2):
        red, green, blue = (randint(0,255), randint(0,255), randint(0,255)), (randint(0,255), randint(0,255), randint(0,255)), (randint(0,255), randint(0,255), randint(0,255))
        rgb = [red, green, blue]
        title = "Centroide aleatorio {}".format(index)

        # Creamos una imagen aleatoria
        randImg = np.zeros([512,512,3], dtype=np.uint8)
        #randImg.fill(randint(0,255))

        #for x in range(512):
            #for y in range(512):
                #randImg[x][y] = randint(0,255)

        #randImg = np.random.rand(512, 512, 3)
        for x in range(512):
            for y in range(512):
                randImg[x][y] = rgb[randint(0,2)]

    
    
        cv2.cv2.imshow('image', randImg)


        for k,colR in enumerate(color):
            histr[colR] = cv2.cv2.calcHist([randImg], [k], None, [H], [0,H])
            print(histr)
            plt.plot(histr[colR], color = colR)
            plt.xlim([0,H])
            ListaCentroides[title] = histr
    
        plt.show()

    return ListaCentroides



def aplicaKmedias(ListaFrames, K, H):
    ListaFramesConClasificacion = dict()
    centroidesIniciales = calcularCentroidesIniciales(H, K)



def CalcularFotogramasClave(INPUTPATH, T, K, H):
    ListaFrames = dict()
    if __name__ == '__main__':
        ListaFrames = recorre_imagenes(INPUTPATH, T, H)
        #print(ListaFrames)
    
    aplicaKmedias(ListaFrames, K, H)


#CalcularFotogramasClave("C:\\Users\\Juanmi\\Desktop\\Pictures AI project",4,3,256)
#aplicaKmedias(list(), 3, 256)
listaPrueba = calcularCentroidesIniciales(256, 3)
