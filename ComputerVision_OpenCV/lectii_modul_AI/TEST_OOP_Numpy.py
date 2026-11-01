"""
Ex1
Creează o clasă Student care să gestioneze informațiile despre un student.
Cerințe:
1. Constructorul primește numele, vârsta și media studentului.
2. Creează o metodă prezentare() care afișează informațiile studentului.
3. Creează o metodă este
_promovat() care verifică dacă media este cel puțin 5.
4. Creează două obiecte diferite.
Exemplu de rezultat:
Student: Andrei
Varsta: 21
Media: 8.50
Status: Promovat
Student: Mihai
Varsta: 20
Media: 4.30
Status: Respins
"""

class Student:
    def __init__(self, nume, varsta, media):
        self.nume = nume
        self.varsta = varsta
        self.media = media

    def prezentare(self):
        print(f"Student: {self.nume}")
        print(f"Varsta: {self.varsta}")
        print(f"Media: {self.media:.2f}")
        if self.este_promovat():
            status = "Promovat"
        else:
            status = "Respins"
        print(status)

    def este_promovat(self):
        return self.media >= 5.0

"""
Exercițiul 2 – Cont bancar
Creează o clasă ContBancar care simulează operațiunile unui cont.
Cerințe:
1. Constructorul primește titularul și soldul inițial.
2. Metoda depunere(suma) adaugă bani.
3. Metoda retragere(suma) scade bani.
4. Nu permite retrageri mai mari decât soldul.
5. Nu permite depuneri sau retrageri cu valori negative ori zero.
Exemplu:
Titular: Bogdan
Sold initial: 1000 RON
Depunere: 500 RON
Sold: 1500 RON
Retragere: 300 RON
Sold: 1200 RON
Retragere: 2000 RON
Fonduri insuficiente!
"""
class ContBancar:
    def __init__(self, titular, sold_initial):
        self.titular = titular
        self.sold_initial = sold_initial

    def depune(self, suma):
        if suma > 0:
            self.sold_initial += suma
            print("Depunere:", suma, "RON")
            print("Sold:", self.sold_initial, "RON")
        else:
            print("Suma invalida!")

    def retragere(self, suma):
        if suma <= 0:
            print("Suma invalida!")
        elif suma > self.sold_initial:
            print("Fonduri insuficiente!")
        else:
            self.sold_initial -= suma
            print("Retragere:", suma, "RON")
            print("Sold:", self.sold_initial, "RON")

"""
Exercițiul 3 – Calculator
Creează o clasă Calculator.
Cerințe:
1. Implementează patru metode: adunare, scădere, înmulțire și împărțire.
2. Fiecare metodă primește două numere.
3. Împărțirea la zero trebuie tratată.
4. Afișează rezultatele operațiilor.
Output așteptat, pentru numerele 10 și 5:
Adunare: 15
Scadere: 5
Inmultire: 50
Impartire: 2.0
"""
class Calculator:
    def adunare(self, n1, n2):
        return n1 + n2

    def scadere(self,n1,n2):
        return n1 - n2

    def inmultire(self,n1, n2):
        return n1 * n2

    def impartire(self, n1,n2):
        if n2 == 0:
            raise Exception("Nu poti imparti la 0!")
        return n1/n2

"""
Exercițiul 4 – Sistem de angajați
Creează o clasă Angajat.
Cerințe:
1. Fiecare angajat are nume, funcție și salariu.
2. Creează metoda mareste
salariul(procent).
_
3. Creează metoda afiseaza
detalii().
_
4. Testează o creștere salarială de 10%.
Output:
Angajat: Maria
Functie: Developer
Salariu initial: 5000 RON
Marire salariala: 10%
Salariu nou: 5500 RON
"""
class Angajat:
    def __init__(self, nume, functie, sal):
        self.nume = nume
        self.functie=functie
        self.sal = sal

    def mareste_salariul(self,procent):
        return self.sal * procent / 100 + self.sal

    def afis_detalii(self):
        print(f"Nume: {self.nume}")
        print(f"Functie: {self.functie}")
        print(f"Salariu: {self.sal}")

"""
Exercițiul 5 – Moștenire: Animale
Creează un sistem simplu folosind moștenirea.
Cerințe:
1. Creează clasa Animal.
2. Constructorul primește numele animalului.
3. Creează metoda sunet().
4. Creează clasele Caine și Pisica , care moștenesc Animal.
5. Suprascrie metoda sunet() în fiecare clasă.
Output:
Rex spune: Ham Ham!
Tom spune: Miau!
"""
class Animal:
    def __init__(self, nume):
        self.nume = nume

    def sunet(self):
        print("Animalul scoat un sunet.")

