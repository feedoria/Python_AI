import cv2

from deepface import DeepFace

cale_fata = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

detector_fata = cv2.CascadeClassifier(cale_fata)


cale_zambet = cv2.data.haarcascades + "haarcascade_smile.xml"
detector_zambet = cv2.CascadeClassifier(cale_zambet)

camera = cv2.VideoCapture(1)



#Verificam daca am reusit sa pornim camera
if not camera.isOpened():
    print("Nu am putut porni camera!")
    raise SystemExit


#Pastram ultima emotie detectata, ca sa nu analizam fiecare cadru
emotie = "Se analizeaza..."
cadre = 0

#Scorul emotiei dominante
scor = 0

#Contorul de zambete
numar_zambete = 0
era_fericit = False


traducere = {
    "happy":"fericit",
    "sad":"trist",
    "angry":"furios",
    "tired":"obosit",
    "angst":"anxios",
    "fear":"speriat",
    "disgust":"dezgustat",
    "neutral":"neutru"
}

#Continuam pana cand utilizatorul apasa Q
while True:
    succes,imagine=camera.read()

    #Daca nu am primit imaginea, oprim programul
    if not succes:
        print("Nu am putut citi imaginea de la camera")
        break

    #Numaram cadrele citite
    cadre += 1
    #Convertim imaginea in gri pentru detectarea fetei
    gri = cv2.cvtColor(imagine,cv2.COLOR_BGR2GRAY)

    #Cautam fete in imagine
    fete = detector_fata.detectMultiScale(
        gri,
        scaleFactor=1.1,
        minNeighbors=5, #Adica sa imi gaseasca minim 5 dovezi ca e om (ochi, gura, nas etc)
        minSize=(100,100)
    )

    if len(fete) > 0:
        x,y,latime,inaltime = fete[0]

        #Decupam fata din imagine, ca sa o analizam
        fata_color = imagine[y:y + inaltime, x:x + latime]
        fata_gri = imagine[y:y + inaltime, x:x + latime]

        #Cautam un zambet sau o emotie in zona fetei
        zambete = detector_zambet.detectMultiScale(
            fata_gri,
            scaleFactor=1.7,
            minNeighbors=20,
            minSize=(25,25)
        )

        #Consideram ca exista un zambet daca detectorul a gasit unul
        zambeste = len(zambete) > 0
        #Analizam emotia o data la 15 cadre, pentru ca asa merge programul mai fara lag (mai usor)
        if cadre % 15 == 0:

            try:
                #Cerem modelului sa estimeze emotia de pe fata decupata
                rezultat = DeepFace.analyze(
                    img_path=fata_color,
                    actions=["emotion"],
                    enforce_detection = False
                )
                #Rezultatul poate fi o lista de dictionare
                #Daca este lista luam primul dictioar din ea
                if isinstance(rezultat,list):
                    rezultat = rezultat[0]

                #Din dictionarul rezultat luam valoarea asociata cheii
                #dominant_emotion adica emotia cea mai puternica
                emotie_engleza = rezultat["dominant_emotion"]

                #Citim scorul emotiei dominante (un procent intre 0 si 100)
                scor = rezultat["emotion"][emotie_engleza]

                #Cautam traducerea etichetei in dictionarul traducere
                #Daca nu exista pastram textul original
                emotie = traducere.get(emotie_engleza,emotie_engleza)
            except Exception:
                print("Analiza nu a reusit")

        #Numaram un zambet cand emotia devine "fericit"
        if emotie == "fericit":
            if era_fericit == False:
                numar_zambete += 1
            era_fericit = True
        else:
            era_fericit = False

        #Desenam triunghiul pe fata
        cv2.rectangle(
            #Imaginea pe care desenam
            imagine,
            (x,y),
            #Coordonatele coltului din dreapta
            (x + latime, y + inaltime),
            (0,255,0),
            2
        )
        #Verificam valoarea booleana din variabila zambeste
        if zambeste:
            text_zambet = "Zambet:Detectat"
        else:
            text_zambet = "Zambet:Nedetectat"

        #Daca scorul e sub 40%, emotia nu e sigura
        if scor < 40:
            text_emotie = "Emotie neclara"
        else:
            text_emotie = "Emotie: " + emotie + " | Scor: " + str(round(scor)) + "%"

        cv2.putText(
            imagine,
            text_emotie,

            (20,35), #Pozitia textului:20 pixeli la stanga si 35 in sus
            cv2.FONT_HERSHEY_SIMPLEX,

            0.8, #Marimea textului
            (255,0,0),
            2
        )
        cv2.putText(
            imagine,
            text_zambet,
            (20, 70), #Pozitia textului, mai jos decat primul text
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8, #Marimea textului
            (0,255,0),
            2
        )
        #Afisam numarul de zambete
        cv2.putText(
            imagine,
            "Numar zambete: " + str(numar_zambete),
            (20, 105), #Mai jos decat textul cu zambetul
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,0,0),
            2
        )
    else:
        cv2.putText(
            imagine,
            "Nu am detectat vreo fata",
            (20,35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,0,255),
            2 #Grosimea textului
        )
    cv2.imshow("Detector Expresii faciale:", imagine)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()