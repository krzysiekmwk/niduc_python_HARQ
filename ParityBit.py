from FileOperator import *

class ParityBit:

    def addParityBit(self, bitList):
        counter = 0
        for bit in bitList:
            if(bit == '1'):
                counter += 1

        # sprawia ze liczba jedynek bedzie parzysta
        if(counter % 2 == 0):
            bitList.append('0')     # 0 jesli ilosc jedynek jest parzysta
        else:
            bitList.append('1')     # 1 jesli ilosc jedynek jest parzysta

        return bitList

    def checkParity(self, bitList):
        counter = 0
        for bit in bitList:
            if (bit == '1'):
                counter += 1

        if (counter % 2 == 0):
            return True
        else:
            return False

    def deleteParityBit(self, bitList):
        tmp = []
        i = 0
        for bit in bitList:
            if(i < len(bitList) - 1):
                tmp.append(bit)
            i += 1
        return tmp
'''
bitList = []
fileOperator = FileOperator()
bitList = fileOperator.readFile("test.txt")
print(bitList)
parity = ParityBit()
bitList = parity.addParityBit(bitList)
print(bitList)
print(parity.checkParity(bitList))
bitList[0] = '1'
print(bitList)
print(parity.checkParity(bitList))
bitList = parity.deleteParityBit(bitList)
print(bitList)
'''
