#Selective Repeat Protocol

from Channel import *

class SelectiveRepeat:
    source = None
    destination = None
    channelModel = None
    bytesInPacket = 0
    window = 0
    errorCounter = 0

    def __init__(self,src,dest,chan,bytinpak,win):
        self.source = src
        self.destination = dest
        self.channelModel = chan
        self.bytesInPacket = bytinpak
        self.window = win
        self.errorCounter = 0

    def getErrors(self):
        return self.errorCounter

    def transmit(self, packs): #packs do testów
        print("Rozpoczynam transmisje danych")

        buffer = [] # wyslane paczki
        indexes = [] #indeksy paczek
        errorBuf = [] #bufor zlych paczek
        errorIndexes = [] #indeksy zlych paczek

        sended = 0
        packets = 0 # TUTAJ BEDZIE METODA KTORA ZWROCI ILOSC WSZYSTKICH PAKIETOW
        
        sourcePackages = packs # pakiety zrodlowe TUTAJ BEDZIE METODA KTORA ZWROCI PAKIETY ZRODLOWE
        destPackages = [] # pakiety docelowe

        while(sended < packets):
            print("petla nr {}".format(sended))
            while (len(buffer) < self.window - len(errorBuf) and sended < packets):  #dodajemy do bufora pakiety,
                                                                                     # jezeli byly wczesniej jakies bledy to dodajemy mniej nowych pakietow bo miejsce w buforze zajmuja pakiety ktore trzeba wyslac od nowa
                buffer.append(self.channelModel.addGilbertNoise(sourcePackages[sended])) # ZAKLOCANIE
                indexes.append(sended)
                sended =+ 1

            errors = [] #zbior blednych paczek w jednym oknie bufora

            #ODBIERANIE PAKIETOW
            while (len(buffer) > 0):
                packet = buffer.pop()
                index = indexes.pop()
                if (self.destination.isValid(packet)): #TUTAJ BEDZIEMY SPRAWDZAC ACK == TRUE, NAK == FALSE
                    print("\tpaczka prawidlowa")
                    destPackages[index] = packet  # paczka zapisana
                else:
                    print("\tpaczka NIEprawidlowa")
                    errors.append(index)  #  dodanie INDEKSU paczki jako bledna
                    self.errorCounter += 1
                while (len(errorBuf) > 0):  # jezeli w glownym buforze z blednymi paczkami sa jakies paczki to nastepuja proba ich wyslania
                    packet = errorBuf.pop()
                    index = errorIndexes.pop()
                    print("Proba wyslania BLEDNYCH pakietow")
                    if (self.destination.isValid(packet)):
                        print("\tpaczka prawidlowa")
                        destPackages[index] = packet  # zapisanie paczki
                    else:
                        print("\tpaczka NIEprawidlowa")
                        errors.append(index)  # dodanie paczki jako bledna
                        self.errorCounter += 1

            while (len(errors) > 0):  # dodanie paczek do glownego bufora z blednymi paczkami, zostana wyslane w nastepnym kroku petli
                index = errors.pop()
                errorBuf.append(self.channelModel.addGilbertNoise(sourcePackages[index])) #dodanie do glownego bufora z blednymi paczkami, pobranymi jeszcze raz z source i zakloconymi
                errorIndexes.append(index)

