import cv2
import time

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Nu am reusit sa deschidem camera web")
else:
    nr_captura = 0
    timp_salvare = 0

    while True:
        ok, frame = camera.read()

        if not ok:
            print("nu am putut citi imaginea")
            break

        tasta = cv2.waitKey(1)

        if tasta == ord('s'):
            nr_captura += 1
            nume_fisier = f"captura_{nr_captura}.png"
            cv2.imwrite(nume_fisier, frame)
            timp_salvare = time.time()

        if time.time() - timp_salvare < 1:
            cv2.putText(
                frame,
                "Salvat!",
                (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        cv2.imshow("Camera web", frame)

        if tasta == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()