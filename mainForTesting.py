from ParityBit import *
from StopAndWait import *
from SelectiveRepeat import *
from Hamming import *
from CRC import *

# Stale do zmieniania do testow
wielkoscPakietu = 8
wielkoscOknaSR = 5

prawdopodobienstwoBSC = 0.00000000000003
channelS0 = 0.1
channelS1 = 0.1
channelP01 = 0.3
channelP10 = 0.6

# Wczytanie listy bitow
bitList = []
fileOperator = FileOperator()
bitList = fileOperator.readFile("test.txt")
print(bitList)

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
crc = CRC()
parity = ParityBit()
channel = Channel(prawdopodobienstwoBSC, channelS0, channelS1, channelP01, channelP10)

print(packets)
packetsWithParityBit = []
for pack in packets:
    pack = tmr.codeTMR(pack)            # DODANIE TMR
    pack = parity.addParityBit(pack)    # DODANIE PARITY BIT
    # pack = hamming.codeHamming(pack)   # DODANIE Hamminga
    # pack = crc.addCRC(pack)            # DODANIE CRC

    packetsWithParityBit.append(pack)

print(packetsWithParityBit)

print("Wysylanie")
# sr = SelectiveRepeat(packetsWithParityBit, channel, parity, wielkoscOknaSR)
sr = StopAndWait(packetsWithParityBit,channel,parity)
sr.transmit()
packList = sr.getDestinationPackets()
print("Odbieranie")

print(packList)
# USUWANIE BITOW PARZYSTOSCI Z KAZDEGO PAKIETU
packets = []
for pack in packList:
    pack = parity.deleteParityBit(pack)     # USUWANIE PARITY BIT
    pack = tmr.decodeTMR(pack)              # USUWANIE TMR

    # pack = hamming.decodeHamming(pack) # usuniecie Hamminga
    # pack = crc.deleteCRC(pack)
    packets.append(pack)                    # USUWANIE CRC

print(packets)

# TWORZENIE PLIKU WYNIKOWEGO
bitListFinal = []
for package in packets:
    for bit in package:
        bitListFinal.append(bit)

print(bitListFinal)

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


# ZAPIS PLIKU WYNIKOWEGO - MOZNA SIE PRZEKONAC JAK WPLYNELY BLEDY NA PLIK
print("save data")
fileOperator.saveFile("wynik.txt", bitListFinal)
print("end")