from math import sqrt
import cv2
import mediapipe as mp  # Importa 'mediapipe' para la detección y el seguimiento de manos.
import open3d as o3d  # Importa la biblioteca 'open3d' para trabajar con modelos 3D.
import os
import platform
import time
import subprocess
import pygame
import pygetwindow as gw
import pygame
import numpy as np
import pygetwindow as gw

pygame.init()


touchcaps = [
    {
        "cap1": (245, 80),
        "cap2": (395, 130),
        "com": ["a"],
        "last": 0,
        "detected": False,
        "timer": 0,
        "title": "Espanol",
    },
    {
        "cap1": (245, 180),
        "cap2": (395, 230),
        "com": ["b"],
        "last": 0,
        "detected": False,
        "timer": 0,
        "title": "Ingles",
    },
    {
        "cap1": (245, 280),
        "cap2": (395, 330),
        "com": ["c"],
        "last": 0,
        "detected": False,
        "timer": 0,
        "title": "Arabe",
    },
    {
        "cap1": (245, 380),
        "cap2": (395, 430),
        "com": ["d"],
        "last": 0,
        "detected": False,
        "timer": 0,
        "title": "Frances",
    },
]


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "render_options.json")
INICIO_PATH = os.path.join(BASE_DIR, "INICIO")
AUDIOS_PATH = os.path.join(BASE_DIR, "AUDIOS")
PIEZAS_PATH = os.path.join(BASE_DIR, "PIEZAS")

archivos = {
    # cara
    0: os.path.join(PIEZAS_PATH, "meshy", "Bearded_Mask_Charm_0112230049_texture.obj"),
    # tres patas
    1: os.path.join(PIEZAS_PATH, "source", "MB7655_119K.obj"),
    # pichinche
    2: os.path.join(PIEZAS_PATH, "amuleto", "17_12_2024.obj"),
    # rojoo
    3: os.path.join(PIEZAS_PATH, "vasijaTunez", "9_1_2025.obj"),
    # rana
    4: os.path.join(PIEZAS_PATH, "armadura", "base_0120171642_texture.obj"),
    5: os.path.join(PIEZAS_PATH, "pieza8", "pieza8.obj"),
    6: os.path.join(PIEZAS_PATH, "pieza10", "pieza10.obj"),  # si
    7: os.path.join(PIEZAS_PATH, "pieza6", "pieza6.obj"),
}

