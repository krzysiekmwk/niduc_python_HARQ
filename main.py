from FileOperator import *
from Channel import *
from TMR import *
from ByteConverter import *

bitList = []

# Wczytanie listy bitow
fileOperator = FileOperator()
print("read data")
bitList = fileOperator.readFile("test.jpg")

# Symulacja wyslania (modyfikacja danych)
bitListToSend = []
bitListReceived = []

tmr = TMR()
bitListToSend = bitList
#bitListToSend = tmr.codeTMR(bitList)  # użycie TMR

# Wprowadzenie zaklocen
channel = Channel(1,0.01,0.9,0.2,0.55)
for bit in bitListToSend:
    bitListReceived.append(channel.addBSCNoise(bit, 0.0001))
    #newBitList.append(channel.addGilbertNoise(bit))


#bitListReceived = tmr.decodeTMR(bitListReceived)

# Sprawdzenie ilosci przeklamanych bitow
counter = 0
index = 0
for bit in bitList:
    if (bit != bitListReceived[index]):
        counter += 1
    index += 1

print("ilosc bledow: ", counter)  # ilosc przeklamanych bitow
print("Procent bledow: ", counter/len(bitList), "%")  # Procent przekłamanych bitów

bitList = bitListReceived

# Zapis listy bitow
print("save data")
fileOperator.saveFile("wynik.jpg", bitList)
print("end")
