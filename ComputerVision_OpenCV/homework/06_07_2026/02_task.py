import cv2

camera = cv2.VideoCapture(0)

detector_fata = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
if not camera.isOpened():
    print("Nu am reusit sa deschidem camera web")
else:
    record = 0
    while True:
        ok, frame = camera.read()
        nr_fete = 0

        if not ok:
            print("nu am putut citi imaginea")
            break

        # Detectează fețele în imagine
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fete = detector_fata.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7)

        # Desenează dreptunghiuri în jurul fețelor detectate
        for (x, y, w, h) in fete:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            nr_fete += 1

        if record < nr_fete:
            record = nr_fete
        cv2.putText(frame, f"Nr fete detectate: {nr_fete}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Record fete detectate: {record}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Camera web", frame)

        if cv2.waitKey(1) == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()