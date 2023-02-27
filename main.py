import cv2
import mediapipe as mp
import pyautogui
import asyncio

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
mouse_x = 0
mouse_y = 0


def main():
    global mouse_x, mouse_y
    with mp_hands.Hands(max_num_hands=1, min_tracking_confidence=0.7, min_detection_confidence=0.7) as hands:
        while True:

            # ------------------------- Camera Load --------------------- #
            success, frame = cap.read()
            frame = cv2.flip(frame, 1)
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            # ----------------------------------------------------------- #

            # ++++++++++++++++++++++ Main body +++++++++++++++++++++++++++++ #
            if results.multi_hand_landmarks:

                # ================== Finger Pos ======================== #
                for hand_landmarks in results.multi_hand_landmarks:
                    for id, lm in enumerate(hand_landmarks.landmark):
                        h, w, c = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cords[f"{id}"] = cx, cy
                # ====================================================== #

                # _____________________Mouse____________________________ #
                mouse_x, mouse_y = int(cords['8'][0]), int(cords['8'][1])
                pyautogui.moveTo(mouse_x * cf_x, mouse_y * cf_y)
                # ______________________________________________________ #
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


if __name__ == '__main__':
    asyncio.run(main())
