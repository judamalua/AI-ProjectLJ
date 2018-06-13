import os
import cv2
from matplotlib import pyplot as plt

def recorre_imagenes(T, H):
    path = "C:\\Users\\Juanmi\\Desktop\\Pictures AI project"
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

            cv2.cv2.imshow('image', img)

            color = ('b', 'g', 'r')

            for i,col in enumerate(color):
                histr = cv2.cv2.calcHist([img], [i], None, [H], [0,256])
                plt.plot(histr, color = col)
                plt.xlim([0,256])
                ListaFrames.append(histr)
        
            plt.show()

    return ListaFrames


def CalcularFotogramasClave(INPUTPATH, T, K, H):
    if __name__ == '__main__':
        ListaFrames = recorre_imagenes(T, H)
        #print(ListaFrames)


CalcularFotogramasClave(1,4,3,256)