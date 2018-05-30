#Stop And Wait Protocol

from Channel import *
from TMR import *
from tkinter import *

class StopAndWaitGUI:
    sourcePackages = [] #pakiety ze zrodla
    destPackages = [] #gotowe "przemielone" pakiety
    ###########################################################
    protocol = None #protocol z funkcja sprawdzajaca poprawnosc IsValid !!!
    ###########################################################
    channelModel = None #model channelu
    errorCounter = 0 #ogolna ilosc NAKów

    def __init__(self, src, chan, prot, isBSC, tk):
        self.sourcePackages = src
        self.channelModel = chan
        self.protocol = prot
        self.isBSC = isBSC
        self.errorCounter = 0
        self.countOfRelay = 0
        self.tk = tk
        self.waitForNextStep = True
        self.isWindowDestroyed = False

    def getDestinationPackets(self): #zwraca "przerobiony" plik
        return self.destPackages

    def getErrors(self):
        return self.errorCounter

    def _nextStep(self):
        self.waitForNextStep = False

    def _delete_window(self):
        self.window.destroy()
        self.isWindowDestroyed = True
        self.waitForNextStep = False

    def transmit(self):   #TRANSMITUJE PAKIETY Z sourcePackages do destPackages

        # Ustawienie GUI
        self.window = Toplevel(self.tk)
        self.window.protocol("WM_DELETE_WINDOW", self._delete_window)
        canvas = Canvas(self.window, width=300, height=300, bg="#429bf4")
        canvas.pack()
        self.window.title("Stop and Wait")

        strLab = "Count of package to send: " + str(len(self.sourcePackages))
        countPackage = Label(canvas, text=strLab)
        canvas.create_window(100, 20, window=countPackage)

        packetLabelText = StringVar()
        packetLabel = Label(canvas, textvariable=packetLabelText)
        canvas.create_window(70, 60, window=packetLabel)

        buttonWaitForNextStep = Button(canvas, text="NEXT STEP", command=self._nextStep)
        buttonWaitForNextStep.configure(width=40, height=3)
        canvas.create_window(150, 150, window=buttonWaitForNextStep)

        #buttonFasterSlower = Button(canvas, text="AUTO / MANUAL", command=self._faster)
        #buttonFasterSlower.configure(width=40, height=3)
        #canvas.create_window(150, 200, window=buttonFasterSlower)

        canvas.update()

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

            # Show nr of package
            packetLabelText.set("Nr package to send: " + str(sended))
            while(self.waitForNextStep):
                canvas.update()

            if(self.isWindowDestroyed == False):
                self.waitForNextStep = True
            canvas.update()

            # ZAKLOCANIE
            if (self.isBSC):
                packet = self.channelModel.addBSCNoise(self.sourcePackages[sended])
            else:
                packet = self.channelModel.addGilbertNoise(self.sourcePackages[sended])

            #ODBIERANIE PAKIETOW
            #TMR
            while (self.protocol.isValid(packet) == False): # Sprawdzenie odkodowanego tymczasowo pakietu z TMR
                #TUTAJ BEDZIEMY SPRAWDZAC ACK == TRUE, NAK == FALSE
                self.errorCounter += 1

                print("\twysylanie pakietu {}".format(sended))
                packetLabelText.set("NAK: " + str(sended))

                # SHOW IF IT IS NAK
                while (self.waitForNextStep):
                    canvas.update()

                if (self.isWindowDestroyed == False):
                    self.waitForNextStep = True
                canvas.update()

                # Show resend
                packetLabelText.set("Resend package to send: " + str(sended))
                while (self.waitForNextStep):
                    canvas.update()

                if (self.isWindowDestroyed == False):
                    self.waitForNextStep = True
                canvas.update()

                # Ponowne zaklocenie poprawnego pakietu. "Retransmisja uszkodzonego pakietu"
                if (self.isBSC):
                    packet = self.channelModel.addBSCNoise(self.sourcePackages[sended])
                else:
                    packet = self.channelModel.addGilbertNoise(self.sourcePackages[sended])

                self.countOfRelay += 1

            packetLabelText.set("ACK: " + str(sended))

            # SHOW IF IT IS ACK
            while (self.waitForNextStep):
                canvas.update()

            if (self.isWindowDestroyed == False):
                self.waitForNextStep = True
            canvas.update()

            self.destPackages[sended] = packet  # paczka zapisana poprawnie odebranych danych (moga byc uszkodzenia)
            sended += 1

        print("Ilosc retranmisji: " + str(self.countOfRelay))
