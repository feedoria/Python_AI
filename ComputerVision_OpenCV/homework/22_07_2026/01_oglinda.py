import cv2
import time

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Nu am reusit sa deschidem camera web")
else:
    while True:
        ok, frame = camera.read()

        if not ok:
            print("nu am putut citi imaginea")
            break

        frame = cv2.flip(frame, 1)

        timp = time.time()

        if int(timp)%5 == 0:
            frame = cv2.flip(frame, 0)
        
        cv2.imshow("Oglinda care clipeste", frame)

        if cv2.waitKey(1) == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()