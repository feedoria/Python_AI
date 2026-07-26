import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Nu am reusit sa deschidem camera web")
else:
    factor_pixelare = 40
    while True:
        ok, frame = camera.read()

        if not ok:
            print("nu am putut citi imaginea")
            break

        inaltime, latime, canale = frame.shape

        mica = cv2.resize(frame, (factor_pixelare, factor_pixelare))
        pixelat = cv2.resize(mica, (latime, inaltime), interpolation=cv2.INTER_NEAREST)

        cv2.imshow("Camera de cartofi", pixelat)

        tasta = cv2.waitKey(1)

        if tasta == ord("+"):
            factor_pixelare = factor_pixelare + 5

        if tasta == ord("-"):
            factor_pixelare = factor_pixelare - 5

        if factor_pixelare < 5:
            factor_pixelare = 5 

        if cv2.waitKey(1) == ord('q'):
            break