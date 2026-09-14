import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk  # Pillow face conversia intre OpenCV si Tkinter pentru frame-uri


class FaceDetectionApp:

    def __init__(self, root):
        self.root = root

        self.root.title("Face Detection cu OpenCV")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Varibilele aplicatiei
        self.camera = None
        self.camera_running = False

        self.face_cascade = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml"
        )

        if self.face_cascade.empty():
            messagebox.showerror(
                "Eroare",
                "Modelul Haarcascade nu a putut fi pornit.\n"
                "Fisierul haarcascade_frontalface_default.xml "
                "trebuie sa existe in folderul proiectului."
            )

            self.root.destroy()
            return

        self.create_widgets()  # Construieste Fereastra de tkinter

        self.root.protocol(
            "WM_DELETE_WINDOW",  # Metoda pentru stergere
            self.close_app  # Functia pentru stergere care se afla mai in jos
        )

    def create_widgets(self):

        title_label = tk.Label(
            self.root,
            text="Face Detection cu OpenCV",
            font=("Arial", 24, "bold")
        )

        title_label.pack(
            pady=20
        )

        # Descriere
        description_label = tk.Label(
            self.root,
            text="Porneste camera pentru a detecta fete",
            font=("Arial", 12)
        )

        description_label.pack(
            pady=5
        )

        # Zona unde afisam camera web din PC
        self.camera_label = tk.Label(
            self.root,
            text="Camera este oprita",
            width=70,
            height=25,
            bg="black",
            fg="white",
            font=("Arial", 16)
        )

        self.camera_label.pack(
            padx=20,
            pady=20,
            expand=True
        )

        # Facem butoane
        button_frame = tk.Frame(
            self.root
        )

        button_frame.pack(
            pady=10
        )

        self.start_button = tk.Button(
            button_frame,
            text="Porneste Camera",
            font=("Arial", 12, "bold"),
            command=self.start_camera,  # E functia butoanelor
            width=18
        )

        self.start_button.pack(
            side=tk.LEFT,
            padx=10
        )

        self.stop_button = tk.Button(
            button_frame,
            text="Opreste camera",
            font=("Arial", 12, "bold"),
            command=self.stop_camera,
            width=18,
            state=tk.DISABLED  # Asta imi opreste camera
        )

        self.stop_button.pack(
            side=tk.LEFT,
            padx=10
        )

        # Buton de exit
        self.exit_button = tk.Button(
            button_frame,
            text="Iesire",
            font=("Arial", 12, "bold"),
            command=self.close_app,
            width=18
        )

        self.exit_button.pack(
            side=tk.LEFT,
            padx=10
        )

    # Metoda de start_camera
    def start_camera(self):

        if self.camera_running:  # Daca deja ruleaza camera nu mai facem nimic
            return

        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            messagebox.showerror(
                "Eroare",
                "Camera nu poate fi pornita"
            )

            self.camera.release()
            self.camera = None

            return

        self.camera_running = True

        # Modificam butoanele
        self.start_button.config(
            state=tk.DISABLED
        )

        self.stop_button.config(
            state=tk.NORMAL
        )

        self.update_frame()  # Porneste procesarea frame-urilor (porneste camera)

    def update_frame(self):

        if not self.camera_running:
            return

        ret, frame = self.camera.read()

        if not ret:
            messagebox.showerror(
                "Eroare",
                "Nu s-a putut citi imaginea"
            )

            self.stop_camera()
            return

        frame = cv2.flip(
            frame,
            1
        )

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        # Detectia fetelor
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,  # Mareste cu 10%
            minNeighbors=5,  # Trebuie sa avem minim 5 dovezi ca sa fie o fata
            minSize=(50, 50)
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame,
                (x, y),  # Coltul din stanga sus
                (x + w, y + h),  # Coltul din dreapta jos
                (0, 255, 0),  # Culoarea
                2
            )

        cv2.putText(
            frame,
            f"Fete Detectate: {len(faces)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Facem conversia dintre OpenCV si Tkinter
        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(
            frame_rgb
        )

        photo = ImageTk.PhotoImage(
            image=image
        )

        self.camera_label.config(
            image=photo,
            text=""
        )

        self.camera_label.image = photo

        self.root.after(
            10,
            self.update_frame
        )

    def stop_camera(self):

        self.camera_running = False

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        self.camera_label.config(
            image="",
            text="Camera este oprita"
        )

        self.camera_label.image = None

        self.start_button.config(
            state=tk.NORMAL
        )

        self.stop_button.config(
            state=tk.DISABLED
        )

    def close_app(self):

        # Oprim camera inainte sa inchidem aplicatia
        self.stop_camera()

        # Inchidem fereastra
        self.root.destroy()


root = tk.Tk()

app = FaceDetectionApp(
    root
)

root.mainloop()

