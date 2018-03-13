#Selective Repeat Protocol

from Channel import *

class SelectiveRepeat:
    sourcePackages = [] #pakiety ze zrodla
    destPackages = [] #gotowe "przemielone" pakiety
    ###########################################################
    protocol = None #protocol z funkcja sprawdzajaca poprawnosc IsValid !!!
    ###########################################################
    channelModel = None #model channelu
    window = 0 #ilosc pakietow w oknie tzn. ile na raz pakietow zostanie wyslanych
    errorCounter = 0 #ogolna ilosc NAKów

    def __init__(self,src,chan,prot,win):
        self.sourcePackages = src
        self.channelModel = chan
        self.protocol = prot
        self.window = win
        self.errorCounter = 0

    def getDestinationPackets(self): #zwraca "przerobiony" plik
        return self.destPackages

    def getErrors(self):
        return self.errorCounter

    def transmit(self):   #TRANSMITUJE PAKIETY Z sourcePackages do destPackages
        print("Rozpoczynam transmisje danych")

        buffer = [] # wyslane paczki
        indexes = [] #indeksy paczek
        errorBuf = [] #bufor zlych paczek
        errorIndexes = [] #indeksy zlych paczek

        sended = 0 # ilosc wyslanych pakietow
        packets = len(self.sourcePackages) #ilosc pakietow

        while(sended < packets or len(errorBuf) > 0):  # ! U W A G A JEZELI JEST ZBYT DUZO BLEDOW TO PLIK NIE PRZEJDZIE BO SENDED DOJDZIE DO KONCA A ERRORBUF NIE BEDZIE PUSTY
            print("petla nr {}".format(sended))
            while (len(buffer) < self.window - len(errorBuf) and sended < packets):  #dodajemy do bufora pakiety,
                                                                                     # jezeli byly wczesniej jakies bledy to dodajemy mniej nowych pakietow bo miejsce w buforze zajmuja pakiety ktore trzeba wyslac od nowa
                buffer.append(self.channelModel.addGilbertNoise(self.sourcePackages[sended])) # ZAKLOCANIE
                #buffer.append(self.channelModel.addBSCNoise(self.sourcePackages[sended]))  # ZAKLOCANIE
                indexes.append(sended)
                sended += 1
                #print("dodaje {}".format(sended))

            errors = [] #zbior blednych paczek w jednym oknie bufora

            #ODBIERANIE PAKIETOW
            while (len(buffer) > 0):
                packet = buffer.pop()
                index = indexes.pop()
                if (self.protocol.isValid(packet)): #TUTAJ BEDZIEMY SPRAWDZAC ACK == TRUE, NAK == FALSE
                    #print("\tpaczka prawidlowa")
                    self.destPackages.insert(index,packet)  # paczka zapisana
                else:
                    print("\tpaczka NIEprawidlowa")
                    errors.append(index)  #  dodanie INDEKSU paczki jako bledna
                    self.errorCounter += 1

            while (len(errorBuf) > 0):  # jezeli w glownym buforze z blednymi paczkami sa jakies paczki to nastepuja proba ich wyslania
                packet = errorBuf.pop()
                index = errorIndexes.pop()
                print("Proba wyslania BLEDNYCH pakietow")
                if (self.protocol.isValid(packet)):
                    print("\tpaczka prawidlowa")
                    self.destPackages.insert(index,packet)  # zapisanie paczki
                else:
                    print("\tpaczka NIEprawidlowa")
                    errors.append(index)  # dodanie paczki jako bledna
                    self.errorCounter += 1

            while (len(errors) > 0):  # dodanie paczek do glownego bufora z blednymi paczkami, zostana wyslane w nastepnym kroku petli
                index = errors.pop()
                errorBuf.append(self.channelModel.addGilbertNoise(self.sourcePackages[index])) #dodanie do glownego bufora z blednymi paczkami, pobranymi jeszcze raz z source i zakloconymi
                errorIndexes.append(index)
