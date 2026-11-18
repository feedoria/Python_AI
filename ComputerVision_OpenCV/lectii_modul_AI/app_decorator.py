# def decorador_politicos(functie_originala):
#     def functie_ambalata():
#         print("[Paznic]:Buna ziua Pregatim sistemul")
    
#         functie_originala() # --> afiseaza_curs sau afiseazA_curs_java 
#         print("[Paznic]:La revedere ma duc acasa functie finalizata")
#         # print("Toata lumea e fericita am invata ceva nou")
#     return functie_ambalata


# @decorador_politicos
# def afiseaza_curs():
#     print("Invatam cum functioneaza Python la nivel de baza")

# @decorador_politicos
# def afiseaza_curs_java():
#     print("Astazi invatam cursul de java")


# @decorador_politicos
# def afiseaza_curs_c():
#     print("Am invatat cursul de c")




# afiseaza_curs()
# afiseaza_curs_java()
# print("===========================================================")
# afiseaza_curs_c()




# def logheaza_actiunea(astea_sunt_metodele_def):
#     def functie_cu_jurnal():
#         print("[Jurnal]:S-a detectat o cerere de rulare a unei functii critice")
#         astea_sunt_metodele_def()
#         print("[Jurnal]:Actiunea s-a incheiat si a fost salvata in arhiva\n")
#     return functie_cu_jurnal



# @logheaza_actiunea
# def ruleaza_scanner():
#     print("Se scaneaza fisierele din directorul principal\n")

# ruleaza_scanner()


# import time

# def masoara_timpul(functie_originala):
#     def functie_cu_cronometru():
#         inceput = time.time()
#         functie_originala()
#         sfarsit = time.time()

#         print(f"Functia a rulat in {sfarsit - inceput:.4f} secunde.\n")

#     return functie_cu_cronometru


# @masoara_timpul
# def descarca_fisier():
#     print("Descarc fisierele de pe Torrent")
#     time.sleep(4)
#     print("Descarcarea e gata")
#     time.sleep(2)

# descarca_fisier()


# import time 

# def cere_autentificare(functie_originala):
#     def functie_verificata():
#         print("Se verifica daca esti logat in cont")

#         utilizator_logat = True

#         if utilizator_logat:
#             print("Utilizator autentificat cu succes!")
#             functie_originala()
#         else:
#             print("Trebuie sa te loghezi mai intai")
#     return functie_verificata

# @cere_autentificare
# def schimba_parola():
#     print("Parola a fost schimbata cu succes")

# schimba_parola()

# def logheaza_modificare(functie_originala):
#     def functie_modificata():
#         print("S-a initiat o modificare pe cont")
#         functie_originala()
#         print("Modificarea a fost salvata cu succes!")

#     return functie_modificata

# @logheaza_modificare
# def actualizeaza_profil():
#     print("Numele si adresa de email au fost modificate")


# actualizeaza_profil()

# def verificare_starea_contului(functia_originala):
#     def functie_verificata():
#         cont_activ = True

#         if cont_activ:
#             print("Verificare... Contul este activ si curat")
#             functia_originala()
#         else:
            
#             print("Eroare contul tau este blocat din motive de securitate")
#             print("Nu se poate efectua nicio tranzactie")
            
#     return functie_verificata

# @verificare_starea_contului
# def retrage_bani():
#     print("Ai retras cu succes 500 de lei din bancomat.ia Lovelele ")

# retrage_bani()
            


def verificare_statut_vip(functie_originala):
    def functie_verificata():
        client_este_vip = bool(input("Esti client de-al bun sau nu?"))

        if client_este_vip == True:
            print("VIP ACCES: Esti cel mai tare ca ai achizionat de la noi bravo!")
            functie_originala()
        else:
            print("Acces Restrictionat:Aceasta operatiune este disponibila doar pentru clientii VIP")
    return functie_verificata



def intrare_lounge_aeroport():
    print("VIP ACCES: Bun venit, client de elita Procesam cererea")
    print("Ai primit acces gratuit la salonul vip din aeroport. Cafeaua e din partea bancii")
    print("Acces Restrictionat:Aceasta operatiune este disponibila doar pentru clientii VIP")



intrare_lounge_aeroport()


def retragere_numerar_militar():
    print("VIP ACCES: Bun venit, client de elita Procesam cererea")
    print("Ai retras 50.000 de lei de la bancomat fara niciun comision")
    print("Acces Restrictionat:Aceasta operatiune este disponibila doar pentru clientii VIP")


retragere_numerar_militar()

@verificare_statut_vip
def apeleaza_consultat_personal():
    print("Te-am conecat cu un mare bacnher smardoi")

apeleaza_consultat_personal()