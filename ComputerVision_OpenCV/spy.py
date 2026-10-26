#Importam opencv pentru camera
import cv2
#Import time pentru cronometrare data si ora la eveniment
import time

#Numele ferestrei, il folosim in mai multe locuri
FEREASTRA = "Monitor de obiecte"

#Alegem camera calculatorului (1 = camera externa)
camera = cv2.VideoCapture(1)

#Daca nu exista a doua camera, incercam camera implicita (0)
if not camera.isOpened():
    camera = cv2.VideoCapture(0)

#Verificam daca s-a deschis camera
if not camera.isOpened():
    print("Nu am putut porni camera. Verifica te rog ")
    raise SystemExit #Raise inseamna ca am oprit programul pentru ca nu avem imagini de analizat



#Setam fereastra la o dimensiune  potrivita
#Le punem cu litere mari pentru a fi evidentiate
LATIME = 960
INALTIME = 540

#Definim zona dreptunghiulara pe masa pe care o vom monitoriza
x1, y1 = 180, 130
x2, y2 = 780, 450

#Lasam 5 secunde pentru masa goala
SECUNDE_CALIBRARE = 5

#Daca schimbarea ramane atat de mult timp, afisam alerta
SECUNDE_PANA_LA_ALERTA = 8

#Diferenta minima de luminozitate ca un pixel sa fie considerat schimbat
PRAG_PIXEL = 30

#Ignoram contururile mai mici de atat (zgomot, umbre mici)
ARIE_MINIMA_CONTUR = 150

#Daca suprafata schimbata depaseste pragul, consideram ca e un obiect in zona
PRAG_SUPRAFATA = 1400

#Culorile sunt in format BGR (albastru, verde, rosu), nu RGB
VERDE = (90, 200, 90)
GALBEN = (0, 220, 255)
PORTOCALIU = (0, 150, 255)
ROSU = (50, 50, 230)
ALB = (255, 255, 255)
GRI = (170, 170, 170)
NEGRU = (0, 0, 0)
FUNDAL_PANOU = (25, 25, 25)

#Fontul folosit pentru toate textele
FONT = cv2.FONT_HERSHEY_SIMPLEX


#Scrie un text cu un contur negru ca sa se vada pe orice fundal
def scrie_text(imagine, mesaj, x, y, marime=0.6, culoare=ALB, grosime=1):
    #Intai textul negru, mai gros, pe post de umbra
    cv2.putText(imagine, mesaj, (x, y), FONT, marime, NEGRU, grosime + 2, cv2.LINE_AA)
    #Apoi textul colorat deasupra
    cv2.putText(imagine, mesaj, (x, y), FONT, marime, culoare, grosime, cv2.LINE_AA)


#Scrie un text centrat in jurul punctului (centru_x, centru_y)
def scrie_centrat(imagine, mesaj, centru_x, centru_y, marime=0.6, culoare=ALB, grosime=1):
    #getTextSize ne spune cat de lat si de inalt va fi textul
    (latime_text, inaltime_text), _ = cv2.getTextSize(mesaj, FONT, marime, grosime)
    #Mutam textul la stanga si in jos cu jumatate din dimensiunea lui
    scrie_text(imagine, mesaj, centru_x - latime_text // 2, centru_y + inaltime_text // 2,
               marime, culoare, grosime)


#Deseneaza un dreptunghi semi-transparent (panou) peste imagine
def panou(imagine, x_st, y_sus, x_dr, y_jos, culoare=FUNDAL_PANOU, opacitate=0.65):
    #Luam bucata din imagine de sub panou
    bucata = imagine[y_sus:y_jos, x_st:x_dr]
    #Facem o copie si o umplem complet cu culoarea panoului
    plin = bucata.copy()
    plin[:] = culoare
    #addWeighted amesteca cele doua imagini: panoul si ce era dedesubt
    imagine[y_sus:y_jos, x_st:x_dr] = cv2.addWeighted(plin, opacitate, bucata, 1 - opacitate, 0)


