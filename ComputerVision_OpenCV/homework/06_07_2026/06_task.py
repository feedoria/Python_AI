import cv2
import numpy as np

# incarc detectorul de fata
detector_fata = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# incarc personajele
personaj1 = cv2.imread(
    "/Users/feedoria/Desktop/Python_AI/ComputerVision_OpenCV/homework/06_07_2026/hello_kitty.png",
    cv2.IMREAD_UNCHANGED
)

personaj2 = cv2.imread(
    "/Users/feedoria/Desktop/Python_AI/ComputerVision_OpenCV/homework/06_07_2026/kuromi.png",
    cv2.IMREAD_UNCHANGED
)

lista_personaje = [personaj1, personaj2]
nume_personaje = ["Hello Kitty", "Kuromi"]

# verific imaginile
for personaj in lista_personaje:
    if personaj is None:
        print("Nu am putut incarca imaginea")
        exit()

    if personaj.shape[2] != 4:
        print("Imaginea nu are canal transparent")
        exit()

# pornesc camera
camera = cv2.VideoCapture(0)

# primul personaj este activ
index_personaj = 0

# overlay-ul este pornit la inceput
activ = True

if not camera.isOpened():
    print("Nu am reusit sa deschidem camera")
else:
    while True:
        ok, frame = camera.read()

        if not ok:
            print("Nu am putut citi imaginea")
            break

        # transform imaginea in alb-negru
        gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detectez fetele
        fete = detector_fata.detectMultiScale(
            gri,
            scaleFactor=1.1,
            minNeighbors=5
        )

        # aleg personajul activ
        personaj = lista_personaje[index_personaj]

        for (x, y, w, h) in fete:

            if activ:
                # redimensionez personajul cat fata
                personaj_redim = cv2.resize(personaj, (w, h))

                # separ imaginea de transparenta
                personaj_bgr = personaj_redim[:, :, :3]
                personaj_alpha = personaj_redim[:, :, 3]

                masca = personaj_alpha / 255.0

                # iau zona fetei
                zona_fata = frame[y:y+h, x:x+w]

                # suprapun personajul
                for c in range(3):
                    zona_fata[:, :, c] = (
                        personaj_bgr[:, :, c] * masca +
                        zona_fata[:, :, c] * (1 - masca)
                    ).astype(np.uint8)

                frame[y:y+h, x:x+w] = zona_fata

            else:
                # daca e off ramane doar dreptunghiul
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

        # afisez daca personajul este pornit sau oprit
        if activ:
            cv2.putText(
                frame,
                "Personaj: ON",
                (frame.shape[1] - 210, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )
        else:
            cv2.putText(
                frame,
                "Personaj: OFF",
                (frame.shape[1] - 210, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # afisez personajul ales
        cv2.putText(
            frame,
            f"Personaj activ: {nume_personaje[index_personaj]}",
            (10, frame.shape[0] - 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.imshow("Personaj pe fata", frame)

        # citesc tasta o singura data
        tasta = cv2.waitKey(1)

        # pornesc/opresc personajul
        if tasta == ord("p"):
            activ = not activ

        # aleg hello kitty
        if tasta == ord("1"):
            index_personaj = 0

        # aleg kuromi
        if tasta == ord("2"):
            index_personaj = 1

        # inchid cu q
        if tasta == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()