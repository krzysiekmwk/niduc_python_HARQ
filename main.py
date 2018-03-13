from FileOperator import *
from Channel import *
from TMR import *
from ByteConverter import *
from ParityBit import *
from SelectiveRepeat import *



# Wczytanie listy bitow

bitList = []
fileOperator = FileOperator()
bitList = fileOperator.readFile("test.jpg")
#print(bitList)
parity = ParityBit()

packets = []
packet = []

counter = 0
for bit in bitList:
    packet.append(bit)  # generuje pakiet

    counter += 1
    if (counter == 8):  # pakiet po 8 bitow
        packets.append(packet)  # tworzy liste pakietow
        packet = []
        counter = 0

packets1 = []
for pack in packets:
    pack1 = []
    pack1 = parity.addParityBit(pack)
    packets1.append(pack1)


channel = Channel(0.3,0.01,0.01,0.3,0.6)

sr = SelectiveRepeat(packets1,channel,parity,5)
sr.transmit()
packList = sr.getDestinationPackets()


bitList1 = []
for pack in packList:
    pack1 = []
    pack1 = parity.deleteParityBit(pack)
    bitList1.append(pack1)

print("save data")
fileOperator.saveFile("wynik.jpg", bitList1)
print("end")

#METODA ZLICZAJACA BLEDY
counterError = 0
ind = 0
for pack in packets:
    if (pack != bitList1[ind]):
        counterError += 1
    ind += 1

#UWAGA TO Nie DZIALA NIE SUGEROAC SIE TYM
print("TA FUNKCJA NIE DZIALA :D ->")
print("ilosc blednych pakietow")
print(counterError)
print("ilosc pakietow ogolem")
print(len(packets))
# # Symulacja wyslania (modyfikacja danych)
# bitListToSend = []
#
#
# tmr = TMR()
# bitListToSend = bitList
# bitListToSend = tmr.codeTMR(bitList)  # użycie TMR
#
# # Wprowadzenie zaklocen
# channel = Channel(1,0.01,0.9,0.2,0.55)
# for bit in bitListToSend:
#     bitListReceived.append(channel.addBSCNoise(bit, 0.0001))
# #newBitList.append(channel.addGilbertNoise(bit))
#
#
# bitListReceived = tmr.decodeTMR(bitListReceived)
#
# # Sprawdzenie ilosci przeklamanych bitow
# counter = 0
# index = 0
# for bit in bitList:
#     if (bit != bitListReceived[index]):
#         counter += 1
#     index += 1
#
# print("ilosc bledow: ", counter)  # ilosc przeklamanych bitow
# print("Procent bledow: ", counter/len(bitList), "%")  # Procent przekłamanych bitów



# Zapis listy bitow

