# pip install opencv-contrib-python
# pip install cvzone
# pip install threading
# pip install pyautogui

import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.HandTrackingModule import HandDetector
import threading
import time
import pyautogui

camera_index = 0

cap = cv2.VideoCapture(camera_index)
cap.set(3, 640)
cap.set(4, 480)

fpsReader = cvzone.FPS()
detector1 = FaceMeshDetector(maxFaces=1)
detector2 = HandDetector(maxHands=2, detectionCon=0.75)

go_right = 0
go_left = 0
go_up = 0
go_down = 0
ges_ctrl_track = 0
gesture_on = None
misle_coldwn = 0
flare_coldwn = 0
fire_on = 0
booster_coldwn = 0


def ges_enable():
    global gesture_on
    global gesture_on_thread
    time.sleep(3)
    gesture_on = 1
    print("Gesture Control On")
    gesture_on_thread = threading.Thread(target=ges_enable)


def misle_cooldown_func():
    global misle_coldwn
    global misle_coldwn_thread
    time.sleep(2)
    misle_coldwn = 0
    print("Missle reloaded")
    misle_coldwn_thread = threading.Thread(target=misle_cooldown_func)


def flare_coldwn_func():
    global flare_coldwn
    global flare_coldwn_thread
    time.sleep(2)
    flare_coldwn = 0
    print("Flares reloaded")
    flare_coldwn_thread = threading.Thread(target=flare_coldwn_func)


def booster_coldwn_func():
    global booster_coldwn
    global booster_coldwn_thread
    time.sleep(2)
    booster_coldwn = 0
    print("Boosters cooling down")
    booster_coldwn_thread = threading.Thread(target=booster_coldwn_func)


gesture_on_thread = threading.Thread(target=ges_enable)
misle_coldwn_thread = threading.Thread(target=misle_cooldown_func)
flare_coldwn_thread = threading.Thread(target=flare_coldwn_func)
booster_coldwn_thread = threading.Thread(target=booster_coldwn_func)

