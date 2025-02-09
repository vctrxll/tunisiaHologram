import pyrealsense2 as rs
import numpy as np
import cv2

# Configurar la cámara
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline.start(config)

try:
    while True:
        # Capturar los frames
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        # Convertir la imagen de profundidad a un array de NumPy
        depth_image = np.asanyarray(depth_frame.get_data())

        # Normalizar los valores para que se ajusten al rango
        cv2.imshow('Depth Image - Colorized', depth_colormap)

        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    pipeline.stop()
    cv2.destroyAllWindows()