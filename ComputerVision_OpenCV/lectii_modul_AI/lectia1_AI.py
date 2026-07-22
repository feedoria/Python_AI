import cv2

# imagine = cv2.imread("/Users/feedoria/Desktop/ProgrameCursPython/WhatsApp Image 2026-06-29 at 19.21.07.jpeg")

# if imagine is None:
#     print("Nu am gasit fisierul cu poza")
# else:
#     x = 50 #orizontala
#     y = 100 #verticala
#     w = 200 #latime
#     h = 150 #inaltime

# #Desenam un dreptunghi pe imagine 
# cv2.rectangle(imagine, (x,y), (x + w, y + h), (0,255,0), 2) #rgb
# cv2.imshow("Poza cu dreptunghi", imagine)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

detector_fata = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#Pornim camera
camera = cv2.VideoCapture(0) # 0 = camera principala -> daca e camera web externa punem 1

#verfificam daca camera s-a deschis 
# if not camera.isOpened():
#     print("Nu am reusit sa deschid camera web")
# else:
#     while True:
#         ok,frame = camera.read()

#         if not ok:
#             print("Nu am putut sa iti vedem fata")
#             break
#         #Transformam imaginea in alb negru
#         gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         fete = detector_fata.detectMultiScale(gri, scaleFactor=1.1, minNeighbors=5)
#         #detectMultiScale -> detecteaza fetele 
#         #scaleFactor -> arata cat de mult micsoram imaginea 

#         #Desenam un dreptunghi in jurul fetei 
#         for (x,y,w,h) in fete:
#             cv2.rectangle(frame, (x, y), (x+w, x+h), (0,255,0), 2)
        
#         cv2.imshow("Detectie de fete - webca,", frame)
#         tasta = cv2.waitKey(1) # asteapta sa pei o tasta

#         if tasta == ord('q'):
#             break
            
#         camera.release() # sa inchizi camera
#         cv2.distroyAllWindows()

# import cv2 

# #Incarc un modul care stie sa recunoasca fetele
# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# )

# #Pornim camera 

# camera = cv2.VideoCapture(0)

# while True:
#     #Citim un cadru (o poza) din video
#     ok, frame = camera.read()

#     #Daca nu merge camera, iefim
#     if not ok:
#         break

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     #Hai sa detectam fetele din cadru 

#     faces = face_cascade.detectMultiScale(gray, 1.1, 5)
#     # ScaleFactor 1.1 --> cauta fata putin mai mare si fata cea mai mica 
#     # minNEighbors = 5 --> Cat de sigur trebuie sa fie, cate fete sa imi arate 
    
#     #Desenam un patrat pe fata 
#     for(x, y, w, h) in faces:
#         #(x,y) --> sunt coltul de sus-stanga a fetei
#         #w --> latimea fetei
#         #h-->inaltimea fetei

#         cv2.rectangle(frame, (x,y),(x + w, y + h), (0,255,0),2)

#     cv2.imshow("Detectare fata", frame)

#     #Daca apesi tasta Q --> iesi acas 
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break


# camera.release()
# cv2.destroyAllWindows()

#-----------------------
# TASK: Sistem de detectare a feței + contur dinamic
# 🎯 Obiectiv
# Creează un program care:

# Pornește camera web.

# Detectează fețele folosind CascadeClassifier (exact ca în codul tău).

# În loc să deseneze un dreptunghi verde fix, desenează un dreptunghi care își schimbă culoarea în funcție de poziția feței.

# 📌 Reguli obligatorii
# Folosește exact codul tău, doar puțin modificat.

# Folosește aceleași variabile: x, y, w, h.

# Nu ai voie să folosești YOLO, doar Haar Cascade.

# Nu ai voie să folosești funcții noi complicate.

# Culoarea dreptunghiului trebuie să depindă de poziția feței:

# Dacă fața este în partea stângă → dreptunghiul devine albastru.

# Dacă fața este în centru → dreptunghiul devine verde.

# Dacă fața este în dreapta → dreptunghiul devine roșu.

# 🧸 Hint vizual (nu este soluție!)
# 🧠 Ce trebuie să folosești din codul tău
# cv2.VideoCapture(0)

# cv2.cvtColor

# detectMultiScale

# bucla for (x, y, w, h) in fete:

# cv2.rectangle

# cv2.imshow

# cv2.waitKey

# camera.release()

# cv2.destroyAllWindows()

# 🧩 Ce trebuie să adaugi tu
# O condiție care verifică poziția feței:
# x < ceva
# x > ceva
# altfel
import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

#pornesc camera
camera = cv2.VideoCapture(0)

while True:
    ok,frame = camera.read()

    if not ok:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x,y,w,h) in faces:
        if x < 200:
            culoare = (255, 0, 0) #albastru 
        elif x > 400:
            culoare = (0, 0, 255)#rosu
        else:
            culoare = (0, 255, 0) #verde
    
        cv2.rectangle(frame, (x,y),(x + w, y + h), culoare,2)
    
    cv2.imshow("Detectare fata", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
