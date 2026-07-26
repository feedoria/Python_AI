#Sistem de tranzactii

class Client:
    def __init__(self,nume):
        self.nume = nume
        self.tranzactii = []

class Tranzactie:
    def __init__(self, produs,cantitate, pret):
        self.produs = produs
        self.cantitate = cantitate
        self.pret = pret 
        self.total = cantitate * pret 


class TransactionRepository:
    def __init__(self):
        #Lista tuturor tranzactiilor 
        self.lista = []
    def salveaza(self, tranzactie):
        #Adaugam tranzactia in lista 
        self.lista.append(tranzactie)

        print("Tranzactia a fost salvata cu succes")


#Cream clientul
client = Client("Irina")
print("Client creat: ",client.nume)
#Cream Repo
repo = TransactionRepository()
print("Repository creat.")

produs = "Laptop"
cantitate = 20
pret = 3000
print("\nProdus ales: ", produs)
print("Cantitate: ", cantitate)
print("Pret ", pret, "lei")

#Verificam cantitatea 

if cantitate > 0:
    print("\nCantitatea este valida")

    #Salvam tranzactia 
    tranzactie = Tranzactie(produs,cantitate,pret)
    print("Tranzactia a fost creata")

    #Salvam tranzactia 
    repo.salveaza(tranzactie)
    #Asocieam tranzactia clientului
    client.tranzactii.append(tranzactie)
else:
    print("Cantitate invalida")


#Afisam toate tranzactiile 
for t in client.tranzactii:
    print("Client: ", client.nume)
    print("Produs:", t.produs)
    print("Cantitate:", t.cantitate)
    print("Pret",t.pret, "Lei")
    print("Valoare totala: ", t.total, "Lei")

print("Numar tranzactii: ", len(client.tranzactii))
print("Program terminat cu final")