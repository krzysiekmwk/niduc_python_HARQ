from ParityBit import *
from SelectiveRepeat import *
from StopAndWait import *
from tkinter import *
from Hamming import *

# Wczytanie listy bitow
from StopAndWaitGUI import StopAndWaitGUI
from SelectiveRepeatGUI import SelectiveRepeatGUI

def nextStep():
    global waitForNextStep
    waitForNextStep = False

waitForNextStep = True;


tk = Tk()
tk.geometry("200x700")
canvas = Canvas(tk, width=200, height=700)

canvas.pack()
tk.title("GUI")
tk.update()

Label(canvas, text="File: ").pack()
Efile = Entry(canvas)
Efile.pack()

CheckVar = IntVar()
Checkbutton(canvas, text = "Visualization", variable = CheckVar,
                 onvalue = 1, offvalue = 0).pack()


Label(canvas, text="Channel model:").pack()
var = IntVar()
Radiobutton(canvas, text="BSC", variable=var,value=1).pack()
EBSC = Entry(canvas)
EBSC.pack()
EBSC.insert(0,1)
Radiobutton(canvas, text="Gilbert", variable=var, value=2).pack()
EG1 = Entry(canvas)
EG2 = Entry(canvas)
EG3 = Entry(canvas)
EG4 = Entry(canvas)
EG1.pack()
EG2.pack()
EG3.pack()
EG4.pack()
EG1.insert(0,1)
EG2.insert(0,1)
EG3.insert(0,1)
EG4.insert(0,1)


Label(canvas, text="Protocol:").pack()
varProtocol = IntVar()
Radiobutton(canvas, text="Selective Repeat", variable=varProtocol,value=1).pack()
Radiobutton(canvas, text="Stop And Wait", variable=varProtocol, value=2).pack()

Label(canvas, text="Encoding protcols:").pack()
var = IntVar()
Radiobutton(canvas, text="TMR + Parity", variable=var,value=1).pack()
Radiobutton(canvas, text="Hamming + CRC32", variable=var, value=2).pack()
Button(canvas, text="START", command=nextStep).pack()
tk.update()

bitList = []
fileOperator = FileOperator()

while (waitForNextStep):
    canvas.update()

waitForNextStep = True;
fileName = Efile.get()

bitList = fileOperator.readFile(fileName)
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
    # pack = hamming.codeHamming(pack)   # odpalenie Hamminga, !jeszcze na znakach!
    packetsWithParityBit.append(pack)

print(packetsWithParityBit)

#channel = Channel(0.00000000000003,0.1,0.1,0.3,0.6)
channel = Channel(float(str(EBSC.get())),float(str(EG1.get())),float(str(EG2.get())),float(str(EG3.get())),float(str(EG4.get())))


if CheckVar == 0:
    if varProtocol == 1:
        sr = SelectiveRepeat(packetsWithParityBit, channel, parity, 5)
    if varProtocol == 2:
        sr = StopAndWait(packetsWithParityBit,channel,parity)
else:
    if varProtocol == 2:
        sr = StopAndWaitGUI(packetsWithParityBit,channel,parity, tk)
    if varProtocol == 1:
        sr = SelectiveRepeatGUI(packetsWithParityBit, channel, parity, 5, tk)


sr.transmit()
packList = sr.getDestinationPackets()

print(packList)
# USUWANIE BITOW PARZYSTOSCI Z KAZDEGO PAKIETU
packets = []
for pack in packList:
    pack = tmr.decodeTMR(pack)  # USUWANIE TMR
    # pack = hamming.decodeHamming(pack) # usuniecie Hamminga
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
