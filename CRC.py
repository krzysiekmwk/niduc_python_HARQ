from FileOperator import *
import numpy

class CRC:

    def addCRC(self, bitList): # wrzucenie trzech 0 na koniec naszej paczki
        for i in range(0,3):
            bitList.append('0')
        return bitList

    def computeCRC(self, bitList): #polynomial x^3 + x + 1 --> 1011, liczymy remainder -> tak jak na wiki
        tmp = [] # robimy kopie bo inaczej mamy wezeorwany pakiecik
        for bit in bitList:
            tmp.append(bit)
        polynomial = ['1','0','1','1']
        lenInput = len(tmp)
        while '1' in tmp[:lenInput]:
            moveRight = tmp.index('1')
            for i in range(len(polynomial) - 1):
                if polynomial[i] == tmp[moveRight + i]:
                    tmp[moveRight + i] = '0'
                else:
                    tmp[moveRight + i] = '1'
        return tmp[lenInput:]

    def isValid(self, bitList): # metoda isValid
        tmp = CRC.computeCRC(self, bitList) # liczymy sobie ten remainder
        counter = 0
        for bit in tmp:
            if bit == '1':
                counter += 1
        if counter == 0: # jezeli ostatecznie lista bedzie skladala sie z samych 0 lub bedzie pusta
            return True # oznacza ze nie ma bledu
        else:
            return False # jest blad

    def deleteCRC(self, bitList): # wyrzucenie tych 3 bitow dorzuconych na koncu
        bitList = bitList[:-3]
        return bitList


''' # przyklad z wiki
bitList = ['1','1','0','1','0','0','1','1','1','0','1','1','0','0']
crc = CRC()
crc.addCRC(bitList)
print(bitList)
print(crc.isValid(bitList))
print(crc.deleteCRC(bitList))
'''