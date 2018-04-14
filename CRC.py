from FileOperator import *
import numpy

class CRC:

    def addCRC(self, bitList): # wrzucenie trzech 0 na koniec naszej paczki
        for i in range(0,3):
            bitList.append('0')
        return bitList

    def computeCRC(self, bitList): #polynomial x^3 + x + 1 --> 1011, liczymy remainder -> tak jak na wiki
        polynomial = ['1','0','1','1']
        lenInput = len(bitList)
        while '1' in bitList[:lenInput]:
            moveRight = bitList.index('1')
            for i in range(len(polynomial) - 1):
                if polynomial[i] == bitList[moveRight + i]:
                    bitList[moveRight + i] = '0'
                else:
                    bitList[moveRight + i] = '1'
        return bitList

    def isValid(self, bitList): # metoda isValid
        bitList = CRC.computeCRC(self, bitList) # liczymy sobie ten remainder
        counter = 0
        for bit in bitList:
            if bit == '1':
                counter += 1
        if counter == 0: # jezeli ostatecznie lista bedzie skladala sie z samych 0
            return True # oznacza ze nie ma bledu
        else:
            return False # jest blad

    # def logical_xor(self, str1,str2): # zdefniowany xor
    #    return bool(str1) ^ bool(str2)

''' # przyklad z wiki
bitList = ['1','1','0','1','0','0','1','1','1','0','1','1','0','0']
crc = CRC()
crc.addCRC(bitList)
print(bitList)
print(crc.isValid(bitList))
print(bitList)
'''