def aircraft_gesture():
    global cap
    global fpsReader
    global detector1
    global detector2
    global go_right
    global go_left
    global go_up
    global go_down
    global ges_ctrl_track
    global gesture_on
    global misle_coldwn
    global flare_coldwn
    global fire_on
    global booster_coldwn

    while True:
        _, img = cap.read()
        img = cv2.flip(img, 1)
        img, faces = detector1.findFaceMesh(img, draw=False)

        if faces:
            ctrl_x, ctrl_y = faces[0][168][0], faces[0][168][1]
            left_x, left_y = faces[0][57][0] + 10, faces[0][57][1]
            right_x, right_y = faces[0][287][0] - 10, faces[0][287][1]

            cv2.circle(img, (ctrl_x, ctrl_y), 5, (255, 255, 0), 2)
            cv2.circle(img, (left_x, left_y), 5, (255, 255, 0), 2)
            cv2.circle(img, (right_x, right_y), 5, (255, 255, 0), 2)
            cv2.line(img, (ctrl_x, 0), (ctrl_x, 1000), (255, 255, 255), 2)
            cv2.line(img, (0, ctrl_y), (1000, ctrl_y), (255, 255, 255), 2)

            hands, img = detector2.findHands(img, draw=True, flipType=False)
            if len(hands) == 2:
                if hands[0]['type'] == "Left":
                    hands_l, hands_r = hands[0], hands[1]
                else:
                    hands_l, hands_r = hands[1], hands[0]

                lmlist_l, lmlist_r = hands_l['lmList'], hands_r['lmList']

                r_idx_x, r_idx_y = lmlist_r[6][0], lmlist_r[6][1]
                l_idx_x, l_idx_y = lmlist_l[6][0], lmlist_l[6][1]
                r_thmb_x, r_thmb_y = lmlist_r[4][0], lmlist_r[4][1]
                l_thmb_x, l_thmb_y = lmlist_l[4][0], lmlist_l[4][1]

                cv2.circle(img, (r_idx_x, r_idx_y), 5, (0, 255, 255), 2)
                cv2.circle(img, (l_idx_x, l_idx_y), 5, (0, 255, 255), 2)
                cv2.circle(img, (r_thmb_x, r_thmb_y), 5, (0, 255, 255), 2)
                cv2.circle(img, (l_thmb_x, l_thmb_y), 5, (0, 255, 255), 2)

                l_fing_upno = detector2.fingersUp(hands_l)
                r_fing_upno = detector2.fingersUp(hands_r)

                if l_fing_upno[0] == 1 and l_fing_upno[4] == 1 and r_fing_upno[0] == 1 and r_fing_upno[4] == 1 and sum(l_fing_upno) == 2 and sum(r_fing_upno) == 2 and ges_ctrl_track == 0:
                    print("Gesture Enabled")
                    updwn_line_control = ctrl_y
                    ges_ctrl_track = 1
                    gesture_on_thread.start()

        if gesture_on == 1:
            cv2.line(img, (0, updwn_line_control),
                    (1000, updwn_line_control), (255, 0, 255), 2)

            # Aircraft Moving Up
            if abs(updwn_line_control - ctrl_y) > 20 and updwn_line_control > ctrl_y and go_up == 0:
                pyautogui.keyDown('W')
                go_up = 1
                print("Going Up")
            elif abs(updwn_line_control - ctrl_y) < 20 and updwn_line_control > ctrl_y and go_up == 1:
                pyautogui.keyUp('W')
                go_up = 0

            # Aircraft Moving down
            if abs(updwn_line_control - ctrl_y) > 35 and updwn_line_control < ctrl_y and go_down == 0:
                pyautogui.keyDown('S')
                go_down = 1
                print("Going Down")
            elif abs(updwn_line_control - ctrl_y) < 35 and updwn_line_control < ctrl_y and go_down == 1:
                pyautogui.keyUp('S')
                go_down = 0

            # Moving the Aircraft to the Right
            if right_x < ctrl_x and go_right == 0:
                pyautogui.keyDown('D')
                go_right = 1
                print('Going Right')

            # Moving the Aircraft to the Left
            elif left_x > ctrl_x and go_left == 0:
                pyautogui.keyDown('A')
                go_left = 1
                print('Going Left')

            # Keeping Aircraft Straight
            elif right_x > ctrl_x and left_x < ctrl_x:
                if go_right == 1:
                    pyautogui.keyUp('D')
                    go_right = 0
                if go_left == 1:
                    pyautogui.keyUp('A')
                    go_left = 0

            # Missile Launch
            if abs(r_thmb_y - r_idx_y) < 30 and abs(l_thmb_y - l_idx_y) < 30 and misle_coldwn == 0:
                misle_coldwn = 1
                print("Missile Launched")
                pyautogui.press("up")
                misle_coldwn_thread.start()

            # Flares Deploying
            elif abs(r_thmb_y - r_idx_y) > 30 and abs(l_thmb_y - l_idx_y) < 30 and flare_coldwn == 0:
                flare_coldwn = 1
                print("Flares Deployed")
                pyautogui.press("down")
                flare_coldwn_thread.start()

            # Aircraft's Gun Fire
            elif abs(r_thmb_y - r_idx_y) < 30 and abs(l_thmb_y - l_idx_y) > 30 and fire_on == 0:
                pyautogui.keyDown("left")
                fire_on = 1
                print("Gun Firing..........")
            if abs(r_thmb_y - r_idx_y) > 30 and fire_on == 1:
                pyautogui.keyUp("left")
                fire_on = 0
                print("Firing stopped")

            # Engaging Speed Boosters
            if abs(r_idx_x - l_idx_x) < 50 and booster_coldwn == 0:
                pyautogui.press("right")
                booster_coldwn = 1
                print("Booster Engaged")
                booster_coldwn_thread.start()

        fps, img = fpsReader.update(
            img, pos=(50, 80), color=(0, 255, 0), scale=5, thickness=5)
        cv2.imshow("Camera Feed", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break