# Diccionario de audios por idioma
audios_por_idioma = {
    "Espanol": {
        0: os.path.join(AUDIOS_PATH, "ESPANOL", "PEDANTE FENICIO DE CRISTAL.mp3"),
        1: os.path.join(AUDIOS_PATH, "ESPANOL", "HERMA CON EL BUSTO DE BACO.mp3"),
        2: os.path.join(AUDIOS_PATH, "ESPANOL", "COLGANTE PUNICO.mp3"),
        3: os.path.join(AUDIOS_PATH, "ESPANOL", "JARRO DE ARCILLA PÚNICO.mp3"),
        4: os.path.join(AUDIOS_PATH, "ESPANOL", "ESCUDO ANTIGUO DE TRES DISCOS.mp3"),
        5: os.path.join(AUDIOS_PATH, "ESPANOL", "8E.mp3"),
        6: os.path.join(AUDIOS_PATH, "ESPANOL", "10E.mp3"),
        7: os.path.join(AUDIOS_PATH, "ESPANOL", "6E.mp3"),
    },
    "Ingles": {
        0: os.path.join(AUDIOS_PATH, "INGLES", "PEDANTE FENICIO DE CRISTAL.mp3"),
        1: os.path.join(AUDIOS_PATH,"INGLES", "HERMA CON EL BUSTO DE BACO.mp3"),
        2: os.path.join(AUDIOS_PATH, "INGLES","COLGANTE PUNICO.mp3"),
        3: os.path.join(AUDIOS_PATH, "INGLES","JARRO DE ARCILLA PÚNICO.mp3"),
        4: os.path.join(AUDIOS_PATH, "INGLES","ESCUDO ANTIGUO DE TRES DISCOS.mp3"),
        5: os.path.join(AUDIOS_PATH, "INGLES","8I.mp3"),
        6: os.path.join(AUDIOS_PATH, "INGLES","10I.mp3"),
        7: os.path.join(AUDIOS_PATH, "INGLES","6I.mp3"),
    },
    "Arabe": {
        0: os.path.join(AUDIOS_PATH, "ARABE","PEDANTE FENICIO DE CRISTAL.mp3"),
        1: os.path.join(AUDIOS_PATH, "ARABE","HERMA CON EL BUSTO DE BACO.mp3"),
        2: os.path.join(AUDIOS_PATH, "ARABE","COLGANTE PUNICO.mp3"),
        3: os.path.join(AUDIOS_PATH, "ARABE","JARRO DE ARCILLA PÚNICO.mp3"),
        4: os.path.join(AUDIOS_PATH, "ARABE","ESCUDO ANTIGUO DE TRES DISCOS.mp3"),
        5: os.path.join(AUDIOS_PATH, "ARABE","8A.mp3"),
        6: os.path.join(AUDIOS_PATH, "ARABE","10A.mp3"),
        7: os.path.join(AUDIOS_PATH, "ARABE","6A.mp3"),
    },
    "Frances": {
        0: os.path.join(AUDIOS_PATH, "FRANCES", "PEDANTE FENICIO DE CRISTAL.mp3"),
        1: os.path.join(AUDIOS_PATH, "FRANCES", "HERMA CON EL BUSTO DE BACO.mp3"),
        2: os.path.join(AUDIOS_PATH, "FRANCES", "COLGANTE PUNICO.mp3"),
        3: os.path.join(AUDIOS_PATH, "FRANCES", "JARRO DE ARCILLA PÚNICO.mp3"),
        4: os.path.join(AUDIOS_PATH, "FRANCES", "ESCUDO ANTIGUO DE TRES DISCOS.mp3"),
        5: os.path.join(AUDIOS_PATH, "FRANCES", "8F.mp3"),
        6: os.path.join(AUDIOS_PATH, "FRANCES", "10F.mp3"),
        7: os.path.join(AUDIOS_PATH, "FRANCES", "6F.mp3"),
    }
}

# Inicialización de variables y configuración
initialState = True
isOpenendWindows = False
objectreadfile = os.path.join(INICIO_PATH, "Green_Circle_0915213601.obj")


isoptimized = "SI"  # Cadena que indica si la optimización está habilitada.
makeoptimize = isoptimized == "SI"  # Convierte la cadena en una variable booleana.

counterMenu = 0
language = ""
contador = 0
cap_width = 640
cap_height = 720
isFullscreen = True

pieceTime = 0


# Cargar el modelo 3D
mesh = o3d.io.read_triangle_mesh(
    objectreadfile, True
)  # Lee el modelo 3D desde el archivo.
# Crear la ventana de visualización del modelo 3D
vis = o3d.visualization.Visualizer()  # Crea un visualizador de Open3D.
vis.create_window(window_name="Open3D", width=960, height=540)
vis.add_geometry(mesh)  # Añade el modelo 3D a la ventana de visualización.
vis.get_render_option().load_from_json(
    json_path
)  # Carga las opciones de renderización desde un archivo JSON.
vis.get_view_control().set_zoom(0.7)  # Establece el nivel de zoom de la vista.
vis.poll_events()  # Procesa los eventos de la ventana.
vis.update_renderer()  # Actualiza el renderizador.

cv2.namedWindow("Idiomas", cv2.WND_PROP_FULLSCREEN)

open3d = gw.getWindowsWithTitle("Open3D")  # Ejemplo con Notepad
menu = gw.getWindowsWithTitle("Idiomas")


if platform.system() == "Linux":
    # Cámaras
    cap = cv2.VideoCapture(0)  # Abre la cámara con optimización (modo DirectShow).

    if isFullscreen:
        # Busca la ventana con título "Open3D"
        window_id = (
            os.popen("wmctrl -l | grep 'Open3D' | awk '{print $1}'").read().strip()
        )
        # Cambia la ventana a pantalla completa
        os.system(f"wmctrl -ir {window_id} -b add,fullscreen")
    print("Se está ejecutando en Linux")
