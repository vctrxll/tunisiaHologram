import pyrealsense2 as rs
import numpy as np
import cv2
import mediapipe as mp

# Inicializar la detección de manos de MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Configurar la cámara RealSense
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convertir a NumPy array
        frame = np.asanyarray(color_frame.get_data())

        # Convertir BGR a RGB (MediaPipe usa RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesar la detección de manos
        results = hands.process(frame_rgb)

        # Dibujar las manos detectadas
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Mostrar el frame
        cv2.imshow("RealSense Hand Tracking", frame)

        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    pipeline.stop()
    cv2.destroyAllWindows()
