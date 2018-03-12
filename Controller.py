from Transmiter import *
from Receiver import *


#zarzadza watkami.
class Controller:

    #https://www.tutorialspoint.com/python/python_multithreading.htm

    def runThreads(self):
        self.threadTransmiter = Transmiter(1, "TRANS", 5, 1, self)
        self.threadReceiver = Receiver(1, "REC", 2, 2)

        self.threadTransmiter.start()
        self.threadReceiver.start()

        #JAKIES METODY DO OBSLUGI TYCH WATKOW

    def printNIC(self):
        print("NIC")
        self.threadReceiver.printNICREC()

controller = Controller()

print("START THREADS")
controller.runThreads()
