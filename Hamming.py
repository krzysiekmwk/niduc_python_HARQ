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
        enc = self.createPacket7(enc)
        h = numpy.array([[1,0,1,0,1,0,1],[0,1,1,0,0,1,1],[0,0,0,1,1,1,1]]) #(3,7)
        parch = numpy.dot(h, enc)%2
        charParch = self.numpyToChar(parch)
        return charParch

    def isValid(self, enc):
        parch = self.parityCheck(enc)
        suma = 0
        dlugosc = len(parch) - 1
        for bit in parch: # liczymy od 0
            if bit == '1':
                if dlugosc != 0:
                    number = 1*pow(2, dlugosc) # liczymy z binarki od razu na system dziesietny
                    suma += number
                    dlugosc -= 1
                else:
                    number = 1
                    suma += number
            else:
                dlugosc -= 1
        if suma > len(enc):
            return False #sa minimum 2 bledy, hamming juz tego nie ogarnie
        else:
            return True #nie ma bledu lub jest tylko 1 wiec mozna naprawic

    def decodeHamming(self, enc): #uzywamy macierz R do odkodowania
        r = numpy.array([[0,0,1,0,0,0,0],[0,0,0,0,1,0,0],[0,0,0,0,0,1,0],[0,0,0,0,0,0,1]]) # (4,7)
        parch = self.parityCheck(enc)
        number = 0
        dlugosc = len(parch) - 1
        suma = 0
        for bit in parch: # liczymy od 0
            if bit == '1':
                if dlugosc != 0:
                    number = 1*pow(2, dlugosc) # liczymy z binarki od razu na system dziesietny
                    suma += number
                    dlugosc -= 1
                else:
                    number = 1
                    suma += number
            else:
                dlugosc -= 1
        if suma > len(enc): # jezeli liczba policzona z binarki jest wieksza niz nasz zakodowany pakiet to oznacza wiecej niz 1 blad
            return enc      #  zwraca to co przyszlo
        for index, bit in enumerate(enc): # jezeli bylo 0 robimy 1, a z 1 robimy 0
            if index == number & number != 0:
                if bit == '1':
                    enc[index] = '0'
                else:
                    enc[index] = '1'
        enc = self.createPacket7(enc)
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

    def chToInt(self, chA):
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

'''
bitList = []
#bitList = ['0','0','0','0','0','0','0','0','0','0','1']
#bitList = ['1','0','1','1','0']
fileOperator = FileOperator()
bitList = fileOperator.readFile("test.txt")
print(bitList)
print("dlugosc bit list na samym pcozatku: ")
print(len(bitList))
hamming = Hamming()
bitList = hamming.codeHamming(bitList)
print("code hamming: ")
print(bitList)
print("dlugosc bit list po code: ")
print(len(bitList))
print("code paritycheck: ")
print(hamming.parityCheck(bitList))
print("dlugosc bitlist przed")
print(len(bitList))
bitList = hamming.decodeHamming(bitList)
print("decode hamming: ")
print(bitList)
print("dlugosc bitlist po")
print(len(bitList))
'''