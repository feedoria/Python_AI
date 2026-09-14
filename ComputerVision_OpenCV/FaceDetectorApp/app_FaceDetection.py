import tkinter as tk
from tkinter import messagebox, ttk

import cv2
import numpy as np

import os
import time
import math
import subprocess

from datetime import datetime
from PIL import Image, ImageTk

from ComputerVision_OpenCV.FaceDetectorApp.mp_palmdet import MPPalmDet
from ComputerVision_OpenCV.FaceDetectorApp.mp_handpose import MPHandPose


class FaceDetectionApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Pink Vision")
        self.root.geometry("1180x900")
        self.root.minsize(1050, 820)

        # =========================
        # COLORS
        # =========================

        self.COLOR_BLACK = "#08070B"
        self.COLOR_CARD = "#121016"
        self.COLOR_CARD_LIGHT = "#1B1720"

        self.COLOR_PINK = "#FF3EA5"
        self.COLOR_PINK_LIGHT = "#FF92CB"
        self.COLOR_PURPLE = "#A73BFF"

        self.COLOR_WHITE = "#FFFFFF"
        self.COLOR_GRAY = "#A8A3AD"
        self.COLOR_DARK_GRAY = "#55515B"

        # OpenCV uses BGR
        self.NEON_PINK = (180, 0, 255)
        self.NEON_PINK_LIGHT = (220, 110, 255)
        self.WHITE_BGR = (255, 255, 255)

        # =========================
        # CAMERA
        # =========================

        self.camera = None
        self.camera_running = False
        self.current_frame = None

        # =========================
        # MODES
        # =========================

        self.face_detection_active = True
        self.hand_detection_active = True

        self.privacy_mode = False
        self.mirror_mode = True

        self.air_draw_active = False
        self.zoom_control_active = False
        self.motion_detection_active = False
        self.gesture_music_active = True

        # =========================
        # FPS
        # =========================

        self.previous_time = 0

        # =========================
        # AIR DRAW
        # =========================

        self.drawing_layer = None
        self.previous_draw_point = None

        # =========================
        # ZOOM
        # =========================

        self.zoom_factor = 1.0
        self.zoom_smoothing = 0.15

        # =========================
        # MOTION DETECTION
        # =========================

        self.previous_motion_frame = None
        self.motion_detected = False
        self.motion_min_area = 1800

        # =========================
        # GESTURE MUSIC
        # =========================

        self.gesture_candidate = None
        self.gesture_candidate_frames = 0

        self.gesture_required_frames = 7

        self.last_music_gesture = None
        self.last_music_time = 0

        self.music_cooldown = 4

        self.audio_process = None

        # =========================
        # FILE PATHS
        # =========================

        self.current_folder = os.path.dirname(
            os.path.abspath(__file__)
        )

        self.korn_song = os.path.join(
            self.current_folder,
            "korn_yall_want_a_single.mp3"
        )

        self.muie_garda_song = os.path.join(
            self.current_folder,
            "muie_garda.mp3"
        )

        # =========================
        # FACE DETECTOR
        # =========================

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades
            + "haarcascade_frontalface_default.xml"
        )

        if self.face_cascade.empty():

            messagebox.showerror(
                "Error",
                "Face detection model could not be loaded."
            )

            self.root.destroy()
            return

        # =========================
        # HAND MODELS
        # =========================

        palm_model_path = os.path.join(
            self.current_folder,
            "palm_detection_mediapipe_2023feb.onnx"
        )

        hand_model_path = os.path.join(
            self.current_folder,
            "handpose_estimation_mediapipe_2023feb.onnx"
        )

        if not os.path.exists(palm_model_path):

            messagebox.showerror(
                "Error",
                "palm_detection_mediapipe_2023feb.onnx was not found."
            )

            self.root.destroy()
            return

        if not os.path.exists(hand_model_path):

            messagebox.showerror(
                "Error",
                "handpose_estimation_mediapipe_2023feb.onnx was not found."
            )

            self.root.destroy()
            return

        self.palm_detector = MPPalmDet(
            modelPath=palm_model_path,
            nmsThreshold=0.3,
            scoreThreshold=0.6,
            backendId=cv2.dnn.DNN_BACKEND_OPENCV,
            targetId=cv2.dnn.DNN_TARGET_CPU
        )

        self.handpose_detector = MPHandPose(
            modelPath=hand_model_path,
            confThreshold=0.8,
            backendId=cv2.dnn.DNN_BACKEND_OPENCV,
            targetId=cv2.dnn.DNN_TARGET_CPU
        )

        # =========================
        # HAND CONNECTIONS
        # =========================

        self.hand_connections = [

            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),

            (0, 5),
            (5, 6),
            (6, 7),
            (7, 8),

            (0, 9),
            (9, 10),
            (10, 11),
            (11, 12),

            (0, 13),
            (13, 14),
            (14, 15),
            (15, 16),

            (0, 17),
            (17, 18),
            (18, 19),
            (19, 20)
        ]

        self.create_gradient_background()
        self.create_styles()
        self.create_widgets()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_app
        )

    # =====================================================
    # GRADIENT BACKGROUND
    # =====================================================

    def create_gradient_background(self):

        self.gradient_canvas = tk.Canvas(
            self.root,
            highlightthickness=0
        )

        self.gradient_canvas.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        self.root.bind(
            "<Configure>",
            self.draw_gradient
        )

    def draw_gradient(self, event=None):

        width = self.root.winfo_width()
        height = self.root.winfo_height()

        if width <= 1 or height <= 1:
            return

        self.gradient_canvas.delete(
            "gradient"
        )

        start_color = (
            255,
            42,
            155
        )

        middle_color = (
            95,
            20,
            95
        )

        end_color = (
            8,
            7,
            11
        )

        for y in range(height):

            ratio = y / height

            if ratio < 0.35:

                local_ratio = ratio / 0.35

                r = int(
                    start_color[0]
                    + (
                        middle_color[0]
                        - start_color[0]
                    )
                    * local_ratio
                )

                g = int(
                    start_color[1]
                    + (
                        middle_color[1]
                        - start_color[1]
                    )
                    * local_ratio
                )

                b = int(
                    start_color[2]
                    + (
                        middle_color[2]
                        - start_color[2]
                    )
                    * local_ratio
                )

            else:

                local_ratio = (
                    ratio - 0.35
                ) / 0.65

                r = int(
                    middle_color[0]
                    + (
                        end_color[0]
                        - middle_color[0]
                    )
                    * local_ratio
                )

                g = int(
                    middle_color[1]
                    + (
                        end_color[1]
                        - middle_color[1]
                    )
                    * local_ratio
                )

                b = int(
                    middle_color[2]
                    + (
                        end_color[2]
                        - middle_color[2]
                    )
                    * local_ratio
                )

            color = (
                f"#{r:02x}{g:02x}{b:02x}"
            )

            self.gradient_canvas.create_line(
                0,
                y,
                width,
                y,
                fill=color,
                tags="gradient"
            )

        self.gradient_canvas.lower()

    # =====================================================
    # TTK STYLES
    # =====================================================

    def create_styles(self):

        self.style = ttk.Style()

        self.style.theme_use(
            "clam"
        )

        self.style.configure(
            "Pink.TButton",
            background=self.COLOR_CARD_LIGHT,
            foreground=self.COLOR_WHITE,
            font=("Arial", 10, "bold"),
            padding=(12, 9),
            borderwidth=1,
            relief="flat"
        )

        self.style.map(
            "Pink.TButton",
            background=[
                ("active", self.COLOR_PINK),
                ("pressed", self.COLOR_PURPLE)
            ],
            foreground=[
                ("active", self.COLOR_WHITE),
                ("pressed", self.COLOR_WHITE)
            ]
        )

        self.style.configure(
            "PinkOn.TButton",
            background=self.COLOR_PINK,
            foreground=self.COLOR_WHITE,
            font=("Arial", 10, "bold"),
            padding=(12, 9),
            borderwidth=1,
            relief="flat"
        )

        self.style.map(
            "PinkOn.TButton",
            background=[
                ("active", self.COLOR_PINK_LIGHT),
                ("pressed", self.COLOR_PURPLE)
            ],
            foreground=[
                ("active", self.COLOR_WHITE),
                ("pressed", self.COLOR_WHITE)
            ]
        )

        self.style.configure(
            "PinkOff.TButton",
            background="#2A2630",
            foreground=self.COLOR_GRAY,
            font=("Arial", 10, "bold"),
            padding=(12, 9),
            borderwidth=1,
            relief="flat"
        )

        self.style.map(
            "PinkOff.TButton",
            background=[
                ("active", "#3A3440"),
                ("pressed", self.COLOR_PURPLE)
            ],
            foreground=[
                ("active", self.COLOR_WHITE),
                ("pressed", self.COLOR_WHITE)
            ]
        )

        self.style.configure(
            "Danger.TButton",
            background="#35111E",
            foreground=self.COLOR_PINK_LIGHT,
            font=("Arial", 10, "bold"),
            padding=(12, 9),
            borderwidth=1,
            relief="flat"
        )

        self.style.map(
            "Danger.TButton",
            background=[
                ("active", "#6A1838"),
                ("pressed", "#8A204A")
            ],
            foreground=[
                ("active", self.COLOR_WHITE),
                ("pressed", self.COLOR_WHITE)
            ]
        )

    # =====================================================
    # UI
    # =====================================================

    def create_widgets(self):

        self.main_card = tk.Frame(
            self.root,
            bg=self.COLOR_CARD
        )

        self.main_card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=1080,
            height=820
        )

        # =========================
        # HEADER
        # =========================

        title_label = tk.Label(
            self.main_card,
            text="PINK VISION",
            bg=self.COLOR_CARD,
            fg=self.COLOR_PINK_LIGHT,
            font=("Arial", 28, "bold")
        )

        title_label.pack(
            pady=(18, 2)
        )

        subtitle_label = tk.Label(
            self.main_card,
            text="FACE  •  HANDS  •  GESTURES  •  MOTION",
            bg=self.COLOR_CARD,
            fg=self.COLOR_GRAY,
            font=("Arial", 11, "bold")
        )

        subtitle_label.pack(
            pady=(0, 8)
        )

        # =========================
        # CAMERA BORDER
        # =========================

        self.camera_border = tk.Frame(
            self.main_card,
            bg=self.COLOR_PINK,
            padx=3,
            pady=3
        )

        self.camera_border.pack(
            pady=8
        )

        self.camera_label = tk.Label(
            self.camera_border,
            text="CAMERA OFF",
            width=80,
            height=27,
            bg="#000000",
            fg=self.COLOR_PINK_LIGHT,
            font=("Arial", 14, "bold")
        )

        self.camera_label.pack()

        # =========================
        # STATISTICS
        # =========================

        stats_frame = tk.Frame(
            self.main_card,
            bg=self.COLOR_CARD_LIGHT
        )

        stats_frame.pack(
            pady=8,
            ipadx=10,
            ipady=7
        )

        self.faces_label = self.create_stat_label(
            stats_frame,
            "FACES  0"
        )

        self.hands_label = self.create_stat_label(
            stats_frame,
            "HANDS  0"
        )

        self.fingers_label = self.create_stat_label(
            stats_frame,
            "FINGERS  0"
        )

        self.gesture_label = self.create_stat_label(
            stats_frame,
            "GESTURE  -"
        )

        self.fps_label = self.create_stat_label(
            stats_frame,
            "FPS  0"
        )

        self.motion_label = self.create_stat_label(
            stats_frame,
            "MOTION  OFF"
        )

        # =========================
        # MAIN BUTTONS
        # =========================

        main_buttons = tk.Frame(
            self.main_card,
            bg=self.COLOR_CARD
        )

        main_buttons.pack(
            pady=7
        )

        self.start_button = self.create_button(
            main_buttons,
            "START CAMERA",
            self.start_camera,
            style="PinkOn.TButton"
        )

        self.stop_button = self.create_button(
            main_buttons,
            "STOP CAMERA",
            self.stop_camera,
            style="Danger.TButton"
        )

        self.stop_button.config(
            state=tk.DISABLED
        )

        self.screenshot_button = self.create_button(
            main_buttons,
            "SCREENSHOT",
            self.take_screenshot
        )

        self.clear_button = self.create_button(
            main_buttons,
            "CLEAR DRAW",
            self.clear_drawing
        )

        self.exit_button = self.create_button(
            main_buttons,
            "EXIT",
            self.close_app,
            style="Danger.TButton"
        )

        # =========================
        # MODE BUTTONS
        # =========================

        mode_buttons = tk.Frame(
            self.main_card,
            bg=self.COLOR_CARD
        )

        mode_buttons.pack(
            pady=7
        )

        self.face_button = self.create_button(
            mode_buttons,
            "FACE ON",
            self.toggle_face_detection,
            style="PinkOn.TButton"
        )

        self.hand_button = self.create_button(
            mode_buttons,
            "HANDS ON",
            self.toggle_hand_detection,
            style="PinkOn.TButton"
        )

        self.air_draw_button = self.create_button(
            mode_buttons,
            "AIR DRAW OFF",
            self.toggle_air_draw,
            style="PinkOff.TButton"
        )

        self.zoom_button = self.create_button(
            mode_buttons,
            "ZOOM OFF",
            self.toggle_zoom_control,
            style="PinkOff.TButton"
        )

        self.motion_button = self.create_button(
            mode_buttons,
            "MOTION OFF",
            self.toggle_motion_detection,
            style="PinkOff.TButton"
        )

        # =========================
        # SECOND MODE ROW
        # =========================

        mode_buttons_2 = tk.Frame(
            self.main_card,
            bg=self.COLOR_CARD
        )

        mode_buttons_2.pack(
            pady=7
        )

        self.privacy_button = self.create_button(
            mode_buttons_2,
            "PRIVACY OFF",
            self.toggle_privacy,
            style="PinkOff.TButton"
        )

        self.mirror_button = self.create_button(
            mode_buttons_2,
            "MIRROR ON",
            self.toggle_mirror,
            style="PinkOn.TButton"
        )

        self.music_button = self.create_button(
            mode_buttons_2,
            "GESTURE MUSIC ON",
            self.toggle_gesture_music,
            width=20,
            style="PinkOn.TButton"
        )

        # =========================
        # STATUS
        # =========================

        self.status_label = tk.Label(
            self.main_card,
            text="Ready.",
            bg=self.COLOR_CARD,
            fg=self.COLOR_GRAY,
            font=("Arial", 10)
        )

        self.status_label.pack(
            pady=8
        )

    def create_stat_label(
        self,
        parent,
        text
    ):

        label = tk.Label(
            parent,
            text=text,
            bg=self.COLOR_CARD_LIGHT,
            fg=self.COLOR_WHITE,
            font=("Arial", 10, "bold")
        )

        label.pack(
            side=tk.LEFT,
            padx=13
        )

        return label

    def create_button(
        self,
        parent,
        text,
        command,
        width=15,
        style="Pink.TButton"
    ):

        button = ttk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            style=style
        )

        button.pack(
            side=tk.LEFT,
            padx=5
        )

        return button

    # =====================================================
    # CAMERA
    # =====================================================

    def start_camera(self):

        if self.camera_running:
            return

        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():

            messagebox.showerror(
                "Error",
                "Camera could not be started."
            )

            self.camera = None
            return

        self.camera_running = True

        self.start_button.config(
            state=tk.DISABLED
        )

        self.stop_button.config(
            state=tk.NORMAL
        )

        self.previous_time = time.time()

        self.previous_motion_frame = None

        self.status_label.config(
            text="Camera started."
        )

        self.update_frame()

    # =====================================================
    # HAND DETECTION
    # =====================================================

    def detect_hands(
        self,
        frame
    ):

        hands = []

        palms = self.palm_detector.infer(
            frame
        )

        for palm in palms:

            hand = self.handpose_detector.infer(
                frame,
                palm
            )

            if hand is not None:
                hands.append(hand)

        return hands

    def get_hand_data(
        self,
        hand
    ):

        landmarks = hand[
            4:67
        ].reshape(
            21,
            3
        )

        handedness_value = hand[-2]
        confidence = hand[-1]

        if handedness_value <= 0.5:
            handedness = "LEFT"
        else:
            handedness = "RIGHT"

        return (
            landmarks,
            handedness,
            confidence
        )

    # =====================================================
    # NEON HAND
    # =====================================================

    def draw_neon_hand(
        self,
        frame,
        landmarks,
        handedness,
        confidence
    ):

        points = []

        for landmark in landmarks:

            x = int(
                landmark[0]
            )

            y = int(
                landmark[1]
            )

            points.append(
                (x, y)
            )

        glow = frame.copy()

        for start, end in self.hand_connections:

            cv2.line(
                glow,
                points[start],
                points[end],
                self.NEON_PINK,
                10,
                cv2.LINE_AA
            )

        glow = cv2.GaussianBlur(
            glow,
            (15, 15),
            0
        )

        frame[:] = cv2.addWeighted(
            frame,
            0.78,
            glow,
            0.22,
            0
        )

        for start, end in self.hand_connections:

            cv2.line(
                frame,
                points[start],
                points[end],
                self.NEON_PINK,
                4,
                cv2.LINE_AA
            )

            cv2.line(
                frame,
                points[start],
                points[end],
                self.NEON_PINK_LIGHT,
                1,
                cv2.LINE_AA
            )

        for index, point in enumerate(points):

            radius = 5

            if index in [
                4,
                8,
                12,
                16,
                20
            ]:

                radius = 8

            cv2.circle(
                frame,
                point,
                radius + 4,
                self.NEON_PINK,
                2,
                cv2.LINE_AA
            )

            cv2.circle(
                frame,
                point,
                radius,
                self.WHITE_BGR,
                -1,
                cv2.LINE_AA
            )

        wrist = points[0]

        cv2.putText(
            frame,
            f"{handedness} {confidence * 100:.0f}%",
            (
                wrist[0] + 10,
                wrist[1] + 30
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            self.NEON_PINK_LIGHT,
            2,
            cv2.LINE_AA
        )

        return points

    # =====================================================
    # FINGER STATES
    # =====================================================

    def get_finger_states(
        self,
        points
    ):

        if len(points) != 21:

            return [
                False,
                False,
                False,
                False,
                False
            ]

        wrist = points[0]

        finger_pairs = [
            (2, 4),
            (6, 8),
            (10, 12),
            (14, 16),
            (18, 20)
        ]

        states = []

        for lower_point, tip_point in finger_pairs:

            lower_distance = math.hypot(
                points[lower_point][0] - wrist[0],
                points[lower_point][1] - wrist[1]
            )

            tip_distance = math.hypot(
                points[tip_point][0] - wrist[0],
                points[tip_point][1] - wrist[1]
            )

            states.append(
                tip_distance
                >
                lower_distance * 1.12
            )

        return states

    # =====================================================
    # GESTURE RECOGNITION
    # =====================================================

    def recognize_gesture(
        self,
        finger_states
    ):

        (
            thumb,
            index,
            middle,
            ring,
            pinky
        ) = finger_states

        if (
            index
            and pinky
            and not middle
            and not ring
        ):

            return "ROCK"

        if (
            middle
            and not index
            and not ring
            and not pinky
        ):

            return "MIDDLE"

        if (
            index
            and middle
            and not ring
            and not pinky
        ):

            return "PEACE"

        if (
            index
            and not middle
            and not ring
            and not pinky
        ):

            return "POINT"

        if (
            index
            and middle
            and ring
            and pinky
        ):

            return "OPEN PALM"

        if (
            not index
            and not middle
            and not ring
            and not pinky
        ):

            return "FIST"

        return "-"

    # =====================================================
    # MUSIC
    # =====================================================

    def process_music_gesture(
        self,
        gesture
    ):

        if not self.gesture_music_active:
            return

        if gesture not in [
            "ROCK",
            "MIDDLE"
        ]:

            self.gesture_candidate = None
            self.gesture_candidate_frames = 0
            self.last_music_gesture = None

            return

        if gesture == self.gesture_candidate:

            self.gesture_candidate_frames += 1

        else:

            self.gesture_candidate = gesture
            self.gesture_candidate_frames = 1

        if (
            self.gesture_candidate_frames
            <
            self.gesture_required_frames
        ):

            return

        current_time = time.time()

        if (
            current_time
            - self.last_music_time
            <
            self.music_cooldown
        ):

            return

        if gesture == self.last_music_gesture:
            return

        if gesture == "ROCK":

            self.play_song(
                self.korn_song,
                "Korn - Y'All Want a Single"
            )

        elif gesture == "MIDDLE":

            self.play_song(
                self.muie_garda_song,
                "Muie Garda"
            )

        self.last_music_gesture = gesture
        self.last_music_time = current_time

    def play_song(
        self,
        song_path,
        song_name
    ):

        if not os.path.exists(song_path):

            self.status_label.config(
                text=f"Missing audio file: {os.path.basename(song_path)}"
            )

            return

        if (
            self.audio_process is not None
            and self.audio_process.poll() is None
        ):

            self.audio_process.terminate()

        try:

            self.audio_process = subprocess.Popen(
                [
                    "afplay",
                    song_path
                ]
            )

            self.status_label.config(
                text=f"Now playing: {song_name}"
            )

        except Exception as error:

            self.status_label.config(
                text=f"Audio error: {error}"
            )

    # =====================================================
    # AIR DRAW
    # =====================================================

    def process_air_draw(
        self,
        frame,
        points,
        finger_states
    ):

        if not self.air_draw_active:

            self.previous_draw_point = None
            return

        if self.drawing_layer is None:

            self.drawing_layer = np.zeros_like(
                frame
            )

        (
            thumb,
            index,
            middle,
            ring,
            pinky
        ) = finger_states

        drawing_gesture = (
            index
            and not middle
        )

        if drawing_gesture:

            current_point = points[8]

            if self.previous_draw_point is not None:

                cv2.line(
                    self.drawing_layer,
                    self.previous_draw_point,
                    current_point,
                    self.NEON_PINK,
                    12,
                    cv2.LINE_AA
                )

                cv2.line(
                    self.drawing_layer,
                    self.previous_draw_point,
                    current_point,
                    self.NEON_PINK_LIGHT,
                    4,
                    cv2.LINE_AA
                )

            self.previous_draw_point = current_point

        else:

            self.previous_draw_point = None

    def clear_drawing(self):

        self.drawing_layer = None
        self.previous_draw_point = None

        self.status_label.config(
            text="Drawing cleared."
        )

    # =====================================================
    # ZOOM
    # =====================================================

    def process_zoom(
        self,
        points
    ):

        if not self.zoom_control_active:

            target_zoom = 1.0

        else:

            thumb_tip = points[4]
            index_tip = points[8]

            palm_left = points[5]
            palm_right = points[17]

            pinch_distance = math.hypot(
                thumb_tip[0] - index_tip[0],
                thumb_tip[1] - index_tip[1]
            )

            palm_width = math.hypot(
                palm_left[0] - palm_right[0],
                palm_left[1] - palm_right[1]
            )

            if palm_width <= 1:

                target_zoom = self.zoom_factor

            else:

                ratio = (
                    pinch_distance /
                    palm_width
                )

                ratio = np.clip(
                    ratio,
                    0.25,
                    1.6
                )

                target_zoom = np.interp(
                    ratio,
                    [
                        0.25,
                        1.6
                    ],
                    [
                        1.0,
                        2.5
                    ]
                )

        self.zoom_factor += (
            target_zoom
            - self.zoom_factor
        ) * self.zoom_smoothing

    def apply_zoom(
        self,
        frame
    ):

        zoom = max(
            1.0,
            self.zoom_factor
        )

        if zoom <= 1.01:
            return frame

        height, width = frame.shape[:2]

        new_width = int(
            width / zoom
        )

        new_height = int(
            height / zoom
        )

        x1 = (
            width - new_width
        ) // 2

        y1 = (
            height - new_height
        ) // 2

        crop = frame[
            y1:y1 + new_height,
            x1:x1 + new_width
        ]

        return cv2.resize(
            crop,
            (
                width,
                height
            ),
            interpolation=cv2.INTER_LINEAR
        )

    # =====================================================
    # MOTION DETECTION
    # =====================================================

    def process_motion(
        self,
        raw_frame
    ):

        self.motion_detected = False

        if not self.motion_detection_active:

            self.previous_motion_frame = None
            return []

        gray = cv2.cvtColor(
            raw_frame,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.GaussianBlur(
            gray,
            (21, 21),
            0
        )

        if self.previous_motion_frame is None:

            self.previous_motion_frame = gray
            return []

        difference = cv2.absdiff(
            self.previous_motion_frame,
            gray
        )

        threshold = cv2.threshold(
            difference,
            25,
            255,
            cv2.THRESH_BINARY
        )[1]

        threshold = cv2.dilate(
            threshold,
            None,
            iterations=2
        )

        contours, hierarchy = cv2.findContours(
            threshold,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        motion_boxes = []

        for contour in contours:

            if (
                cv2.contourArea(contour)
                <
                self.motion_min_area
            ):

                continue

            x, y, w, h = cv2.boundingRect(
                contour
            )

            motion_boxes.append(
                (
                    x,
                    y,
                    w,
                    h
                )
            )

            self.motion_detected = True

        self.previous_motion_frame = cv2.addWeighted(
            self.previous_motion_frame,
            0.90,
            gray,
            0.10,
            0
        ).astype(
            np.uint8
        )

        return motion_boxes

    # =====================================================
    # FACE CORNERS
    # =====================================================

    def draw_face_corners(
        self,
        frame,
        x,
        y,
        w,
        h
    ):

        length = int(
            min(w, h) * 0.25
        )

        color = self.NEON_PINK_LIGHT

        thickness = 3

        cv2.line(
            frame,
            (x, y),
            (x + length, y),
            color,
            thickness
        )

        cv2.line(
            frame,
            (x, y),
            (x, y + length),
            color,
            thickness
        )

        cv2.line(
            frame,
            (x + w, y),
            (x + w - length, y),
            color,
            thickness
        )

        cv2.line(
            frame,
            (x + w, y),
            (x + w, y + length),
            color,
            thickness
        )

        cv2.line(
            frame,
            (x, y + h),
            (x + length, y + h),
            color,
            thickness
        )

        cv2.line(
            frame,
            (x, y + h),
            (x, y + h - length),
            color,
            thickness
        )

        cv2.line(
            frame,
            (x + w, y + h),
            (x + w - length, y + h),
            color,
            thickness
        )

        cv2.line(
            frame,
            (x + w, y + h),
            (x + w, y + h - length),
            color,
            thickness
        )

    # =====================================================
    # UPDATE FRAME
    # =====================================================

    def update_frame(self):

        if not self.camera_running:
            return

        ret, frame = self.camera.read()

        if not ret:

            messagebox.showerror(
                "Error",
                "Camera frame could not be read."
            )

            self.stop_camera()
            return

        if self.mirror_mode:

            frame = cv2.flip(
                frame,
                1
            )

        raw_frame = frame.copy()

        # =========================
        # MOTION DETECTION
        # =========================

        motion_boxes = self.process_motion(
            raw_frame
        )

        if self.motion_detection_active:

            for (
                x,
                y,
                w,
                h
            ) in motion_boxes:

                cv2.rectangle(
                    frame,
                    (
                        x,
                        y
                    ),
                    (
                        x + w,
                        y + h
                    ),
                    self.NEON_PINK,
                    2
                )

            if self.motion_detected:

                cv2.putText(
                    frame,
                    "MOTION DETECTED",
                    (
                        20,
                        frame.shape[0] - 25
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    self.NEON_PINK_LIGHT,
                    2,
                    cv2.LINE_AA
                )

        # =========================
        # FACE DETECTION
        # =========================

        faces = []

        if self.face_detection_active:

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(50, 50)
            )

            for (
                x,
                y,
                w,
                h
            ) in faces:

                if self.privacy_mode:

                    face = frame[
                        y:y + h,
                        x:x + w
                    ]

                    if face.size > 0:

                        blurred_face = cv2.GaussianBlur(
                            face,
                            (99, 99),
                            30
                        )

                        frame[
                            y:y + h,
                            x:x + w
                        ] = blurred_face

                else:

                    self.draw_face_corners(
                        frame,
                        x,
                        y,
                        w,
                        h
                    )

        # =========================
        # HAND DETECTION
        # =========================

        hands = []

        total_fingers = 0
        current_gesture = "-"

        if self.hand_detection_active:

            hands = self.detect_hands(
                frame
            )

            for hand_index, hand in enumerate(
                hands
            ):

                (
                    landmarks,
                    handedness,
                    confidence
                ) = self.get_hand_data(
                    hand
                )

                points = self.draw_neon_hand(
                    frame,
                    landmarks,
                    handedness,
                    confidence
                )

                finger_states = self.get_finger_states(
                    points
                )

                fingers = sum(
                    finger_states
                )

                total_fingers += fingers

                gesture = self.recognize_gesture(
                    finger_states
                )

                if hand_index == 0:

                    current_gesture = gesture

                    self.process_music_gesture(
                        gesture
                    )

                    self.process_air_draw(
                        frame,
                        points,
                        finger_states
                    )

                    self.process_zoom(
                        points
                    )

        else:

            self.previous_draw_point = None

            if not self.zoom_control_active:
                self.zoom_factor = 1.0

        # =========================
        # AIR DRAW
        # =========================

        if (
            self.drawing_layer is not None
            and
            self.drawing_layer.shape
            ==
            frame.shape
        ):

            frame = cv2.add(
                frame,
                self.drawing_layer
            )

        # =========================
        # ZOOM
        # =========================

        if self.zoom_control_active:

            frame = self.apply_zoom(
                frame
            )

        else:

            self.zoom_factor += (
                1.0 - self.zoom_factor
            ) * self.zoom_smoothing

        # =========================
        # FPS
        # =========================

        current_time = time.time()

        difference = (
            current_time
            -
            self.previous_time
        )

        if difference > 0:

            fps = (
                1 /
                difference
            )

        else:

            fps = 0

        self.previous_time = current_time

        # =========================
        # HUD
        # =========================

        cv2.putText(
            frame,
            f"FACES {len(faces)}",
            (
                20,
                32
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            self.NEON_PINK_LIGHT,
            2,
            cv2.LINE_AA
        )

        cv2.putText(
            frame,
            f"HANDS {len(hands)}",
            (
                20,
                60
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            self.NEON_PINK_LIGHT,
            2,
            cv2.LINE_AA
        )

        cv2.putText(
            frame,
            f"GESTURE {current_gesture}",
            (
                20,
                88
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            self.NEON_PINK_LIGHT,
            2,
            cv2.LINE_AA
        )

        if self.zoom_control_active:

            cv2.putText(
                frame,
                f"ZOOM {self.zoom_factor:.1f}x",
                (
                    20,
                    116
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                self.NEON_PINK_LIGHT,
                2,
                cv2.LINE_AA
            )

        # =========================
        # SAVE FRAME
        # =========================

        self.current_frame = frame.copy()

        # =========================
        # DISPLAY
        # =========================

        frame_display = cv2.resize(
            frame,
            (
                760,
                500
            )
        )

        frame_rgb = cv2.cvtColor(
            frame_display,
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
            text="",
            width=760,
            height=500
        )

        self.camera_label.image = photo

        # =========================
        # UPDATE UI
        # =========================

        self.faces_label.config(
            text=f"FACES  {len(faces)}"
        )

        self.hands_label.config(
            text=f"HANDS  {len(hands)}"
        )

        self.fingers_label.config(
            text=f"FINGERS  {total_fingers}"
        )

        self.gesture_label.config(
            text=f"GESTURE  {current_gesture}"
        )

        self.fps_label.config(
            text=f"FPS  {int(fps)}"
        )

        if not self.motion_detection_active:

            self.motion_label.config(
                text="MOTION  OFF",
                fg=self.COLOR_GRAY
            )

        elif self.motion_detected:

            self.motion_label.config(
                text="MOTION  YES",
                fg=self.COLOR_PINK_LIGHT
            )

        else:

            self.motion_label.config(
                text="MOTION  CLEAR",
                fg=self.COLOR_WHITE
            )

        self.root.after(
            10,
            self.update_frame
        )

    # =====================================================
    # TOGGLES
    # =====================================================

    def toggle_face_detection(self):

        self.face_detection_active = (
            not self.face_detection_active
        )

        if self.face_detection_active:

            self.face_button.config(
                text="FACE ON",
                style="PinkOn.TButton"
            )

        else:

            self.face_button.config(
                text="FACE OFF",
                style="PinkOff.TButton"
            )

    def toggle_hand_detection(self):

        self.hand_detection_active = (
            not self.hand_detection_active
        )

        if self.hand_detection_active:

            self.hand_button.config(
                text="HANDS ON",
                style="PinkOn.TButton"
            )

        else:

            self.hand_button.config(
                text="HANDS OFF",
                style="PinkOff.TButton"
            )

    def toggle_privacy(self):

        self.privacy_mode = (
            not self.privacy_mode
        )

        if self.privacy_mode:

            self.privacy_button.config(
                text="PRIVACY ON",
                style="PinkOn.TButton"
            )

        else:

            self.privacy_button.config(
                text="PRIVACY OFF",
                style="PinkOff.TButton"
            )

    def toggle_mirror(self):

        self.mirror_mode = (
            not self.mirror_mode
        )

        if self.mirror_mode:

            self.mirror_button.config(
                text="MIRROR ON",
                style="PinkOn.TButton"
            )

        else:

            self.mirror_button.config(
                text="MIRROR OFF",
                style="PinkOff.TButton"
            )

    def toggle_air_draw(self):

        self.air_draw_active = (
            not self.air_draw_active
        )

        self.previous_draw_point = None

        if self.air_draw_active:

            self.air_draw_button.config(
                text="AIR DRAW ON",
                style="PinkOn.TButton"
            )

            self.status_label.config(
                text="Air Draw enabled. Point with your index finger."
            )

        else:

            self.air_draw_button.config(
                text="AIR DRAW OFF",
                style="PinkOff.TButton"
            )

            self.status_label.config(
                text="Air Draw disabled."
            )

    def toggle_zoom_control(self):

        self.zoom_control_active = (
            not self.zoom_control_active
        )

        if self.zoom_control_active:

            self.zoom_button.config(
                text="ZOOM ON",
                style="PinkOn.TButton"
            )

            self.status_label.config(
                text="Zoom enabled. Use thumb + index distance."
            )

        else:

            self.zoom_button.config(
                text="ZOOM OFF",
                style="PinkOff.TButton"
            )

            self.zoom_factor = 1.0

            self.status_label.config(
                text="Zoom disabled."
            )

    def toggle_motion_detection(self):

        self.motion_detection_active = (
            not self.motion_detection_active
        )

        self.previous_motion_frame = None

        if self.motion_detection_active:

            self.motion_button.config(
                text="MOTION ON",
                style="PinkOn.TButton"
            )

            self.status_label.config(
                text="Motion detection enabled."
            )

        else:

            self.motion_button.config(
                text="MOTION OFF",
                style="PinkOff.TButton"
            )

            self.status_label.config(
                text="Motion detection disabled."
            )

    def toggle_gesture_music(self):

        self.gesture_music_active = (
            not self.gesture_music_active
        )

        if self.gesture_music_active:

            self.music_button.config(
                text="GESTURE MUSIC ON",
                style="PinkOn.TButton"
            )

            self.status_label.config(
                text="Gesture music enabled."
            )

        else:

            self.music_button.config(
                text="GESTURE MUSIC OFF",
                style="PinkOff.TButton"
            )

            if (
                self.audio_process is not None
                and
                self.audio_process.poll() is None
            ):

                self.audio_process.terminate()

            self.status_label.config(
                text="Gesture music disabled."
            )

    # =====================================================
    # SCREENSHOT
    # =====================================================

    def take_screenshot(self):

        if self.current_frame is None:

            messagebox.showwarning(
                "Warning",
                "Start the camera first."
            )

            return

        screenshots_folder = os.path.join(
            self.current_folder,
            "screenshots"
        )

        os.makedirs(
            screenshots_folder,
            exist_ok=True
        )

        file_name = datetime.now().strftime(
            "pink_vision_%Y-%m-%d_%H-%M-%S.jpg"
        )

        full_path = os.path.join(
            screenshots_folder,
            file_name
        )

        cv2.imwrite(
            full_path,
            self.current_frame
        )

        self.status_label.config(
            text=f"Screenshot saved: {file_name}"
        )

    # =====================================================
    # STOP CAMERA
    # =====================================================

    def stop_camera(self):

        self.camera_running = False

        if self.camera is not None:

            self.camera.release()

            self.camera = None

        self.current_frame = None
        self.previous_motion_frame = None
        self.previous_draw_point = None

        self.zoom_factor = 1.0

        self.camera_label.config(
            image="",
            text="CAMERA OFF",
            width=80,
            height=27
        )

        self.camera_label.image = None

        self.faces_label.config(
            text="FACES  0"
        )

        self.hands_label.config(
            text="HANDS  0"
        )

        self.fingers_label.config(
            text="FINGERS  0"
        )

        self.gesture_label.config(
            text="GESTURE  -"
        )

        self.fps_label.config(
            text="FPS  0"
        )

        self.motion_label.config(
            text="MOTION  OFF",
            fg=self.COLOR_GRAY
        )

        self.start_button.config(
            state=tk.NORMAL
        )

        self.stop_button.config(
            state=tk.DISABLED
        )

        self.previous_time = 0

        self.status_label.config(
            text="Camera stopped."
        )

    # =====================================================
    # CLOSE APP
    # =====================================================

    def close_app(self):

        self.stop_camera()

        if (
            self.audio_process is not None
            and
            self.audio_process.poll() is None
        ):

            self.audio_process.terminate()

        self.root.destroy()


root = tk.Tk()

app = FaceDetectionApp(
    root
)

root.mainloop()