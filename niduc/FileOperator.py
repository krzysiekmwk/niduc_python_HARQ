#pobieranie pliku binarnego (.wav, .dat) konwertowanie go na bajty
import array
import random
class FileOperator:

    # wczytuje plik w postaci zer i jedynek do listy bitów
    def readFile(self, filePath):
        bitList = []
        with open(filePath, "rb") as f:
            byte = f.read(1)    # pobranie pojedynczego bajtu
            while byte != b'':
                bitFromByte = [bin(char)[2:].zfill(8) for char in byte] # wyciagniecie pojedynczych bitow
                for i in range(0, 8):
                    bitList.append(bitFromByte[0][i])   # wsadzenie bitow do listy
                byte = f.read(1)
        f.close()
        return bitList

    # zapis pliku binarnego
    def saveFile(self, filePath, bitList):
        file = open(filePath, "wb")

        byte_list = []
        for i in range(0, len(bitList), 8):
            byte = 0
            index = 7
            for j in range(i, i + 8): # wytworzenie bajtu z pojedynczych bitow
                if(bitList[j] == '1'):
                    byte |= (1 << index)
                index -= 1

            byte_list.append(byte)  # wrzucenie bajtu do listy bajtow

        file.write(bytearray(byte_list))    # zapis listy do pliku.
        file.close()
