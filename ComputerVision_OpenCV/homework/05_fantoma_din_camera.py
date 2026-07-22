import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Nu am reusit sa deschidem camera web")
else:
    nr_frameuri = 0
    frame_vechi = None

    while True:
        ok, frame = camera.read()

        if not ok:
            print("nu am putut citi imaginea")
            break
        
        nr_frameuri += 1

        if frame_vechi is None:
            frame_vechi = frame.copy()

        fantoma = cv2.addWeighted(frame, 0.6, frame_vechi, 0.4, 0)

        if nr_frameuri % 15 == 0:
            frame_vechi = frame.copy()

        cv2.imshow("Fantoma", fantoma)

        if cv2.waitKey(1) == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()