import cv2
import mediapipe as mp
import time
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

w1, h1 = 1920, 1080
w, h = 640, 480
cf_x = w1 / w
cf_y = h1 / h
cap.set(3, w)
cap.set(4, h)

cords = {}
pTime = 0
last_status, hand_type = "", ""

with mp_hands.Hands(max_num_hands=1, min_tracking_confidence=0.9, min_detection_confidence=0.9) as hands:
    while True:

        # ------------------------- Camera Load --------------------- #
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        # ----------------------------------------------------------- #
        #############################################################

        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        imgRGB = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:

            # +++++++++++++++++++++++++ Hand_Type +++++++++++++++++++++++++++ #
            if results.multi_handedness:
                hand_type = results.multi_handedness[0].classification[0].label
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

            # ======================== Hand_Draw ============================ #
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(imgRGB, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0, 0, 255)),
                                          mp_drawing.DrawingSpec(color=(0, 0, 0)))

            # =============================================================== #

                # ----------------------- Hand_Cords ------------------------ #
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cords[f"{id}"] = cx, cy
                # ----------------------------------------------------------- #

                # ######################## Hand_Status ###################### #
                pyautogui.moveTo(int(cords['8'][0]) * cf_x, int(cords['8'][1]) * cf_y)
                ###############################################################
        else:
            hand_type = "-"
            last_status = "-"

        if cv2.waitKey(1) == 27:
            break

cap.release()
cv2.destroyAllWindows()
