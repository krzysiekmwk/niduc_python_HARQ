import threading
import time

class Receiver (threading.Thread):
    def __init__(self, threadID, name, counter, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.delay = delay

    def run(self):
        print("Starting Receiver" + self.name)

        #Metoda ktora powinna byc w petli
        self.print_time(self.name, self.counter, self.delay)


        print("Exiting Receiver" + self.name)


    def print_time(self, threadName, counter, delay):
        while counter:
            #if exitFlag:
            #    threadName.exit()
            time.sleep(delay)
            print("Receiver: ", threadName, time.ctime(time.time()))
            counter -= 1

    def printNICREC(self):
        print("NIC REC")