#Deseneaza doar colturile unui dreptunghi, ca la vizorul unei camere
def colturi(imagine, x_st, y_sus, x_dr, y_jos, culoare, lungime=28, grosime=4):
    #Pentru fiecare colt: pozitia lui si directia in care pleaca liniile
    for x, y, dx, dy in [(x_st, y_sus, 1, 1), (x_dr, y_sus, -1, 1),
                         (x_st, y_jos, 1, -1), (x_dr, y_jos, -1, -1)]:
        #Linia orizontala a coltului
        cv2.line(imagine, (x, y), (x + dx * lungime, y), culoare, grosime, cv2.LINE_AA)
        #Linia verticala a coltului
        cv2.line(imagine, (x, y), (x, y + dy * lungime), culoare, grosime, cv2.LINE_AA)


#Deseneaza o bara de progres; procent este un numar intre 0 si 1
def bara_progres(imagine, x, y, latime, inaltime, procent, culoare):
    #Fundalul gol al barei
    cv2.rectangle(imagine, (x, y), (x + latime, y + inaltime), (60, 60, 60), -1)
    #Partea plina, proportionala cu procentul (il tinem intre 0 si 1)
    umplut = int(latime * min(max(procent, 0), 1))
    if umplut > 0:
        cv2.rectangle(imagine, (x, y), (x + umplut, y + inaltime), culoare, -1)
    #Marginea barei
    cv2.rectangle(imagine, (x, y), (x + latime, y + inaltime), GRI, 1)


#IN ZONA ASTA PASTRAM IMAGINEA INITIALA CU ZONA GOALA
fundal = None

#Pornim cronometrul pentru perioada de calibrare
inceput_calibrare = time.time()

#Memoram cand a aparut prima schimbare
inceput_schimbare = None

#Memoram cand schimbarea a disparut
disparitie_schimbare = None

#retinem daca alerta a fost deja declansata
alerta_pornita = False

#Ora la care a pornit alerta (o afisam pe ecran)
ora_alertei = None

#Numaram cate alerte au fost in total
numar_alerte = 0

#Putem ascunde sau afisa masca alb-negru cu tasta M
arata_masca = True

#Pregatim o fereastra pentru imaginea camerei
cv2.namedWindow(FEREASTRA)

print("Monitorul a pornit. Taste: Q / ESC = iesire, R = recalibrare, M = masca")

#Repetam analiza pana cand utilizatorul apasa Q

