class ByteConverter:

    def toByteList(self, bitList):
        byteList = []
        counter = 0
        byte = []
        for bit in bitList:
            byte.append(bit)    # generuje bajt

            counter += 1
            if(counter == 8):
                byteList.append(''.join(byte))  # Dla każdego odczytanego bajtu, dodaje go do listy
                byte.clear()
                counter = 0

        return byteList

    def toBitList(self, byteList):
        bitList = []

        for byte in byteList:
            for i in range(0, 8):
                bitList.append(byte[i]) # Z każdego bajtu są wyciągane bity, ktore nastepnie są wkladane do listy bitow

        return bitList
