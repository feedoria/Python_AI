"""
Exercițiul 7 – Biblioteca
Creează o clasă Carte.
Cerințe:
1. Constructorul primește titlul, autorul și anul publicării.
2. Adaugă un atribut care indică dacă o carte este disponibilă.
3. Creează metoda imprumuta().
4. Creează metoda returneaza().
5. O carte deja împrumutată nu poate fi împrumutată din nou.
Output:
Carte: Python Basics
Autor: John Smith
Imprumut realizat!
Cartea nu este disponibila!
Carte returnata!
"""
class Carte:
    def __init__(self, titlu, autor, an):
        self.titlu = titlu
        self.autor = autor
        self.an = an
        self.disponibila = True

    def imprumut(self):
        if self.disponibila:
            self.disponibila = False
            print("Cartea a fost imprumutata.")
        else:
            self.disponibila = True
            print("Cartea este disponibila.")

    def returneaza(self):
        if not self.disponibila:
            self.disponibila = True
            print("Carte returnata.")
        else:
            print("Cartea e deja disponibila.")

carte = Carte("Python Basics", "J", 1998)
carte.imprumut()
print("Imprumut realizat")
carte.returneaza()
        