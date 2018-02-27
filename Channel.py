# kanal transmisyjny
# dodawanie zaklocen wg okreslonego modelu (BSC, Gilberta)

import random


class Channel:
    __prop = 1  # prawdopodobienstwo wystapienia zaklocenia  0 - 100
    __noisePropS0 = 0  # prawdopodobienstwo zaklocenia w stanie S0
    __noisePropS1 = 0  # prawdopodobienstwo zaklocenia w stanie S1

    # S0 stan z malym prawd. bledu
    # S1 stan z duzym prawd. bledu

    __P00 = 0  # prawd. przejscia z S0 do S0
    __P01 = 0  # prawd. przejscia z S0 do S1
    __P11 = 0  # prawd. przejscia z S1 do S1
    __P10 = 0  # prawd. przejscia z S1 do S0
    __gilbertState = 0  # stan w jakim sie znajduje model Gilberta

    def __init__(self, prop, s0, s1, p00, p01, p11, p10):
        self.__prop = prop
        self.__noisePropS0 = s0
        self.__noisePropS1 = s1
        self.__P00 = p00
        self.__P01 = p01
        self.__P11 = p11
        self.__P10 = p10

    def addBSCNoise(self, bit):

        if (self.draw(self.__prop)):
            if (bit == '0'):
                bit = '1'
            else:
                bit = '0'

        return bit

    def addGilbertNoise(self, bit):
        pass

    def draw(self, propability):
        seed = random.randint(0, 100)
        if (seed <= propability):
            return True
        else:
            return False
