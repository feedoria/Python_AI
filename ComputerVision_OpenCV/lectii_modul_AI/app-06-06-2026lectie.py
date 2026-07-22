import cv2

# incarcam detectorul de fete
detector_fata = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# incarcam detectorul de zambete
detector_zambet = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_smile.xml"
)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Nu am reusit sa deschidem camera web")
else:
    while True:
        ok, frame = camera.read()

        if not ok:
            print("Nu am putut sa iti vedem fata")
            break

        # transformam imaginea in alb-negru
        gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detectam fetele
        fete = detector_fata.detectMultiScale(
            gri,
            scaleFactor=1.1,
            minNeighbors=5
        )

        for (x, y, w, h) in fete:
            # desenam dreptunghi in jurul fetei
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # decupam zona fetei
            fata_gri = gri[y:y+h, x:x+w]

            # detectam zambetul doar in zona fetei
            zambete = detector_zambet.detectMultiScale(
                fata_gri,
                scaleFactor=1.7,
                minNeighbors=20
            )

            if len(zambete) > 0:
                cv2.putText(
                    frame,
                    "Zambeste mai tare",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

        cv2.imshow("Detectare zambet - Webcam", frame)

        if cv2.waitKey(1) == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()