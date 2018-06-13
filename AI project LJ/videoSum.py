import os
import cv2
from matplotlib import pyplot as plt

def recorre_imagenes():
    path = "prueba\\"

    for image in os.listdir(path):
        input_path = os.path.join(path, image)

        print(input_path)

        img = cv2.cv2.imread(input_path)

        cv2.cv2.imshow('image', img)

        color = ('b', 'g', 'r')

        for i,col in enumerate(color):
            histr = cv2.cv2.calcHist([img], [i], None, [256], [0,256])
            plt.plot(histr, color = col)
            plt.xlim([0,256])
        
        plt.show()

if __name__ == '__main__':
    recorre_imagenes()


def CalcularFotogramasClave(INPUTPATH, T, K, H):
    print("Hola")


CalcularFotogramasClave(1,2,3,4)