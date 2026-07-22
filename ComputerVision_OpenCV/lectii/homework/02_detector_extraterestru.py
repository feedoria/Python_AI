import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Nu am reusit sa deschidem camera web")
else:
    frame_count = 0

    while True:
        ok, frame = camera.read()

        if not ok:
            print("nu am putut citi imaginea")
            break
        
        frame[:,:, 0] = 0  # Eliminam canalul albastru
        frame[:,:, 2] = 0  # Eliminam canalul rosu

        frame_count += 1
        if frame_count % 40 < 20:
            cv2.putText(
                frame,
                "EXTRATERESTRU DETECTAT",
                (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

        cv2.imshow("Detector de extraterestri", frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
camera.release()
cv2.destroyAllWindows()