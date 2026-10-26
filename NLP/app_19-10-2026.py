from transformers import pipeline
 
import pandas as pd
 
 
#Proiect de AI helpdesk tichete
 
#Cream modelul care decide categoria fiecarui mesaj
clasificator = pipeline(
    #Spunem AI-ului ca vrem clasificare fara sa antrenam feicare mesaj
    "zero-shot-classification",
    #Alegem modelul antrenat
    model ="facebook/bart-large-mnli"
)
 
#Cream un model care face rezumatul mesajelor
rezumator = pipeline(
    #Spunem ca vrem sa facem rezumate
    "summarization",
 
    #Algeme modelul specializat pe rezumate
    model="facebook/bart-large-cnn"
)
 
#Vreau sa cream o lista cu departamentel firmei
 
categorii = [
    #Probleme cu aplicatia
    "technical support",
 
    #Probleme legate de bani si facturi
    "billing",
 
    #Clientu doreste sa cumpere ceva
    "sales",
 
    #Probleme legate de cont si de autentificare
    "account acces",
    #Probleme legate de HR
    "HR"
 
]
 
#Facem o lista cu tichete
tickete = [
    "I cannot log into my account anymore. I changed my password yesterday but website still says my password is incorrect",
 
    "The cable guy was so rude with me, I want my money back. He fall inb love with my wife",
 
    "I checked my bank account this morning and noticed that your company charget me twice for the same subscription. I will go to ANPC",
 
    "I canceled my subscription last mounth, but you idiots charge my credit card and by the way the application crashes every day, every time",
 
    "Our company needs twenty licenses for your software. I would like to know the price and wheter you offer discounts for business"
]
 
#Facem o lista goala pentru mesajele originale
lista_mesaje = []
 
#Facem o lista goala pentru departamente
lista_departamente = []
 
#Mai facem o lista pentru scoruri
 
lista_scoruri = []
 
#Lista pentru rezumate
 
lista_rezumate = []
 
#Parcutgem fiecare ticket primit
 
for ticket in tickete:
    #Trimitem ticketul catre modelul de clasificare
    rezultat_clasificare = clasificator(
        ticket,
        candidate_labels = categorii
    )
    #Luam categoria cu cel mai mare scor
    departament = rezultat_clasificare["labels"][0]
 
    scor = rezultat_clasificare["scores"][0]
 
    #Trimitem ticketele catre modelul care face rezumate
 
    rezultat_rezumat = rezumator(
        ticket,
 
        #Spunem care e lungimea maxima
        max_length = 35,
 
        min_length = 10,
 
        do_sample = False #Spunem ca nu vrem rezultate aleatorii
    )
 
    #Luam textul rezumat din AI
    rezumat = rezultat_rezumat[0]["summary_text"]
 
    #Adaugam mesajul original in lista
    lista_mesaje.append(ticket)
 
    #Adaugam departamentul in lista
    lista_departamente.append(departament)
 
    #Adaugam scorul in lista
    lista_scoruri.append(scor)
 
    #Adaugam rezumatul in lista
    lista_rezumate.append(rezumat)
 
    print("\n-------------------------------------------")
 
    print("Mesaj client:")
    print(ticket)
 
    #Afisam departamentul
    print("\nDepartamente:", departament)
 
    #Afisam scorul
    print("Scor AI:", round(scor, 2))
 
    print("Rezumat:", rezumat)
 
 
#Dupa toate analizele sa facem un raport final
 
date = {
    "Mesaj":lista_mesaje,
 
    "Departament":lista_departamente,
 
    "Scor":lista_scoruri,
 
    "Rezumat": lista_rezumate
}
tabel = pd.DataFrame(date)
 
print("\n========================== Raport Final ========================== ")
 
print(tabel)