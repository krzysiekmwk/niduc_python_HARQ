import numpy
from FileOperator import *

class Hamming:

    def createBitList(self, bitList):
        newBitList = []
        for bit in bitList:
            if(bit == '1'):
                newBitList.append(1)
            if(bit == '0'):
                newBitList.append(0)
        return newBitList

    def codeHamming(self,newBitList): #uzywajac macierzy G kodujemy nasz pakiecik
        g = numpy.array([1,1,0,1],[1,0,1,1],[1,0,0,0],[0,1,1,1],[0,1,0,0],[0,0,1,0],[0,0,0,1])
        enc = numpy.dot(g, newBitList)
        return enc

    def parityCheck(self, enc): #uzywamy macierzy H aby stworzyc macierz na ktorej sprawdzimy czy sa bledy
        h = numpy.array([1,0,1,0,1,0,1],[0,1,1,0,0,1,1],[0,0,0,1,1,1,1])
        parch = numpy.dot(h,enc)
        return parch

    def decodeHamming(self, enc): #uzywamy macierz R do odkodowania, robimy to dopiero jak poprawimy bledy "duh"
        r = numpy.array([0,0,1,0,0,0,0],[0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1])
        dec = numpy.dot(r,enc)
        return dec

    def isValid(self, parch): #metoda isValid
        counter = 0
        for bit in parch:
            if(bit == 1): #jezeli w macierzy parch jest chociaz 1 jedynka, oznacza to blad na jakiejs pozycji
                counter += 1
        if(counter != 0):
            return False #jest blad
        else:
            return True #nie ma bledu

    def findError(self,parch): #jezeli jest blad zobaczmy na jakiej pozycji
        if(self.isValid(parch) == False):
            number = 0
            for index, bit in enumerate(parch): #liczymy od 0
                if(bit == 1):
                    number += 2^index #liczymy z binarki od razu na system dziesietny
            return number #mamy pozycje

    def correctError(self, enc, number): #majac pozycje trzeba bledu sie pozbyc
        if(enc[number] == 0): #3jezeli bylo 0 robimy 1
            enc[number] == 1
        if(enc[number] == 1):
            enc[number] == 0
        return enc
