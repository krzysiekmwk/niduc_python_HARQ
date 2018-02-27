# kanal transmisyjny
# dodawanie zaklocen wg okreslonego modelu (BSC, Gilberta)

import random

class Channel:

    __prop = 0  # prawdopodobienstwo wystapienia zaklocenia na pakiet 0 - 100 %



    def __init__(self,prop):
        self.__prop = prop

    def addBSCNoise(self, packet):
        seed = random.randint(0, 100)

        if(seed <= self.__prop):
            #zaklocanie

        return packet