class Caine(Animal):
    def sunet(self):
        print(f"{self.nume} spune: Ham Ham!")

class Pisica(Animal):
    def sunet(self):
        print(f"{self.nume} spune: miaaaau mr")

"""
Exercițiul 6 – Magazin online
Creează clasa Produs.
Cerințe:
1. Fiecare produs are nume, preț și cantitate.
2. Creează metoda valoare
stoc().
_
3. Creează metoda vinde(cantitate).
4. Actualizează stocul după vânzare.
5. Nu permite vânzarea unei cantități mai mari decât stocul.
Output:
Produs: Laptop
Pret: 3000 RON
Stoc initial: 5
Vandute: 2
Stoc ramas: 3
Valoare stoc: 9000 RON
"""
class Produs:
    def __init__(self,nume,pret,cantitate):
        self.nume = nume
        self.pret =pret
        self.cantitate=cantitate

    def val_stoc(self):
        return self.pret * self.cantitate

    def vinde_cantitatea(self, cant_vanduta):
        if self.cantitate >= cant_vanduta:
            self.cantitate -= cant_vanduta
            print(f"Vandute: {cant_vanduta}")
            print(f"Stoc ramas: {self.cantitate}")
        elif cant_vanduta <= 0:
            print("Cantitate invalida.")
        elif self.stoc < cant_vanduta:
            print("Stoc insuficient.")

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
    def __init__(self, titlu, autor, an_publicare):
        self.titlu = titlu
        self.autor = autor
        self.an_publicare = an_publicare
        self.disponibila = True

    def imprumuta(self):
        if self.disponibila:
            self.disponibila = False
            print("imprumut ok")

    def returneaza(self):
        if not self.disponibila:
            self.disponibila = True
            print("carte returnata!")
        else:
            print("Cartea era deja disponibila.")

"""
Exercițiul 8 – Sistem de autentificare
Creează o clasă Utilizator.
Cerințe:
1. Constructorul primește username și parolă.
2. Creează metoda autentificare(username, parola).
3. Verifică dacă datele introduse sunt corecte.
4. Returnează True sau False.
5. Afișează un mesaj corespunzător.
Output:
Username: admin
Password: 1234
Autentificare reusita!
Username: admin
Password: gresit
Date incorecte!
Notă: parolele în clar sunt acceptate doar pentru acest 
exercițiu introductiv, nu într-o aplicație reală.
"""
class Utilizator:
    def __init__(self,utilizator, parola):
        self.utilizator =utilizator
        self.utilizator =parola

    def autentificare(self,username,parola):
        if username == self.utilizator and parola == self.parola:
            print("Username si parola ok!")
            return True
        else:
            print("Username sau parola incorecta!")
            return False

"""
PARTEA a II-a – NUMPY
Toate exercițiile se rezolvă folosind funcții NumPy, nu bucle scrise manual,
 acolo unde este posibil.
Exercițiul 9 – Analiza temperaturilor
Ai următoarele temperaturi înregistrate într-o săptămână:
[22, 25, 19, 30, 28, 24, 21]
Cerințe:
1. Creează un array NumPy.
2. Calculează temperatura medie.
3. Identifică temperatura maximă.
4. Identifică temperatura minimă.
5. Numără zilele cu temperaturi peste 24°C.
Output:
Temperatura medie: 24.14
Temperatura maxima: 30
Temperatura minima: 19
Zile peste 24 grade: 3
"""
import numpy as np

#task9
class Temperatura:
    def __init__(self, temperaturi: list):
        self.temperaturi = np.array(temperaturi)

    def temperatura_medie(self):
        return np.mean(self.temperaturi)

    def temperatura_minima(self):
        return np.min(self.temperaturi)

    def temperatura_maxima(self):
        return np.max(self.temperaturi)

    def zile_cu_temp_peste(self, temperatura_cautata):
        return np.sum(self.temperaturi > temperatura_cautata)

"""
Exercițiul 10 – Analiza notelor
Primești următoarele note:
[10, 8, 7, 4, 9, 5, 3, 10]
Cerințe:
1. Transformă lista într-un array NumPy.
2. Calculează media notelor.
3. Numără elevii promovați (nota ≥ 5).
4. Numără elevii respinși.
5. Identifică cea mai mare notă.
Output:
Media: 7.0
Promovati: 6
Respinsi: 2
Nota maxima: 10
"""
class Nota:
    def __init__(self, note:list):
        self.note = np.array(note)

    def medie_note(self):
        return np.mean(self.note)

    def elevi_promovati(self):
        return np.sum(self.note >= 5)

    def elevi_respinsi(self):
        return np.sum(self.note < 5)

    def nota_maxima(self):
        return np.max(self.note)

