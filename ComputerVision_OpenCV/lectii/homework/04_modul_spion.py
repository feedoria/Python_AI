import cv2
import numpy as np

camera = cv2.VideoCapture(0)

detector_fata = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

if not camera.isOpened():
    print("Nu am reusit sa deschidem camera web")
else:
    while True:
        ok, frame = camera.read()

        if not ok:
            print("nu am putut citi imaginea")
            break
        
        gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        fete = detector_fata.detectMultiScale(
                gri,
                scaleFactor=1.1,
                minNeighbors=5
            )
        
        masca = np.zeros_like(frame)

        for (x, y, w, h) in fete:
            #calculez mijlocul fetei
            centru_x = x + w // 2
            centru_y = y + h // 2

            cv2.circle(masca, (centru_x, centru_y), 150, (255, 255, 255), -1)

        rezultat = cv2.bitwise_and(frame, masca)

        cv2.imshow("Modul spion", rezultat)

        if cv2.waitKey(1) == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()