while True:

    #Citim o imagine de la camera
    ok, cadru = camera.read()
    if not ok:
        print("Nu mai primim imagini de la camera.")
        break

    #Vreau sa intoarcem imaginea intr-o oglinda
    cadru = cv2.flip(cadru, 1)

    #Redimensionam imaginea ca sa se potriveasca in fereastra
    cadru = cv2.resize(cadru, (LATIME, INALTIME))

    #Luam momentul curent pentru cronometrele programului
    acum = time.time()

    #Convertim cadrul in tonuri gri
    gri = cv2.cvtColor(cadru, cv2.COLOR_BGR2GRAY)

    #Facem imaginea mai uniforma pentru micile detalii
    gri = cv2.GaussianBlur(gri, (21,21),0)

    #Pentru design: intunecam tot ce e in afara zonei, ca zona sa iasa in evidenta
    #Pastram o copie a zonei inainte sa intunecam imaginea
    zona_color = cadru[y1:y2, x1:x2].copy()
    #convertScaleAbs inmulteste fiecare pixel cu alpha (0.5 = de doua ori mai intunecat)
    cadru = cv2.convertScaleAbs(cadru, alpha=0.5)
    #Punem zona inapoi, cu luminozitatea normala
    cadru[y1:y2, x1:x2] = zona_color

    #Daca inca nu avem imagine de referinta, suntem inca in calibrare
    if fundal is None:
        #Calculam cate secunde au mai ramas din calibrare
        ramas = SECUNDE_CALIBRARE-int(acum - inceput_calibrare)

        #In calibrare nu avem inca valori de afisat in panoul din stanga
        stare = "CALIBRARE"
        culoare_stare = GALBEN
        text_suprafata = "-"
        text_durata = "-"

        #Desenam un cadru dreptunghiular in zona mesei sau zona pe care o urmarim
        cv2.rectangle(cadru, (x1,y1), (x2,y2), GALBEN, 1)
        colturi(cadru, x1, y1, x2, y2, GALBEN)

        #Afisam intructiunile de calibrare
        scrie_text(cadru, "Calibrare: lasati masa goala", x1, y1 - 12, 0.6, GALBEN, 2)

        #Afisam numerotarea inversa, mare, in mijlocul zonei
        scrie_centrat(cadru, str(max(0,ramas)), (x1 + x2) // 2, (y1 + y2) // 2, 4, GALBEN, 8)

        #Sub zona aratam cat a avansat calibrarea
        bara_progres(cadru, x1, y2 + 14, x2 - x1, 12,
                     (acum - inceput_calibrare) / SECUNDE_CALIBRARE, GALBEN)
        scrie_text(cadru, "Nu puneti nimic in zona pana se termina numaratoarea",
                   x1, y2 + 46, 0.5, GRI)

        #Dupa calibrare memoram imaginea zonei goale
        #Daca au trecut cele cinci secunde de calibrare
        if acum - inceput_calibrare >= SECUNDE_CALIBRARE:
            #Devine reperul pentru zona goala
            fundal = gri.copy() # copy() creeaza o copie separata a imaginii
            print(f"[{time.strftime('%H:%M:%S')}] Calibrare terminata, incepe monitorizarea")

    #Daca avem imaginea de referinta,putem sa incepem monitorizarea
    else:
        # decupeaza din imagine doar drepunghiul monitorizat,
        #In numpy formatul este in felul urmator imagine[inaltime,latime]
        zona = gri[y1:y2, x1:x2]
        #Decupam aceeasi zona din imaginea salvata in timpul calibrarii
        zona_fundal = fundal[y1:y2, x1:x2]
        #absdiff calculeaza diferenta abosluta dintre imagini
        #Zonele neschimbate o sa fie intunecate, zonele schimbate o sa fie mai luminate
        diferenta = cv2.absdiff(zona_fundal, zona)
        #threshold transforma diferenta intr-o imagine alb-negru
        #Pixelii cu diferenta mai mare de 30 devin albi, iar restul devine negru
        _, masca = cv2.threshold(
            diferenta,
            PRAG_PIXEL,
            255,
            cv2.THRESH_BINARY
        )
        #getStructuringElement creeaza o forma folosita pentru curatarea imagini
        #Morph_rect inseamna ca elementul are o forma dreptunghiulara
        #(5,5) Dimensiunea
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (5,5)
        )
        #morphologyEx aplica o operatie morfologica asupra imaginii (curata)
        #Morph_open elimina punctele albe foarte mici
        masca = cv2.morphologyEx(
            masca,
            cv2.MORPH_OPEN,
            kernel
        )
        #dilate() ingroase zonele albe din masca ca sa le vedem mai clare
        #iteration = 2 aplica operatia de doua ori
        masca = cv2.dilate(
            masca,
            kernel,
            iterations=2
        )
        #FindContours = gaseste marginile din zonele albe
        #RETR_EXTERNAL, = cere doar contururile exterioare
        #CHAIN_APPROX_SIMPLE = pastreaza o versiune mai simplificata a contururilor
        # _ ignora informatiile despre contururi
        contururi, _ = cv2.findContours(
            masca,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        #ContourArea() = calculeaza aria unui contur in pixeli
        #Pastram doar contururile mai mari de 150 de pixeli
        #ca sa ignoram diferentele mici din imagine
        contururi_mari = [
            contur
            for contur in contururi
            if cv2.contourArea(contur) > ARIE_MINIMA_CONTUR
        ]

        #Adunam ariile contururilor ramase
        suprafata_schimbata = sum(cv2.contourArea(contur) for contur in contururi_mari)

        #Daca suprafata schimbata depaseste pragul de 1400 de pixeli
        #Consideram ca exista o schimbare importanta in zona
        schimbare_prezenta = suprafata_schimbata > PRAG_SUPRAFATA
        if schimbare_prezenta:
            #Resetam cronometrul disparitie
            disparitie_schimbare = None
            #Daca aceasta este prima schimbare detectata,
            #pornim cronometrul pentru ea
            if inceput_schimbare is None:
                inceput_schimbare = acum
            #Scadem timpul de inceput din timpul actual ca sa aflam durata
            durata = acum - inceput_schimbare

            #Verificam daca schimbarea a persistat suficient de mult
            if durata >= SECUNDE_PANA_LA_ALERTA:
                #marcam alerta ca pornita
                alerta_pornita = True

                #Salvam ora doar prima data cand porneste alerta
                if ora_alertei is None:
                    ora_alertei = time.strftime("%H:%M:%S")
                    numar_alerte += 1
                    print(f"[{ora_alertei}] ALERTA: un obiect a ramas in zona")
        else:
            #Daca schimbarea a disparut, memoram momentul disparitiei
            if inceput_schimbare is not None and disparitie_schimbare is None:
                #Salvam timpul curent ca sa verificam daca zona a ramas libera
                disparitie_schimbare = acum
            #Asteptam o secunda
            if disparitie_schimbare is not None and acum - disparitie_schimbare > 1:
                if alerta_pornita:
                    print(f"[{time.strftime('%H:%M:%S')}] Zona a redevenit libera")
                inceput_schimbare = None
                disparitie_schimbare = None
                alerta_pornita = False
                ora_alertei = None

        #Cat timp a trecut de cand a aparut schimbarea (0 daca nu e nicio schimbare)
        durata = acum - inceput_schimbare if inceput_schimbare is not None else 0

        #Alegem textul si culoarea starii curente
        if alerta_pornita:
            stare, culoare_stare = "ALERTA", ROSU
        elif inceput_schimbare is not None:
            stare, culoare_stare = "SCHIMBARE", PORTOCALIU
        else:
            stare, culoare_stare = "LIBER", VERDE

        #Valorile pe care le afisam in panoul din stanga
        text_suprafata = f"{int(suprafata_schimbata)} px"
        text_durata = f"{durata:.1f} s"

        #Desenam zona: un contur subtire si colturi groase in culoarea starii
        cv2.rectangle(cadru, (x1,y1), (x2,y2), culoare_stare, 1)
        colturi(cadru, x1, y1, x2, y2, culoare_stare)
        scrie_text(cadru, "ZONA MONITORIZATA", x1, y1 - 12, 0.55, culoare_stare, 1)

        #Incadram fiecare obiect gasit intr-un dreptunghi
        for contur in contururi_mari:
            #boundingRect gaseste cel mai mic dreptunghi care cuprinde conturul
            x, y, w, h = cv2.boundingRect(contur)
            #Coordonatele sunt fata de zona, asa ca adaugam x1 si y1
            cv2.rectangle(cadru, (x1 + x, y1 + y), (x1 + x + w, y1 + y + h), culoare_stare, 2)

        #Bara de progres arata cat mai e pana la alerta
        bara_progres(cadru, x1, y2 + 14, x2 - x1, 12,
                     durata / SECUNDE_PANA_LA_ALERTA, culoare_stare)
        if alerta_pornita:
            mesaj_bara = f"Obiectul este in zona de {int(durata)} s"
        elif inceput_schimbare is not None:
            mesaj_bara = f"Alerta in {max(0, SECUNDE_PANA_LA_ALERTA - durata):.1f} s daca obiectul ramane"
        else:
            mesaj_bara = "Zona este libera"
        scrie_text(cadru, mesaj_bara, x1, y2 + 46, 0.5, GRI)

        #Bannerul rosu de alerta, deasupra zonei
        if alerta_pornita:
            panou(cadru, x1, 56, x2, 100, ROSU, 0.75)
            scrie_centrat(cadru, f"ALERTA! Obiect in zona din {ora_alertei}",
                          (x1 + x2) // 2, 78, 0.7, ALB, 2)

        #Afisam masca alb-negru, micsorata, in coltul din dreapta
        if arata_masca:
            mica = cv2.resize(masca, (160, 85))
            #Masca are un singur canal, cadrul are trei (BGR)
            mica = cv2.cvtColor(mica, cv2.COLOR_GRAY2BGR)
            cadru[70:155, LATIME - 170:LATIME - 10] = mica
            cv2.rectangle(cadru, (LATIME - 171, 69), (LATIME - 10, 155), GRI, 1)
            scrie_text(cadru, "MASCA (M)", LATIME - 170, 62, 0.45, GRI)

    #Bara de sus cu titlul si ceasul
    panou(cadru, 0, 0, LATIME, 50)
    #Un punct colorat care arata starea curenta
    cv2.circle(cadru, (26, 25), 8, culoare_stare, -1, cv2.LINE_AA)
    scrie_text(cadru, "MONITOR DE OBIECTE", 44, 33, 0.75, ALB, 2)
    #Data si ora, aliniate la dreapta
    ceas = time.strftime("%d.%m.%Y  %H:%M:%S")
    (latime_ceas, _), _ = cv2.getTextSize(ceas, FONT, 0.6, 1)
    scrie_text(cadru, ceas, LATIME - latime_ceas - 20, 32, 0.6, GRI)

    #Panoul din stanga cu informatii despre stare
    panou(cadru, 10, 70, 168, 300)
    randuri = [
        ("STARE", stare, culoare_stare),
        ("SUPRAFATA", text_suprafata, ALB),
        ("DURATA", text_durata, ALB),
        ("ALERTE", str(numar_alerte), ALB),
    ]
    for i, (eticheta, valoare, culoare) in enumerate(randuri):
        #Fiecare rand are 55 de pixeli inaltime
        y = 95 + i * 55
        scrie_text(cadru, eticheta, 22, y, 0.45, GRI)
        scrie_text(cadru, valoare, 22, y + 27, 0.7, culoare, 2)

    #Bara de jos cu tastele si setarile
    panou(cadru, 0, INALTIME - 34, LATIME, INALTIME)
    scrie_text(cadru, "Q / ESC - iesire    R - recalibrare    M - masca",
               20, INALTIME - 12, 0.5, GRI)
    setari = f"Alerta dupa {SECUNDE_PANA_LA_ALERTA} s  |  prag {PRAG_SUPRAFATA} px"
    (latime_setari, _), _ = cv2.getTextSize(setari, FONT, 0.5, 1)
    scrie_text(cadru, setari, LATIME - latime_setari - 20, INALTIME - 12, 0.5, GRI)

    #In timpul alertei, marginea ferestrei clipeste rosu (de doua ori pe secunda)
    if alerta_pornita and int(acum * 2) % 2 == 0:
        cv2.rectangle(cadru, (0, 0), (LATIME - 1, INALTIME - 1), ROSU, 8)

    #Afisam imaginea finala in fereastra
    cv2.imshow(FEREASTRA, cadru)

    #waitKey(1) asteapta 1 milisecunda o tasta; & 0xFF pastreaza doar codul tastei
    tasta = cv2.waitKey(1) & 0xFF

    #Q sau ESC (27) opresc programul
    if tasta in (ord("q"), ord("Q"), 27):
        break

    #R porneste din nou calibrarea (de exemplu daca s-a schimbat lumina)
    if tasta in (ord("r"), ord("R")):
        fundal = None
        inceput_calibrare = time.time()
        inceput_schimbare = None
        disparitie_schimbare = None
        alerta_pornita = False
        ora_alertei = None
        print(f"[{time.strftime('%H:%M:%S')}] Recalibrare...")

    #M ascunde sau afiseaza masca
    if tasta in (ord("m"), ord("M")):
        arata_masca = not arata_masca

    #Daca utilizatorul inchide fereastra din X, oprim programul
    if cv2.getWindowProperty(FEREASTRA, cv2.WND_PROP_VISIBLE) < 1:
        break

#Eliberam camera si inchidem ferestrele
camera.release()
cv2.destroyAllWindows()