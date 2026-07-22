import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Nu am reusit sa deschidem camera web")
else:
    gri_vechi = None

    while True:
        ok, frame = camera.read()

        if not ok:
            print("Nu am putut citi imaginea")
            break

        gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if gri_vechi is None:
            gri_vechi = gri.copy()

        diferenta = cv2.absdiff(gri, gri_vechi)
        scor = diferenta.sum()

        inaltime, latime = gri.shape

        if scor > 10000000:
            cv2.putText(
                frame,
                "MISCARE DETECTATA!",
                (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

            cv2.rectangle(
                frame,
                (0, 0),
                (latime - 1, inaltime - 1),
                (0, 0, 255),
                5
            )
        else:
            cv2.putText(
                frame,
                "Totul e calm",
                (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        gri_vechi = gri.copy()

        cv2.imshow("Alarma de hoti", frame)

        if cv2.waitKey(1) == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()