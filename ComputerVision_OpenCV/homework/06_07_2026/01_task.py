import cv2

#incarc detectorul de fete
detector_fata = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Nu am reusit sa deschidem camera web")
else:
    while True:
        ok, frame = camera.read()

        if not ok:
            print("nu am putut citi imaginea")
            break

        gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        fete = detector_fata.detectMultiScale(gri, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in fete:
            #desenez dreptunghi verde in jurul fetei detectate
            cv2.rectangle(
                frame,
                (x, y), 
                (x+w, y+h), 
                (0, 255, 0), 
                2)
            #daca fata e prea sus afisez textul in interiorul dreptunghiului
            if y > 20:
                pozitie_text = (x, y-10)
            else:
                pozitie_text = (x, y+20)

            #afisez textul de deasupra fetei
            cv2.putText(
                frame, 
                "Fata detectata", 
                pozitie_text, 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, 
                (0, 255, 0), 
                2)
            #afisez dimensiunile fetei sub dreptunghi 
            cv2.putText(
                frame, 
                f"Dimensiuni: {w}x{h} px", 
                (x, y+h+20), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, 
                (0, 255, 0), 
                2)

        cv2.imshow("Detector de fete", frame)

        if cv2.waitKey(1) == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()