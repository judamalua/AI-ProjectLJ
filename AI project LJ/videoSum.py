import os
import cv2
from matplotlib import pyplot as plt
import numpy
from random import randint

def recorre_imagenes(INPUTPATH, T, H):
    path = INPUTPATH
    index = T
    ListaFrames = list()

    for image in os.listdir(path):
        if index != T:
            index += 1
        elif index == T:
            index = 1
            input_path = os.path.join(path, image)

            print(input_path)

            img = cv2.cv2.imread(input_path)

            cv2.cv2.imshow('scene', img)

            color = ('b', 'g', 'r')

            for i,col in enumerate(color):
                histr = cv2.cv2.calcHist([img], [i], None, [H], [0,H])
                print(histr)
                plt.plot(histr, color = col)
                plt.xlim([0,H])
                ListaFrames.append(histr)
        
            plt.show()

    return ListaFrames


def aplicaKmedias(ListaFrames, K, H):
    ListaFramesConClasificacion = list()
    centroides = calculaCentroides(K, H)


    



def calculaCentroides(K, H):
    centroides = list()
    histr0 = list()
    histrH = list()
    
    for i in range(H):
        listOfList0 = []
        if i == 0:
            listOfList0.append(10000.)
            histr0.append(listOfList0)
        else:
            listOfList0.append(0.)
            histr0.append(listOfList0)

    for i in range(H):
        listOfListH = []
        if i == H - 1:
            listOfListH.append(10000.)
            histrH.append(listOfListH)
        else:
            listOfListH.append(0.)
            histrH.append(listOfListH)
    
    centroides.append(histr0)
    centroides.append(histrH)


    #print(histr0)
    #print(histrH)
    #print(centroides)
    if K > 2:
        for index in range(K - 2):
            histrK = []
            for j in range(H):
                listOfListDoubleLoop = []
                listOfListDoubleLoop.append(randint(0., 10000.))
                histrK.append(listOfListDoubleLoop)
        
            centroides.append(histrK)

    
    return centroides


def CalcularFotogramasClave(INPUTPATH, T, K, H):
    if __name__ == '__main__':
        ListaFrames = recorre_imagenes(INPUTPATH, T, H)
        #print(ListaFrames)


#CalcularFotogramasClave("C:\\Users\\Juanmi\\Desktop\\Pictures AI project",4,3,256)
aplicaKmedias(list(), 3, 256)