"""
Exercițiul 11 – Matrice 3×3
Creează următoarea matrice folosind NumPy:
1 2 3
4 5 6
7 8 9
Cerințe:
1. Afișează matricea.
2. Calculează suma tuturor elementelor.
3. Calculează suma fiecărui rând.
4. Calculează suma fiecărei coloane.
5. Afișează elementul central.
Output:
Suma totala: 45
Sume randuri: [6, 15, 24]
Sume coloane: [12, 15, 18]
Element central: 5
"""
class Matrice:
    def __init__(self, matrice_data: list):
        self.matrice = np.array(matrice_data)

    def suma_elem(self):
        return np.sum(self.matrice)

    def suma_pe_randuri(self):
        suma_randuri = np.sum(self.matrice, axis=1)
        return suma_randuri

    def suma_coloane(self):
        return np.sum(self.matrice, axis=0)

    def element_central(self):
        randuri = self.matrice.shape[0]
        coloane = self.matrice.shape[1]

        elemente = []

        for i in range(randuri):
            for j in range(coloane):
                if (i == randuri // 2 or (randuri % 2 == 0 and i == randuri // 2 - 1)):
                    if (j == coloane // 2 or (coloane % 2 == 0 and j == coloane // 2 - 1)):
                        elemente.append(self.matrice[i][j])

        if len(elemente) == 1:
            return elemente[0]
        else:
            return elemente

"""
Exercițiul 13 – Analiza vânzărilor
Un magazin a înregistrat următoarele vânzări zilnice:
[150, 200, 175, 300, 250, 400, 225]
Cerințe:
1. Calculează vânzările totale.
2. Calculează media zilnică.
3. Identifică ziua cu cele mai mari vânzări.
4. Calculează câte zile au depășit media.
5. Crește toate vânzările cu 10%.
Output parțial:
Vanzari totale: 1700
Media zilnica: 242.86
Ziua cu vanzari maxime: 6
Zile peste medie: 3
Consideră prima zi ca fiind ziua 1.
"""
#task13
class Vanzari:
    def __init__(self, vanzari: list):
        self.vanzari = np.array(vanzari)

    def vanzari_totale(self):
        return np.sum(self.vanzari)

    def media_zilnica(self):
        return np.mean(self.vanzari)

    def ziua_vanzari_maxime(self):
        return np.argmax(self.vanzari) + 1

    def zile_peste_medie(self):
        return np.sum(self.vanzari > np.mean(self.vanzari))

    def crestere_vanzari(self, procent):
        self.vanzari = self.vanzari * (1 + procent / 100)
        return self.vanzari


if __name__ == "__main__":
    #task1
    s1 = Student("Andrei", 21, 8.5)
    s2 = Student("Mihai", 20, 4.3)

    print("---------task1")
    s1.prezentare()
    s2.prezentare()

    #task2
    cont = ContBancar("Bogdan", 1000)

    print("---------task2")
    print("Titular:", cont.titular)
    print("Sold initial:", cont.sold_initial, "RON")

    cont.depune(500)
    cont.retragere(300)
    cont.retragere(2000)

    print("---------task3")
    c = Calculator()
    n1 = 10
    n2 = 5
    print(f"Adunare: {c.adunare(n1,n2)}")
    print(f"Scadere: {c.scadere(n1,n2)}")
    print(f"Inmultire: {c.inmultire(n1,n2)}")
    print(f"Impartire: {c.impartire(n1,n2)}")

    print("-------------task4")
    angajat = Angajat("Maria", "Developer", 5000)

    angajat.afis_detalii()

    sal_marit = angajat.mareste_salariul(10)

    print("Marire salariala: 10%")
    print(f"Salariu nou: {sal_marit} RON")

    print("---------------task5")
    caine = Caine("Rex")
    pisica = Pisica("Tom")

    caine.sunet()
    pisica.sunet()

    print("------task 6")
        #task6
    produs = Produs("Laptop", 3000, 5)

    print("---------task6")
    print(f"Produs: {produs.nume}")
    print(f"Pret: {produs.pret} RON")
    print(f"Stoc initial: {produs.cantitate}")

    produs.vinde_cantitatea(2)

    print(f"Valoare stoc: {produs.val_stoc()} RON")


    #task7
    carte = Carte("Python Basics", "John Smith", 2020)

    print("---------task7")
    print(f"Carte: {carte.titlu}")
    print(f"Autor: {carte.autor}")

    carte.imprumuta()
    carte.imprumuta()
    carte.returneaza()

    #task 8
    print("--------task8")
    u = Utilizator("admin", "1234")
    user = input("Introdu utilizatorul: ")
    password = input("Introdu parola: ")
    u.autentificare(user, password)
    if user=="admin" and password=="1234":
        print("Autentificare reusita!")
    else:
        print("User sau parola gresita.")

    #task9
    temp = Temperatura([22, 25, 19, 30, 28, 24, 21])

    print("---------task9")
    print(f"Temperatura medie: {temp.temperatura_medie():.2f}")
    print(f"Temperatura maxima: {temp.temperatura_maxima()}")
    print(f"Temperatura minima: {temp.temperatura_minima()}")
    print(f"Zile peste 24 grade: {temp.zile_cu_temp_peste(24)}")

    #task10
    print("--------10")
    note = Nota([10, 9, 5, 4, 3, 9.6, 8])
    print(f"Nota cea mai mare: {note.nota_maxima()}")
    print(f"Numar elevi respinsi: {note.elevi_respinsi()}")
    print(f"Numar elevi promovati: {note.elevi_promovati()}")
    print(f"Media notelor: {note.medie_note()}")

    #task11
    print("---------task11")

    m = Matrice([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])

    print(f"Matricea:\n{m.matrice}")
    print(f"Suma totala: {m.suma_elem()}")
    print(f"Sume randuri: {m.suma_pe_randuri()}")
    print(f"Sume coloane: {m.suma_coloane()}")
    print(f"Element central: {m.element_central()}")

    """
Exercițiul 12 – Filtrarea numerelor
Ai array-ul:
[12, 5, 18, 7, 25, 3, 30, 9]
Cerințe:
1. Selectează numerele mai mari decât 10.
2. Selectează numerele pare.
3. Calculează suma numerelor pare.
4. Înlocuiește toate valorile mai mici decât 10 cu zero.
Output:
Mai mari decat 10: [12, 18, 25, 30]
Numere pare: [12, 18, 30]
Suma numerelor pare: 60
Array modificat:
[12, 0, 18, 0, 25, 0, 30, 0]
"""
    #task12
    print("---------task12")

    numere = np.array([12, 5, 18, 7, 25, 3, 30, 9])

    print(f"Mai mari decat 10: {numere[numere > 10]}")
    print(f"Numere pare: {numere[numere % 2 == 0]}")
    print(f"Suma numerelor pare: {np.sum(numere[numere % 2 == 0])}")

    numere[numere < 10] = 0
    print(f"Array modificat: {numere}")


    #task13
    print("---------task13")

    v = Vanzari([150, 200, 175, 300, 250, 400, 225])

    print(f"Vanzari totale: {v.vanzari_totale()}")
    print(f"Media zilnica: {v.media_zilnica():.2f}")
    print(f"Ziua cu vanzari maxime: {v.ziua_vanzari_maxime()}")
    print(f"Zile peste medie: {v.zile_peste_medie()}")
    print(f"Vanzari dupa crestere: {v.crestere_vanzari(10)}")

    """
Exercițiul 14 – Imagine artificială cu NumPy
Creează o matrice NumPy care simulează o imagine alb-negru de 5×5 pixeli.
Cerințe:
1. Creează o matrice de 5×5 cu toate valorile zero.
2. Modifică pixelul central la valoarea 255.
3. Modifică prima linie astfel încât toți pixelii să aibă valoarea 100.
4. Calculează media valorilor din matrice.
5. Afișează matricea finală.
Output:
[[100 100 100 100 100]
[ 0 0 0 0 0]
[ 0 0 255 0 0]
[ 0 0 0 0 0]
[ 0 0 0 0 0]]
Media pixelilor: 30.2
"""
    # #task14
    # heightmap = Matrice([
    #     [0,0,0,0,0],
    #     [0,0,0,0,0],
    #     [0,0,0,0,0],
    #     [0,0,0,0,0],
    #     [0,0,0,0,0]
    # ])

    # print(f"Element central initial: {heightmap.element_central()}")

    # heightmap.matrice[2][2] = 255
    # heightmap.matrice[0] = 100

    # print(heightmap.matrice)
    # print(f"Media pixelilor: {np.mean(heightmap.matrice)}")