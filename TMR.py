class TMR:

    # Bierze bit z listy i następnie go powiela 3 razy. Dodaje do nowej listy, którą na koniec zwraca
    def codeTMR(self, bitList):
        codedBitList = []
        for bit in bitList:
            for i in range(0, 3):
                codedBitList.append(bit)

        return codedBitList

    # funkcja dekodera
    def decodeTMR(self, bitList):
        decodedBitList = []
        count = 0
        amount = 0
        for bit in bitList:
            if(bit == '1'): # Liczy ilosc jedynek
                amount += 1

            count += 1
            if(count == 3): # Po każdych 3 zliczonych bitach, sprawdza co powinno zostac odczytane
                if(amount >= 2):
                    decodedBitList.append('1')
                else:
                    decodedBitList.append('0')
                    amount = 0
                count = 0

        return decodedBitList   # zwraca odkodowaną liste