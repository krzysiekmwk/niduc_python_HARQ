# kanal transmisyjny
# dodawanie zaklocen wg okreslonego modelu (BSC, Gilberta)

import random


class Channel:
    __prop = 1  # prawdopodobienstwo wystapienia zaklocenia  0.0 - 1.0
    __noisePropS0 = 0  # prawdopodobienstwo zaklocenia w stanie S0
    __noisePropS1 = 0  # prawdopodobienstwo zaklocenia w stanie S1

    # S0 stan z malym prawd. bledu
    # S1 stan z duzym prawd. bledu

    __P00 = 0  # prawd. przejscia z S0 do S0
    __P01 = 0  # prawd. przejscia z S0 do S1
    __P11 = 0  # prawd. przejscia z S1 do S1
    __P10 = 0  # prawd. przejscia z S1 do S0
    __gilbertState = 0  # stan w jakim sie znajduje model Gilberta

    def __init__(self, prop, s0, s1, p01, p10):
        self.__prop = prop
        self.__noisePropS0 = s0
        self.__noisePropS1 = s1
        self.__P01 = p01
        self.__P00 = 1 - p01
        self.__P10 = p10
        self.__P11 = 1 - p10

    def addBSCNoise(self, bit, prop):  #zmiana na przeciwny bit z danym prawdopodobienstwem
        if (self.draw(prop)):
            if (bit == '0'):
                bit = '1'
            else:
                bit = '0'

        return bit

    def addGilbertNoise(self, bit):
        if(self.__gilbertState == 0):       #losowanie stanu modelu Gilberta
            if(self.draw(self.__P01)):
                self.__gilbertState = 1
        elif(self.__gilbertState == 1):
            if(self.draw(self.__P10)):
                self.__gilbertState = 0

        if(self.__gilbertState == 0):                               #zamiana bitu na przeciwny z prawdopodobienstwem dla danego stanu modelu
            bit = self.addBSCNoise(bit,self.__noisePropS0)
        elif(self.__gilbertState == 1):
            bit = self.addBSCNoise(bit,self.__noisePropS1)

        #print("GILBERT:{}".format(self.__gilbertState))
        return bit

    def draw(self, propability):  #losowanie czy wystapi zdarzenie z okreslonym prawdopodobienstwem seed -> 0.0 - 1.0
        seed = random.random()
        #print("SEED:{}".format(seed))
        if (seed <= propability):
            return True
        else:
            return False

'''
channel = Channel(1,0.01,0.9,0.2,0.55)
counter = 0
for x in range(0,100):
    bit = '0'
    bit = channel.addGilbertNoise(bit)
    if(bit == '1'):
        counter += 1
    print(bit)
print(counter) # ilosc przeklamanych bitow
'''