class CardFidelitate:
    def __init__(self, nume_client):
        #crearea unui card de fidelitate pentru un client
        self.nume_client = nume_client
        self.sold_puncte = 0
        self.puncte_utilizate = 0
        self.istoric_puncte = []

    def calculeaza_puncte(self, valoare_cumparatura):
        #calculeaza punctele obtinute la o cumparatura
        #se acorda 1 punct pentru fiecare 10 lei cheltuiti
        if valoare_cumparatura <= 0:
            return 0

        puncte_obtinute = int(valoare_cumparatura / 10)

        return puncte_obtinute

    def adauga_puncte(self, valoare_cumparatura):
        #calculeaza si adauga automat punctele in sold
        puncte_obtinute = self.calculeaza_puncte(valoare_cumparatura)

        self.sold_puncte += puncte_obtinute

        mesaj = f"Cumparatura de {valoare_cumparatura} lei: +{puncte_obtinute} puncte. Sold actual: {self.sold_puncte} puncte."

        self.istoric_puncte.append(mesaj)

        print(puncte_obtinute, 
              "puncte au fost adaugate in cardul de fidelitate pentru cumparatura de ",
                valoare_cumparatura,
                "lei.")

        return puncte_obtinute

    def verifica_puncte(self, puncte):
        #verfic daca exista suficiente puncte in sold
        return puncte > 0 and puncte <= self.sold_puncte

    def calculeaza_reducere(self, puncte):
        #calc reducerea: 100 de puncte valoreaza 5 lei
        if puncte <= 0:
            return 0

        reducere = puncte / 100 * 5

        return reducere

    def foloseste_puncte(self, puncte):
        #foloseste pct disponibile si returneaza reducerea

        if puncte < 0:
            print("Numarul de puncte trebuie sa fie pozitiv.")
            return 0

        if self.verifica_puncte(puncte):
            reducere = self.calculeaza_reducere(puncte)
            self.sold_puncte -= puncte
            self.puncte_utilizate += puncte

            mesaj = f"Au fost utilizate {puncte} puncte. Reducere: {reducere} lei. Sold actual: {self.sold_puncte} puncte."

            self.istoric_puncte.append(mesaj)

            print(puncte, "puncte au fost utilizate.")
            print("Reducere obtinuta: ", reducere, "lei.")

            return reducere
        else:
            print("Nu exista suficiente puncte in cardul de fidelitate.")
            print("Sold actual: ", self.sold_puncte, "puncte.")
            return 0

    def reseteaza_puncte_utilizate(self):
        #reseteaza evidenta punctelor utilizate
        #soldul pct disponibile nu e afectat
        self.puncte_utilizate = 0

        self.istoric_puncte.append("Evidenta punctelor utilizate a fost resetata.")

        print("Punctele utilizate au fost resetate. Soldul actual de puncte disponibile: ", self.sold_puncte, "puncte.")

    def afiseaza_sold(self):
        #afiseaza soldul curent al cardului
        print("Client: ", self.nume_client)
        print("Sold actual: ", self.sold_puncte, "puncte.")
        print("Puncte utilizate: ", self.puncte_utilizate, "puncte.")

    def afiseaza_istoric(self):
        #afiseaza istoricul tranzactiilor cu puncte
        print("Istoric tranzactii pentru clientul: ", self.nume_client)

        if len(self.istoric_puncte) == 0:
            print("Nu exista tranzactii in istoric.")
        else:
            for tranzactie in self.istoric_puncte:
                print(tranzactie)

if __name__ == "__main__":
    #creez cardul de fidelitate
    card = CardFidelitate("Victoria")

    print("Card de fidelitate creat pentru clientul: ", card.nume_client)

    #Scenariul 1 => cump valida
    valoare_cumparatura = 1250
    print("\nScenariul 1: Cumpărătura validă de ", valoare_cumparatura, "lei.")
    card.adauga_puncte(valoare_cumparatura)
    card.afiseaza_sold()

    #Scenariul 2 => a doua cumparatura
    valoare_cumparatura = 800
    print("\nScenariul 2: A doua cumpărătura de ", valoare_cumparatura, "lei.")
    card.adauga_puncte(valoare_cumparatura)
    card.afiseaza_sold()

    #Scenariul 3 => folosirea unui nr prea mare de puncte
    puncte_dorite = 500
    print("\nScenariul 3: Folosirea unui număr prea mare de puncte: ", puncte_dorite)
    card.foloseste_puncte(puncte_dorite)
    card.afiseaza_sold()

    #Scenariul 4 => folosirea unui nr valid de puncte
    puncte_dorite = 50
    print("\nScenariul 4: Folosirea unui număr valid de puncte: ", puncte_dorite)
    card.foloseste_puncte(puncte_dorite)
    card.afiseaza_sold()

    #Scenariul 5 => cumparatura invalida
    valoare_cumparatura = -100
    print("\nScenariul 5: Cumpărătura invalidă de ", valoare_cumparatura, "lei.")
    puncte = card.adauga_puncte(valoare_cumparatura)

    if puncte == 0:
        print("Valoarea cumparaturii este invalidă. Nu s-au adăugat puncte în cardul de fidelitate.")

    #Afisez istoricul punctelor
    card.afiseaza_istoric()

    #Resetez evidenta punctelor utilizate
    print("\nResetarea evidenței punctelor utilizate.")
    card.reseteaza_puncte_utilizate()
    card.afiseaza_sold()
    card.afiseaza_istoric()


    print("\nProgram finalizat")

