import threading
import time
#from Controller import controller

class Transmiter (threading.Thread):
    def __init__(self, threadID, name, counter, delay, controller):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.delay = delay
        self.controller = controller

    def run(self):
        print("Starting Transmiter" + self.name)

        #Metoda ktora powinna byc w petli
        self.print_time(self.name, self.counter, self.delay)


        print("Exiting Transmiter" + self.name)


    def print_time(self, threadName, counter, delay):
        while counter:
            #if exitFlag:
            #    threadName.exit()
            time.sleep(delay)
            print("Transmiter: ", threadName, time.ctime(time.time()))
            self.controller.printNIC()
            counter -= 1
