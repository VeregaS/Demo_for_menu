import math

import cv2
import mediapipe as mp
import pyautogui
import asyncio

# MEDIAPIPE CONSTS
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# CAM CONSTS
cap = cv2.VideoCapture(0)
w, h = 640, 480
w1, h1 = 1920, 1080
cap.set(3, w)
cap.set(4, h)

# X, Y CONSTS
cf_x, cf_y = w1 / w, h1 / h
mouse_x, mouse_y = 0, 0
shandx, shandy = 0, 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Others
cords, last_status, hand_type = {}, "", ""
hands_detect = True
pyautogui.FAILSAFE = False
smoothening = 2.5
click_recognize_delt = 10
lenght = 0


async def hands_detection():
    global mouse_x, mouse_y, shandx, shandy, lenght
    if hands_detect:
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
                    shandx, shandy = int(cords['12'][0]), int(cords['12'][1])
                    lenght = math.hypot(shandx - mouse_x, shandy - mouse_y)
                    # ______________________________________________________ #
                # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
                await asyncio.sleep(0)


async def hands_func():
    global clocX, clocY, plocY, plocX, shandx, shandy, mouse_y, mouse_x, lenght
    if hands_detect:
        while True:
            x, y = mouse_x * cf_x, mouse_y * cf_y
            clocX = plocX + (x - plocX) / smoothening
            clocY = plocY + (y - plocY) / smoothening
            pyautogui.moveTo(clocX, clocY)
            plocX, plocY = clocX, clocY
            if lenght <= 40:
                pyautogui.click()
            await asyncio.sleep(0)


async def main():
    task1 = asyncio.create_task(hands_detection())
    task2 = asyncio.create_task(hands_func())
    await task1
    await task2

if __name__ == '__main__':
    asyncio.run(main())
