"""
Cerință
Creează un singur decorator numit @verifica_securitate pe care să îl aplici 
la 4 funcții diferite.

Decoratorul trebuie să:
1. Întrebe utilizatorul dacă are contul activ.
2. Dacă răspunsul este "da", să afișeze mesajul "SECURITATE: 
Acces autorizat!" și să execute funcția.
3. Dacă răspunsul este "nu", să afișeze "ACCES RESPINS: Contul este blocat!"
 și să nu execute funcția.
4. La finalul fiecărei operațiuni autorizate, să afișeze "Operațiunea a fost
 înregistrată în sistemul băncii."
Cele 4 funcții pe care trebuie să le creezi
- retrage_bani() – Afișează că utilizatorul a retras 1.000 lei.
- transfera_bani() – Afișează că utilizatorul a transferat 5.000 lei către 
alt cont.
- verifica_sold() – Afișează că utilizatorul are un sold de 25.000 lei.
- schimba_pin() – Afișează că PIN-ul cardului a fost schimbat cu succes.
Regulă obligatorie: Toate cele 4 funcții trebuie să folosească același 
decorator, fără să copiezi codul de verificare în fiecare funcție.
"""

def verifica_securitate(functie_originala):
    def functie_verificata():
        raspuns = input("Aveti cont activ? (da/nu)")

        if raspuns == "da":
            print("SECURITATE: Acces autorizat!")
            functie_originala()
            print("Operatiunea a fost înregistrata în sistemul bancii.")
        elif raspuns == "nu":
            print("ACCES RESPINS: Contul este blocat!")

    return functie_verificata

@verifica_securitate
def retrage_bani():
    print("Ati retras 1.000 lei.")


@verifica_securitate
def transfera_bani():
    print("Ati transferat 5.000 lei către alt cont.")


@verifica_securitate
def verifica_sold():
    print("Soldul dumneavoastră este de 25.000 lei.")


@verifica_securitate
def schimba_pin():
    print("PIN-ul cardului a fost schimbat cu succes.")

retrage_bani()
transfera_bani()
verifica_sold()
schimba_pin()