elif platform.system() == "Windows":
    if makeoptimize:  # Verifica si se debe optimizar la captura de video.
        cap = cv2.VideoCapture(
            0 + cv2.CAP_DSHOW
        )  # Abre la cámara con optimización (modo DirectShow).
    else:
        cap = cv2.VideoCapture(0)  # Abre la cámara sin optimización.

    if isFullscreen:
        import win32gui
        import win32con
        import win32api

        hwnd = win32gui.FindWindow(None, "Open3D")
        win32gui.SetWindowLong(
            hwnd, win32con.GWL_STYLE, win32con.WS_POPUP | win32con.WS_VISIBLE
        )
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOP,
            0,
            0,
            win32api.GetSystemMetrics(0),
            win32api.GetSystemMetrics(1),
            win32con.SWP_FRAMECHANGED,
        )
        print("Se está ejecutando en Windows")
else:
    print("Se está ejecutando en otro sistema operativo")

moveX = 0  # Movimiento actual en X.
moveY = 0  # Movimiento actual en Y.
moveZ = 0  # Movimiento actual en Z.
newZ = True  # Bandera para indicar si el movimiento en Z es nuevo.
refZ = 0  # Referencia de posición en Z.
absZ = 0  # Posición absoluta en Z.
downtime = 0

def calc_distance(p1, p2):
    return sqrt(
        (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2
    )  # Calcula la distancia euclidiana entre dos puntos p1 y p2.

def cambiarObj(vis, modelo_viejo, objectreadfile):
    if objectreadfile in archivos.values():
        current_index = list(archivos.values()).index(objectreadfile)
        next_index = (current_index + 1) % len(archivos)
        if current_index == 0:
            pygame.mixer.music.stop()
        audios_cargados[current_index].stop()
        audios_cargados[next_index].play()
        objectreadfile = list(archivos.values())[next_index]
        audioreadfile = list(archivos.values())[next_index]
    else:
        objectreadfile = list(archivos.values())[0]
        audios_cargados[0].play()

    meshNew = o3d.io.read_triangle_mesh(objectreadfile, True)
    vis.remove_geometry(modelo_viejo)
    vis.add_geometry(meshNew)
    vis.get_view_control().set_zoom(0.7)
    # vis.get_view_control().rotate(300, 1200, xo=0.0, yo=0.0)  # Rota la vista del modelo 3D.
    # vis.get_view_control().rotate(1000, 0, xo=0.0, yo=0.0)  # Rota la vista del modelo 3D.
    vis.poll_events()  # Procesa los eventos de la ventana.
    vis.update_renderer()  # Actualiza el renderizador.
    print(f" Pieza cambiada a '{objectreadfile}'")
    # print(f" audio en reproduccion '{audioreadfile}'")
    return objectreadfile, meshNew


def detect_finger_down(hand_landmarks):
    print("-----------------------------")
    finger_down = False
    x_base1 = int(hand_landmarks.landmark[0].x * cap_width)
    y_base1 = int(hand_landmarks.landmark[0].y * cap_height)

    x_base2 = int(hand_landmarks.landmark[17].x * cap_width)
    y_base2 = int(hand_landmarks.landmark[17].y * cap_height)

    x_pinky = int(hand_landmarks.landmark[20].x * cap_width)
    y_pinky = int(hand_landmarks.landmark[20].y * cap_height)

    x_anular = int(hand_landmarks.landmark[16].x * cap_width)
    y_anular = int(hand_landmarks.landmark[16].y * cap_height)

    x_medio = int(hand_landmarks.landmark[12].x * cap_width)
    y_medio = int(hand_landmarks.landmark[12].y * cap_height)

    p1 = (x_base1, y_base1)
    p5 = (x_base2, y_base2)
    p2 = (x_pinky, y_pinky)
    p3 = (x_anular, y_anular)
    p4 = (x_medio, y_medio)
    d_base_base = calc_distance(p1, p5)
    d_base_pinky = calc_distance(p1, p2)
    d_base_anular = calc_distance(p1, p3)
    d_base_medio = calc_distance(p1, p4)
    print(d_base_base)
    print("------------------------------------")
    print("Pinky ", d_base_pinky)
    print("Anular ", d_base_anular)
    print("Medio ", d_base_medio)
    if d_base_anular < 65 and d_base_medio < 65 and d_base_pinky < 65:
        finger_down = True
    print("---------------------")
    return finger_down

print(
    "Ejecutando..."
)  # Imprime un mensaje indicando que el programa está en ejecución.
mp_drawing = (
    mp.solutions.drawing_utils
)  # Inicializa las utilidades de dibujo de MediaPipe.
mp_hands = (
    mp.solutions.hands
)  # Inicializa el módulo de detección de manos de MediaPipe.

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9,
) as hands:
    # Inicia el contexto del modelo de manos de MediaPipe con una confianza mínima de detección de 0.8 y una confianza mínima de seguimiento de 0.5.

    while cap.isOpened():
        # Bucle que se ejecuta mientras la cámara esté abierta.
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frameWidth = image.shape[1]
        frameHeight = image.shape[0]
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        pos = (0, 0)

        # Dibuja un rectángulo negro que cubre toda la imagen.

        totalHands = 0

        if results.multi_handedness:
            totalHands = len(results.multi_handedness)


        # Inicializa el contador de manos detectadas.
        cv2.rectangle(image, pos, (frameWidth, frameHeight), (0, 0, 0), -1)

        hands_inside_regions = [False] * len(touchcaps)

        if results.multi_hand_landmarks:

            if initialState:
                if counterMenu == 0:
                    counterMenu = 1
                    if open3d and menu:
                        #print("Abrir ventana del menu")
                        #open3d[0].minimize()
                        #open3d[0].maximize()
                        menu[0].activate()
                        menu[0].show()


                hand = results.multi_hand_landmarks[0]

                if totalHands == 1:
                    for num, hand in enumerate(results.multi_hand_landmarks):
                        indexTip = results.multi_hand_landmarks[0].landmark[
                            mp_hands.HandLandmark.INDEX_FINGER_TIP
                        ]
                        indexTipXY = mp_drawing._normalized_to_pixel_coordinates(
                            indexTip.x, indexTip.y, frameWidth, frameHeight
                        )

                        thumbTip = results.multi_hand_landmarks[0].landmark[
                            mp_hands.HandLandmark.THUMB_TIP
                        ]
                        thumbTipXY = mp_drawing._normalized_to_pixel_coordinates(
                            thumbTip.x, thumbTip.y, frameWidth, frameHeight
                        )

                        if indexTipXY and thumbTipXY is not None:
                            indexXY = (indexTipXY[0], indexTipXY[1])
                            thumbXY = (thumbTipXY[0], thumbTipXY[1])

                    for i, r in enumerate(touchcaps):
                        # Verificar si el índice está dentro de la región táctil
                        if (
                            r["cap1"][0] < indexXY[0] < r["cap2"][0]
                            and r["cap1"][1] < indexXY[1] < r["cap2"][1]
                        ):
                            if not r["detected"]:  # Si aún no ha sido detectada
                                r["timer"] = time.time()  # Guardar el tiempo de entrada
                                r["detected"] = True  # Marcar la región como detectada

                            # Calcular tiempo transcurrido desde que entró en la región
                            elapsed_time = time.time() - r["timer"]

                            # Generar color dinámico durante los 3 segundos
                            color_factor = int(
                                (elapsed_time % 5) * 85
                            )  # Cambia progresivamente (0 a 255 en 3s)
                            dynamic_color = (
                                0,
                                255 - color_factor,
                                color_factor,
                            )  # Color RGB dinámico

                            # Dibujar un rectángulo de la región con color dinámico
                            enlarged_cap1 = (r["cap1"][0] - 10, r["cap1"][1] - 10)
                            enlarged_cap2 = (r["cap2"][0] + 10, r["cap2"][1] + 10)

                            cv2.rectangle(
                                image,
                                enlarged_cap1,
                                enlarged_cap2,
                                dynamic_color,
                                -1,  # Relleno del rectángulo
                            )

                            # Si han pasado 3 segundos, imprimir el comando una sola vez
                            if elapsed_time >= 5:
                                #print(r["title"])
                                language = r["title"]

                                audios = audios_por_idioma.get(language, {})
                                audios_cargados = {k: pygame.mixer.Sound(v) for k, v in audios.items()}
                                # Imprimir confirmación de carga
                                print(f"Audios cargados para el idioma: {language}")

                                objectreadfile, meshNew = cambiarObj(vis=vis, modelo_viejo=mesh,
                                                                     objectreadfile=objectreadfile)
                                mesh = meshNew
                                r["detected"] = False
                                r["timer"] = None
                                menu[0].hide()
                                #print("cerrar ventada")
                                initialState = False
                        else:
                            # Si el índice sale de la región, se reinicia la detección
                            r["detected"] = False
                            r["timer"] = None

                            # Dibujar la región con borde blanco cuando no está detectada
                            cv2.rectangle(
                                image,
                                r["cap1"],
                                r["cap2"],
                                (255, 255, 255),
                                1,  # Borde blanco sin relleno
                            )

                            # Dibujar los puntos de la mano detectada y sus conexiones en la imagen
                            mp_drawing.draw_landmarks(
                                image,  # Imagen sobre la cual se dibujan las marcas
                                hand,  # Datos de la mano detectada
                                mp_hands.HAND_CONNECTIONS,  # Conexiones entre los puntos de la mano
                                mp_drawing.DrawingSpec(
                                    color=(121, 22, 76),
                                    thickness=2,
                                    circle_radius=4,  # Estilo de las conexiones
                                ),
                                mp_drawing.DrawingSpec(
                                    color=(250, 44, 250),
                                    thickness=2,
                                    circle_radius=2,  # Estilo de los puntos
                                ),
                            )
            else:
                pieceTime += 1
                downtime = 1

                for hand_landmarks in results.multi_hand_landmarks:
                    if pieceTime >= 25:
                        if detect_finger_down(hand_landmarks):
                            objectreadfile, meshNew = cambiarObj(vis=vis, modelo_viejo=mesh,
                                                                 objectreadfile=objectreadfile)
                            mesh = meshNew
                            pieceTime = 0

                if totalHands == 1:
                    for num, hand in enumerate(results.multi_hand_landmarks):
                        indexTip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        indexTipXY = mp_drawing._normalized_to_pixel_coordinates(indexTip.x, indexTip.y, frameWidth,
                                                                                 frameHeight)
                        thumbTip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP]
                        thumbTipXY = mp_drawing._normalized_to_pixel_coordinates(thumbTip.x, thumbTip.y, frameWidth,
                                                                                 frameHeight)

                        mp_drawing.draw_landmarks(
                            image,
                            hand,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                            mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                        )
                        # Normaliza las coordenadas de los puntos de la mano a las coordenadas del píxel en la imagen.

                        if indexTipXY and thumbTipXY is not None:
                            indexXY = (indexTipXY[0], indexTipXY[1])
                            thumbXY = (thumbTipXY[0], thumbTipXY[1])
                            dist = calc_distance(indexXY, thumbXY)
                            # Dibuja círculos en la punta del índice y el pulgar y calcula la distancia entre ellos.

                            # Movimiento de la piezas con las manos
                            if dist < 20:
                                netX = round((indexTipXY[0] + thumbTipXY[0]) / 2)
                                netY = round((indexTipXY[1] + thumbTipXY[1]) / 2)

                                deltaX = moveX - netX
                                moveX = netX
                                deltaY = moveY - netY
                                moveY = netY
                                if abs(deltaX) > 40 or abs(deltaY) > 40:
                                    print("Max reached: " + str(deltaX) + "," + str(deltaY))
                                else:
                                    # print(str(deltaX) + "," + str(deltaY))
                                    vis.get_view_control().rotate(deltaX * 8, -deltaY * 8, xo=0.0, yo=0.0)
                                    vis.poll_events()
                                    vis.update_renderer()
                                # Si la distancia es menor que 50, mueve la vista del modelo 3D de acuerdo con los movimientos detectados.
                            # No hacer movimiento
                            else:
                                moveX = 0
                                moveY = 0
                                # Si la distancia es mayor que 50, reinicia los movimientos.
                elif totalHands == 2:
                    handX = [0, 0]
                    handY = [0, 0]
                    isHands = [False, False]
                    # Inicializa las posiciones de las manos y las banderas para la detección.

                    for num, hand in enumerate(results.multi_hand_landmarks):
                        indexTip = results.multi_hand_landmarks[num].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        indexTipXY = mp_drawing._normalized_to_pixel_coordinates(indexTip.x, indexTip.y, frameWidth,
                                                                                 frameHeight)
                        thumbTip = results.multi_hand_landmarks[num].landmark[mp_hands.HandLandmark.THUMB_TIP]
                        thumbTipXY = mp_drawing._normalized_to_pixel_coordinates(thumbTip.x, thumbTip.y, frameWidth,
                                                                                 frameHeight)
                        # Normaliza las coordenadas de los puntos de la mano a las coordenadas del píxel en la imagen.

                        if indexTip and indexTipXY and thumbTipXY is not None:
                            indexXY = (indexTipXY[0], indexTipXY[1])
                            thumbXY = (thumbTipXY[0], thumbTipXY[1])
                            dist = calc_distance(indexXY, thumbXY)
                            # Dibuja círculos en la punta del índice y el pulgar y calcula la distancia entre ellos.

                            if dist < 50:
                                netX = round((indexTipXY[0] + thumbTipXY[0]) / 2)
                                netY = round((indexTipXY[1] + thumbTipXY[1]) / 2)
                                handX[num] = netX
                                handY[num] = netY
                                isHands[num] = True
                                # Si la distancia es menor que 50, guarda las posiciones promedio de los puntos detectados.

                        # print(isHands[0], ",", isHands[1])
                        if isHands[0] and isHands[1]:
                            distpar = calc_distance((handX[0], handY[0]), (handX[1], handY[1]))
                            if newZ:
                                newZ = False
                                moveZ = distpar
                                refZ = distpar

                            netX = round((handX[0] + handX[1]) / 2)
                            netY = round((handY[0] + handY[1]) / 2)
                            deltaZ = (distpar - moveZ) / refZ
                            if deltaZ < abs(1):
                                absZ = absZ - deltaZ
                                if absZ > 2.0:
                                    absZ = 2.0
                                elif absZ < 0.6:
                                    absZ = 0.6
                                moveZ = distpar
                                print(absZ)
                                vis.get_view_control().set_zoom(absZ)
                                vis.poll_events()
                                vis.update_renderer()
                            # Si se detectan ambas manos, calcula la distancia entre ellas y ajusta el zoom del modelo 3D en función de esa distancia.

                        elif not isHands[0] and not isHands[1]:
                            newZ = True

        # Recorre todas las regiones táctiles para dibujar sus bordes y mostrar sus títulos en la imagen
        for r in touchcaps:
            # Dibuja un rectángulo blanco alrededor de cada región táctil
            cv2.rectangle(image, r["cap1"], r["cap2"], (255, 255, 255), 1)

            # Calcula la posición del texto (título de la región) centrado dentro del rectángulo
            title_position_x = (r["cap1"][0] + r["cap2"][0]) // 2 - len(r["title"]) * 5
            title_position_y = (r["cap1"][1] + r["cap2"][1]) // 2 + 5  # Ajuste vertical

            # Dibuja el texto del título dentro de la región táctil
            cv2.putText(
                image,
                r["title"],  # Texto del título
                (title_position_x, title_position_y),  # Posición calculada
                cv2.FONT_HERSHEY_SIMPLEX,  # Tipo de fuente
                0.6,  # Tamaño del texto
                (255, 255, 255),  # Color blanco
                1,  # Grosor de la línea del texto
            )

        else:
            ctrl = vis.get_view_control()
            ctrl.rotate(3, 0, xo=0.0, yo=0.0)
            vis.poll_events()
            vis.update_renderer()

            if downtime >= 1:
                if downtime >= 2000:
                    for key in audios:
                        pygame.mixer.music.stop()
                        audios_cargados[key].stop()
                    vis.remove_geometry(mesh)
                    audios_cargados = None
                    objectreadfile = os.path.join(INICIO_PATH, "Green_Circle_0915213601.obj")
                    mesh = o3d.io.read_triangle_mesh(objectreadfile, True)
                    mesh.compute_vertex_normals()
                    vis.add_geometry(mesh)
                    vis.get_view_control().set_zoom(0.7)
                    vis.poll_events()  # Procesa los eventos de la ventana.
                    vis.update_renderer()  # Actualiza el renderizador.
                    downtime = 0
                    initialState = True
                    counterMenu = 0
                    print("Regresar inicio")
                else:
                    downtime += 1


        if counterMenu >= 1:
            if counterMenu >= 500:
                menu[0].hide()
                counterMenu = 0
                #print("Cerrar ventana del menu")
            elif initialState:
                counterMenu += 1

        cv2.imshow("Idiomas", image)

        if cv2.waitKey(5) & 0xFF == ord("q"):
            print("Programa cerrado por el usuario.")
            break

        # Si no está activado el modo de pantalla completa, muestra la imagen en una ventana de OpenCV

cap.release()
vis.destroy_window()
cv2.destroyAllWindows()
