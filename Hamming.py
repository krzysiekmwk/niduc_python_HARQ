import numpy
from FileOperator import *

class Hamming:

    def createPacket(self, pack): # robimy z naszych pakiecikow po 8, pakieciki po 4 do Hamminga
        packet = []
        newPacket = []
        counter = 0
        for bit in pack:
            if bit == '1':
                packet.append(1)
                counter += 1
            if bit == '0':
                packet.append(0)
                counter += 1
            if counter == 4:
                newPacket.append(packet)
                counter = 0
                packet = []
        length = len(packet)
        for i in range(0, 4 - length):
           packet.append(0)
        newPacket.append(packet)
        matrix = numpy.asarray(newPacket)
        return numpy.transpose(matrix)

    def codeHamming(self, pack):   #uzywajac macierzy G kodujemy nasz pakiecik
        newPacket = self.createPacket(pack)
        g = numpy.array([[1,1,0,1],[1,0,1,1],[1,0,0,0],[0,1,1,1],[0,1,0,0],[0,0,1,0],[0,0,0,1]]) #(7,4)
        enc = numpy.dot(g, newPacket)%2
        #Powrot do listy char. ENC posiada 7 wierszy po kilka kolumn (len/7)
        charPack = self.numpyToChar(enc)
        #nummi = self.charToNumpy(charPack) #wyglada tak samo jak enc
        return charPack

    def parityCheck(self, enc): #uzywamy macierzy H aby stworzyc macierz na ktorej sprawdzimy czy sa bledy
        enc = numpy.asarray(enc, dtype = int) # ValueError: setting an array element with a sequence.
        h = numpy.array([[1,0,1,0,1,0,1],[0,1,1,0,0,1,1],[0,0,0,1,1,1,1]])
        parch = numpy.dot(h, enc)%2
        return parch

    def isValid(self, enc):
        parch = Hamming.parityCheck(self, enc)
        counter = 0
        if numpy.argmax(parch) == 1: # jezeli jest 1 czyli argument maksymalny to znaczy ze jest blad
            counter += 1
        if counter > 1:
            return False #sa minimum 2 bledy, hamming juz tego nie ogarnie
        else:
            return True #nie ma bledu lub jest tylko 1 wiec mozna naprawic

    def decodeHamming(self, enc, parch): #uzywamy macierz R do odkodowania, robimy to dopiero jak poprawimy bledy "duh"
        number = 0
        for index, bit in enumerate(parch): # liczymy od 0
            if bit == 1:
                number += 2^index # liczymy z binarki od razu na system dziesietny
        if enc[number] == '0': # jezeli bylo 0 robimy 1
            enc[number] == '1'
        else:
            enc[number] == '0'
        r = numpy.array([[0,0,1,0,0,0,0],[0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1]])
        dec = numpy.dot(r, enc)
        return dec

    def numpyToChar(self, enc):
        chA = []
        for row in enc:
            for col in row:
                if col == 1:
                    chA.append('1')
                if col == 0:
                    chA.append('0')
        return chA

    def charToNumpy(self, list):
        listLength = len(list)
        rowsNumber = listLength / 7
        row = []
        col = []
        i = 0
        for char in list:
            if(char == '1'):
                row.append(1)
            else:
                row.append(0)

            i += 1

            if(i == rowsNumber):
                i = 0
                col.append(row)
                row = []

        return numpy.array(col)

    def chToInt(self, chA): # nie dziala :c
        # The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
        intA = []
        for bit in chA:
            if bit == '1':
                intA.append(0)
            if bit == '0':
                intA.append(0)
        return numpy.array(intA)