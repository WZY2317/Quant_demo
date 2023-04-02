import numpy as np


def cau():
    a = np.array([21.6, 71.1, 173.7, 262.8, 358.4, 418.8])
   
    for x in a:
        print(1 - x / 500)


cau()
