from ParityBit import *
from StopAndWait import *
from SelectiveRepeat import *
from Hamming import *
from CRC import *

# Wczytanie listy bitow
from StopAndWaitGUI import *
from SelectiveRepeatGUI import *

def nextStep():
    global waitForNextStep
    waitForNextStep = False

waitForNextStep = True;


iloscPetli = 1
wielkoscPakietu = 8
wielkoscOknaSR = 5

isBSC = True    # True - BSC / False - Gilbert
isSAW = True    # True - SAW / FALSE - SR

sumaTestowBER = 0
iloscBER = iloscPetli


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
varChannel = IntVar()
Radiobutton(canvas, text="BSC", variable=varChannel,value=1).pack()
EBSC = Entry(canvas)
EBSC.pack()
EBSC.insert(0,1)
Radiobutton(canvas, text="Gilbert", variable=varChannel, value=2).pack()
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
varPACK = IntVar()
Radiobutton(canvas, text="TMR + Parity", variable=varPACK,value=1).pack()
Radiobutton(canvas, text="Hamming + CRC32", variable=varPACK, value=2).pack()
Button(canvas, text="START", command=nextStep).pack()
tk.update()

bitList = []
fileOperator = FileOperator()

while (waitForNextStep):
    canvas.update()

waitForNextStep = True;
fileName = Efile.get()

bitList = fileOperator.readFile(fileName)
parity = ParityBit()

if varChannel.get() == 1:
    isBSC = True
if varChannel.get() == 2:
    isBSC = False

packets = []
packet = []

# GENEROWANIE LISTY PAKIETOW DO WYSLANIA
counter = 0
for bit in bitList:
    packet.append(bit)  # generuje pakiet

    counter += 1
    if (counter == wielkoscPakietu):  # pakiet po 8 bitow
        packets.append(packet)  # tworzy liste pakietow
        packet = []
        counter = 0

if(len(packet) > 0):    # mozliwe tworzenie pakietow wiekszych niz 8 bitow. po prostu ostatni pakiet, bedzie malutki
    packets.append(packet)

# DODANIE BITU PARZYSTOSCI DO KAZDEGO Z PAKIETOW
tmr = TMR()
hamming = Hamming()
parity = ParityBit()
crc = ParityBit()
channel = Channel(float(str(EBSC.get())),float(str(EG1.get())),float(str(EG2.get())),float(str(EG3.get())),float(str(EG4.get())))

packetsWithParityBit = []
for pack in packets:
    if varPACK.get() == 1:
        pack = tmr.codeTMR(pack)  # DODANIE TMR
        pack = parity.addParityBit(pack)
    if varPACK.get() == 2:
        pack = hamming.codeHamming(pack)  # DODANIE Hamming
        pack = crc.addParityBit(pack)

    packetsWithParityBit.append(pack)

sr = StopAndWait(packetsWithParityBit, channel, parity, isBSC) # przypisanie czegokolwiek, coby sie python nie czepial

if CheckVar.get() == 0:
    if varProtocol.get() == 1:
        print("VAR 0 PROT 1")
        sr = SelectiveRepeat(packetsWithParityBit, channel, parity, wielkoscOknaSR, isBSC)
    if varProtocol.get() == 2:
        print("VAR 0 PROT 2")
        sr = StopAndWait(packetsWithParityBit, channel, parity, isBSC)
else:
    if varProtocol.get() == 2:
        print("VAR 1 PROT 2")
        sr = StopAndWaitGUI(packetsWithParityBit, channel, parity, isBSC, tk)
    if varProtocol.get() == 1:
        print("VAR 1 PROT 1")
        sr = SelectiveRepeatGUI(packetsWithParityBit, channel, parity, wielkoscOknaSR, isBSC, tk)

sr.transmit()
packList = sr.getDestinationPackets()

print(packList)
# USUWANIE BITOW PARZYSTOSCI Z KAZDEGO PAKIETU
packets = []
for pack in packList:
    if varPACK.get() == 1:
        pack = parity.deleteParityBit(pack)
        pack = tmr.decodeTMR(pack)
    if varPACK.get() == 2:
        pack = hamming.decodeHamming(pack)  # usuniecie Hamminga
        pack = crc.deleteParityBit(pack)

    packets.append(pack)

# TWORZENIE PLIKU WYNIKOWEGO
bitListFinal = []
for package in packets:
    for bit in package:
        bitListFinal.append(bit)

# print(bitListFinal)

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
print("BER")
print(counterError / len(bitListFinal) * 100)

BER = counterError / len(bitListFinal) * 100
sumaTestowBER = sumaTestowBER + BER

iloscPetli = iloscPetli - 1

print("KONIEC TESTOW")

print("Srednia BER: ")
print(sumaTestowBER / iloscBER)

# ZAPIS PLIKU WYNIKOWEGO - MOZNA SIE PRZEKONAC JAK WPLYNELY BLEDY NA PLIK
print("save data")
# fileOperator.saveFile("wynik.txt", bitListFinal)
fileOperator.saveFile("wynik.jpg", bitListFinal)
print("end")

tk.mainloop()
