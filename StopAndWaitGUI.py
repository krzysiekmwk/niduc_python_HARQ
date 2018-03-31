#Stop And Wait Protocol

from Channel import *
from TMR import *
from tkinter import *
import time

class StopAndWaitGUI:
    sourcePackages = [] #pakiety ze zrodla
    destPackages = [] #gotowe "przemielone" pakiety
    ###########################################################
    protocol = None #protocol z funkcja sprawdzajaca poprawnosc IsValid !!!
    ###########################################################
    channelModel = None #model channelu
    errorCounter = 0 #ogolna ilosc NAKów

    def __init__(self,src,chan,prot,canvas, tk):
        self.sourcePackages = src
        self.channelModel = chan
        self.protocol = prot
        self.errorCounter = 0
        self.tmr = TMR()
        self.canvas = canvas
        self.tk = tk

    def getDestinationPackets(self): #zwraca "przerobiony" plik
        return self.destPackages

    def getErrors(self):
        return self.errorCounter

    def transmit(self):   #TRANSMITUJE PAKIETY Z sourcePackages do destPackages
        strLab = "Count of package to send: " + str(len(self.sourcePackages))
        countPackage = Label(self.tk, text=strLab)
        self.canvas.create_window(100, 20, window=countPackage)

        packetLabelText = StringVar()
        packetLabel = Label(self.tk, textvariable=packetLabelText)
        self.canvas.create_window(100, 100, window=packetLabel)

        receiveLabelText = StringVar()
        receiveLabel = Label(self.tk, textvariable=receiveLabelText)
        self.canvas.create_window(100, 150, window=receiveLabel)

        print("Rozpoczynam transmisje danych")

        packetsize = len(self.sourcePackages[0])

        tempDest = []
        for i in range(0,len(self.sourcePackages)):
            temp = []
            for j in range(0,packetsize):
                temp.append('0')
            tempDest.append(temp)

        self.destPackages = tempDest

        sended = 0 # ilosc wyslanych pakietow
        packets = len(self.sourcePackages) #ilosc pakietow

        while(sended < packets):  # ! U W A G A JEZELI JEST ZBYT DUZO BLEDOW TO PLIK NIE PRZEJDZIE BO SENDED DOJDZIE DO KONCA A ERRORBUF NIE BEDZIE PUSTY
            print("petla nr {}".format(sended))
            packetLabelText.set("Nr package to send: " + str(sended))
            self.tk.update()
            packet = self.channelModel.addGilbertNoise(self.sourcePackages[sended]) # ZAKLOCANIE

            #ODBIERANIE PAKIETOW
            while (self.protocol.isValid(self.tmr.decodeTMR(packet)) == False): # Sprawdzenie odkodowanego tymczasowo pakietu z TMR
                #TUTAJ BEDZIEMY SPRAWDZAC ACK == TRUE, NAK == FALSE
                self.errorCounter += 1
                print("\twysylanie pakietu {}".format(sended))
                receiveLabelText.set("NAK: " + str(sended))
                self.tk.update()
                time.sleep(0.4)
                packet = self.channelModel.addGilbertNoise(self.sourcePackages[sended])
            receiveLabelText.set("ACK: " + str(sended))
            self.tk.update()
            time.sleep(0.1)
            self.destPackages[sended] = packet  # paczka zapisana
            sended += 1