from ParityBit import *
from SelectiveRepeat import *
from StopAndWait import *
from tkinter import *
from Hamming import *

# Wczytanie listy bitow
from StopAndWaitGUI import StopAndWaitGUI

bitList = []
fileOperator = FileOperator()
bitList = fileOperator.readFile("test.jpg")
print(bitList)
parity = ParityBit()

packets = []
packet = []

# GENEROWANIE LISTY PAKIETOW DO WYSLANIA
counter = 0
for bit in bitList:
    packet.append(bit)  # generuje pakiet

    counter += 1
    if (counter == 8):  # pakiet po 8 bitow
        packets.append(packet)  # tworzy liste pakietow
        packet = []
        counter = 0

# DODANIE BITU PARZYSTOSCI DO KAZDEGO Z PAKIETOW
tmr = TMR()
hamming = Hamming()
print(packets)
packetsWithParityBit = []
for pack in packets:
    pack = parity.addParityBit(pack)
    pack = tmr.codeTMR(pack)    # DODANIE TMR
    pack = hamming.codeHamming(pack) # odpalenie Hamminga, !jeszcze na znakach!
    packetsWithParityBit.append(pack)

print(packetsWithParityBit)

channel = Channel(0.00000000000003,0.1,0.1,0.3,0.6)

tk = Tk()
canvas = Canvas(tk, width=500, height=400, bg="#b6f7a3")
canvas.pack()
tk.title("GUI")

# sr = SelectiveRepeat(packetsWithParityBit, channel, parity, 5)
# sr = StopAndWait(packetsWithParityBit,channel,parity)
sr = StopAndWaitGUI(packetsWithParityBit,channel,parity,canvas, tk)
sr.transmit()
packList = sr.getDestinationPackets()

print(packList)
# USUWANIE BITOW PARZYSTOSCI Z KAZDEGO PAKIETU
packets = []
for pack in packList:
    pack = tmr.decodeTMR(pack)  # USUWANIE TMR
    pack = hamming.decodeHamming(pack) # usuniecie Hamminga
    pack = parity.deleteParityBit(pack)
    packets.append(pack)

print(packets)

# TWORZENIE PLIKU WYNIKOWEGO
bitListFinal = []
for package in packets:
    for bit in package:
        bitListFinal.append(bit)

print(bitListFinal)

print("save data")
fileOperator.saveFile("wynik.jpg", bitListFinal)
print("end")

#METODA ZLICZAJACA BLEDY
counterError = 0
ind = 0
for bit in bitListFinal:
    if (bit != bitList[ind]):
        counterError += 1
    ind += 1

print("ilosc blednych bitow wynikowych")
print(counterError)
print("ilosc pakietow ogolem")
print(len(bitListFinal))

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

tk.mainloop()
