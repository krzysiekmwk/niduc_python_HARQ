import numpy
from FileOperator import *

class Hamming:

    def createPacket4(self, pack): # robimy z naszych pakiecikow po 8, pakieciki po 4 do Hamminga
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

    def createPacket7(self, pack): # robimy z naszych pakiecikow robimy pakieciki po 7 do ParitiyCheck Hamminga
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
            if counter == 7:
                newPacket.append(packet)
                counter = 0
                packet = []
        length = len(packet)
        for i in range(0, 7 - length):
            packet.append(0)
        newPacket.append(packet)
        matrix = numpy.asarray(newPacket)
        return numpy.transpose(matrix)


    def codeHamming(self, pack):   #uzywajac macierzy G kodujemy nasz pakiecik
        newPacket = self.createPacket4(pack)
        g = numpy.array([[1,1,0,1],[1,0,1,1],[1,0,0,0],[0,1,1,1],[0,1,0,0],[0,0,1,0],[0,0,0,1]]) #(7,4)
        enc = numpy.dot(g, newPacket)%2
        #Powrot do listy char. ENC posiada 7 wierszy po kilka kolumn (len/7)
        charEnc = self.numpyToChar(enc)
        #nummi = self.charToNumpy(charPack) #wyglada tak samo jak enc
        return charEnc

    def parityCheck(self, enc): #uzywamy macierzy H aby stworzyc macierz na ktorej sprawdzimy czy sa bledy
        enc = self.createPacket7(enc) # ValueError: setting an array element with a sequence.
        h = numpy.array([[1,0,1,0,1,0,1],[0,1,1,0,0,1,1],[0,0,0,1,1,1,1]]) #(3,7)
        parch = numpy.dot(h, enc)%2
        charParch = self.numpyToChar(parch)
        return charParch

    def isValid(self, enc):
        parch = self.parityCheck(enc)
        counter = 0
        for i in parch:
            if i == '1': # jezeli jest 1 czyli argument maksymalny to znaczy ze jest blad
                counter += 1
        if counter > 1:
            return False #sa minimum 2 bledy, hamming juz tego nie ogarnie
        else:
            return True #nie ma bledu lub jest tylko 1 wiec mozna naprawic

    def decodeHamming(self, enc): #uzywamy macierz R do odkodowania, robimy to dopiero jak poprawimy bledy "duh"
        parch = self.parityCheck(enc)
        number = 0
        for index, bit in enumerate(parch): # liczymy od 0
            if bit == '1':
                print(index)
                number += 2^index # liczymy z binarki od razu na system dziesietny
        print(number)
        print(enc)
        for index, bit in enumerate(enc): # jezeli bylo 0 robimy 1, a z 1 robimy 0
            if index == number:
                if bit == '1':
                    enc[index] = '0'
                else:
                    enc[index] = '1'
        print(enc)
        r = numpy.array([[0,0,1,0,0,0,0],[0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1]]) # (4,7)
        enc = self.createPacket4(enc)
        dec = numpy.dot(r, enc)
        charDec = self.numpyToChar(dec)
        return charDec

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


#mala zabawa i powtorka z algebry
'''
a = numpy.array([[1,2],[3,4]])
b = numpy.array([[1,2],[3,4]])
wynik1 = numpy.dot(a,b)
b = numpy.transpose(b)
wynik2 = numpy.dot(a,b)
print(wynik1)
print(wynik2)
'''

# podstawowe testy

bitList = []
fileOperator = FileOperator()
bitList = fileOperator.readFile("test.txt")
print(bitList)
hamming = Hamming()
bitList = hamming.codeHamming(bitList)
print(bitList)
print(hamming.parityCheck(bitList))
print("dlugosc bitlist przed")
print(len(bitList))
bitList = hamming.decodeHamming(bitList)
print(bitList)
print("dlugosc bitlist po")
print(len(bitList))
