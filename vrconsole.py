import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.HandTrackingModule import HandDetector
from cvzone.PoseModule import PoseDetector

import threading

import time
import pyautogui
import numpy as np
import mouse
import mediapipe as mp
import pandas as pd


exit_status = -1
go_right = 0
go_left = 0
go_up = 0
go_down = 0
ges_ctrl_track = 0
gesture_on = None
misle_coldwn = 0
flare_coldwn = 0
fire_on = 0
booster_coldwn =0
def exit_stat_change():
    global exit_status
    print("change")
    exit_status = 0
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


def activate(mode,mode_ctrl_state):
    cap = cv2.VideoCapture(1)
    cam_w, cam_h = 640, 480
    cap.set(3, cam_w)
    cap.set(4, cam_h)
    frameR = 100
    global go_right, go_left, go_up, go_down, ges_ctrl_track, gesture_on, misle_coldwn, flare_coldwn,fire_on, booster_coldwn
    global gesture_on_thread, misle_coldwn_thread, flare_coldwn_thread, booster_coldwn_thread
    global exit_status
    charac_pos = [0, 1, 0]
    index_pos = 1
    fixedx = None
    fixedy = None
    rec = None

    ######## Csv Control Files ################
    df_flight = pd.read_csv("flight_ctrl.csv")
    df_sub = pd.read_csv("sub_ctrl.csv")
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
    print("load")
    fpsReader = cvzone.FPS()
    face_detect = FaceMeshDetector(maxFaces=1)
    hand_detect = HandDetector(maxHands=2, detectionCon=0.75)
    pose_detect = PoseDetector()
    exit_status = -1
    while True:
        print(exit_status)
        success, img = cap.read()
        if success:
            img = cv2.flip(img, 1)

            #Aircraft
            if mode== 3:
                img, faces = face_detect.findFaceMesh(img, draw=False)

                if faces:
                    ctrl_x, ctrl_y = faces[0][168][0], faces[0][168][1]
                    left_x, left_y = faces[0][57][0] + 10, faces[0][57][1]
                    right_x, right_y = faces[0][287][0] - 10, faces[0][287][1]

                    cv2.circle(img, (ctrl_x, ctrl_y), 5, (255, 255, 0), 2)
                    cv2.circle(img, (left_x, left_y), 5, (255, 255, 0), 2)
                    cv2.circle(img, (right_x, right_y), 5, (255, 255, 0), 2)
                    cv2.line(img, (ctrl_x, 0), (ctrl_x, 1000), (255, 255, 255), 2)
                    cv2.line(img, (0, ctrl_y), (1000, ctrl_y), (255, 255, 255), 2)

                    hands, img = hand_detect.findHands(img, draw=True, flipType=False)
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

                        l_fing_upno = hand_detect.fingersUp(hands_l)
                        r_fing_upno = hand_detect.fingersUp(hands_r)

                        if l_fing_upno[0] == 1 and l_fing_upno[4] == 1 and r_fing_upno[0] == 1 and r_fing_upno[4] == 1 and \
                                sum(l_fing_upno) == 2 and sum(r_fing_upno) == 2 and ges_ctrl_track == 0:
                            updwn_line_control = ctrl_y
                            ges_ctrl_track = 1
                            print("Gesture Enabled")
                            gesture_on_thread.start()

                if gesture_on == 1:
                    cv2.line(img, (0, updwn_line_control), (1000, updwn_line_control), (255, 0, 255), 2)

                    # Aircraft Moving Up
                    if abs(updwn_line_control - ctrl_y) > 20 and updwn_line_control > ctrl_y and go_up == 0:
                        pyautogui.keyDown(df_flight["up"][mode_ctrl_state])
                        go_up = 1
                        print("Going Up")
                    elif abs(updwn_line_control - ctrl_y) < 20 and updwn_line_control > ctrl_y and go_up == 1:
                        pyautogui.keyUp(df_flight["up"][mode_ctrl_state])
                        go_up = 0

                    # Aircraft Moving down
                    if abs(updwn_line_control - ctrl_y) > 35 and updwn_line_control < ctrl_y and go_down == 0:
                        pyautogui.keyDown(df_flight["down"][mode_ctrl_state])
                        go_down = 1
                        print("Going Down")
                    elif abs(updwn_line_control - ctrl_y) < 35 and updwn_line_control < ctrl_y and go_down == 1:
                        pyautogui.keyUp(df_flight["down"][mode_ctrl_state])
                        go_down = 0

                    # Moving the Aircraft to the Right
                    if right_x < ctrl_x and go_right == 0:
                        pyautogui.keyDown(df_flight["right"][mode_ctrl_state])
                        go_right = 1
                        print('Going Right')

                    # Moving the Aircraft to the Left
                    elif left_x > ctrl_x and go_left == 0:
                        pyautogui.keyDown(df_flight["left"][mode_ctrl_state])
                        go_left = 1
                        print('Going Left')

                    # Keeping Aircraft Straight
                    elif right_x > ctrl_x and left_x < ctrl_x:
                        if go_right == 1:
                            pyautogui.keyUp(df_flight["right"][mode_ctrl_state])
                            go_right = 0
                        if go_left == 1:
                            pyautogui.keyUp(df_flight["left"][mode_ctrl_state])
                            go_left = 0

                    # Missile Launch
                    if abs(r_thmb_y - r_idx_y) < 30 and abs(l_thmb_y - l_idx_y) < 30 and misle_coldwn == 0:
                        misle_coldwn = 1
                        print("Missile Launched")
                        pyautogui.press(df_flight["missiles"][mode_ctrl_state])
                        misle_coldwn_thread.start()

                    # Flares Deploying
                    elif abs(r_thmb_y - r_idx_y) > 30 and abs(l_thmb_y - l_idx_y) < 30 and flare_coldwn == 0:
                        flare_coldwn = 1
                        print("Flares Deployed")
                        pyautogui.press(df_flight["flares"][mode_ctrl_state])
                        flare_coldwn_thread.start()


                    # Aircraft's Gun Fire
                    elif abs(r_thmb_y - r_idx_y) < 30 and abs(l_thmb_y - l_idx_y) > 30 and fire_on == 0:
                        pyautogui.keyDown(df_flight["gun_fire"][mode_ctrl_state])
                        fire_on = 1
                        print("Gun Firing..........")
                    if abs(r_thmb_y - r_idx_y) > 30 and fire_on == 1:
                        pyautogui.keyUp(df_flight["left"][mode_ctrl_state])
                        fire_on = 0
                        print("Firing stopped")

                    # Engaging Speed Boosters
                    if abs(r_idx_x - l_idx_x) < 50 and booster_coldwn == 0:
                        pyautogui.press(df_flight["boosters"][mode_ctrl_state])
                        booster_coldwn = 1
                        print("Booster Engaged")
                        booster_coldwn_thread.start()

                fps, img = fpsReader.update(img, pos=(50, 80), color=(0, 255, 0), scale=5, thickness=5)
                cv2.imshow("Camera Feed", img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            #Fruit Ninja
            elif mode == 1:
                hands, img = hand_detect.findHands(img)
                cv2.rectangle(img, (frameR, frameR), (cam_w - frameR, cam_h - frameR), (255, 0, 255), 2)
                if hands:
                    lmlist = hands[0]['lmList']
                    ind_x, ind_y = lmlist[8][0], lmlist[8][1]
                    cv2.circle(img, (ind_x, ind_y), 5, (0, 255, 255), 2)
                    conv_x = int(np.interp(ind_x, (frameR, cam_w - frameR), (0, 1920)))
                    conv_y = int(np.interp(ind_y, (frameR, cam_h - frameR), (0, 1080)))
                    mouse.move(conv_x, conv_y)
                    fingers = hand_detect.fingersUp(hands[0])
                    if fingers[4] == 1:
                        pyautogui.mouseDown()
                cv2.imshow("Camera Feed", img)
                cv2.waitKey(1)

            #Hillclimb
            elif mode == 4:
                hand, img = hand_detect.findHands(img)
                if hand and hand[0]["type"] == "Left":
                    fingers = hand_detect.fingersUp(hand[0])
                    totalFingers = fingers.count(1)
                    print(totalFingers)
                    cv2.putText(img, f'Fingers:{totalFingers}', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    if totalFingers == 5:
                        pyautogui.keyDown("right")
                        pyautogui.keyUp('left')
                    if totalFingers == 0:
                        pyautogui.keyDown("left")
                        pyautogui.keyUp("right")
                cv2.imshow('Camera Feed', img)
                cv2.waitKey(1)

            #Subway
            elif mode == 2:
                img = cv2.resize(img, (440, 330))
                height, width, channel = img.shape
                width_hf = int(width / 2)
                height_hf = int(height / 2)
                img = pose_detect.findPose(img, draw=False)
                lmList, bboxInfo = pose_detect.findPosition(img, bboxWithHands=False, draw=False)
                # Extracting Shoulder Landmarks
                if lmList:
                    right_x = lmList[11][1] - 7
                    right_y = lmList[11][2]
                    cv2.circle(img, (right_x, right_y), 5, (0, 0, 0), 2)
                    left_x = lmList[12][1] + 7
                    left_y = lmList[12][2]
                    cv2.circle(img, (left_x, left_y), 5, (0, 0, 0), 2)
                    # cv2.line(img, (left_x,left_y), (right_x,right_y), (255, 0, 255), 2)
                    mid_x = left_x + int(abs(right_x - left_x) / 2)
                    mid_y = int(abs(right_y + left_y) / 2)
                    # cv2.circle(img, (mid_x, mid_y), 2, (255, 255, 0), 2)
                    if rec != None:
                        # Sideways movement command
                        if right_x < width_hf and index_pos > 0 and charac_pos[index_pos - 1] == 0:
                            charac_pos[index_pos] = 0
                            charac_pos[index_pos - 1] = 1
                            pyautogui.press(df_sub["left"][mode_ctrl_state])
                            index_pos -= 1
                            print("Left key")
                            print(charac_pos)
                        if left_x > width_hf and index_pos < 2 and charac_pos[index_pos + 1] == 0:
                            print("Right key")
                            charac_pos[index_pos] = 0
                            charac_pos[index_pos + 1] = 1
                            pyautogui.press(df_sub["right"][mode_ctrl_state])
                            index_pos += 1
                            print(charac_pos)
                        if right_x > width_hf and left_x < width_hf and index_pos == 0:
                            charac_pos[index_pos] = 0
                            charac_pos[index_pos + 1] = 1
                            index_pos += 1
                            pyautogui.press(df_sub["right"][mode_ctrl_state])
                            print(charac_pos)
                            print('left to center')
                        if right_x > width_hf and left_x < width_hf and index_pos == 2:
                            charac_pos[index_pos] = 0
                            charac_pos[index_pos - 1] = 1
                            index_pos -= 1
                            pyautogui.press(df_sub["left"][mode_ctrl_state])
                            print('right to center')
                            print(charac_pos)
                hands, img = hand_detect.findHands(img, draw=True, flipType=False)
                if len(hands) == 2:
                    if hands[0]['type'] == "Left":
                        hands_l, hands_r = hands[0], hands[1]
                    else:
                        hands_l, hands_r = hands[1], hands[0]

                    lmlist_l, lmlist_r = hands_l['lmList'], hands_r['lmList']

                    fingers_left = hand_detect.fingersUp(hands_l)
                    fingers_right = hand_detect.fingersUp(hands_r)  # Command to Start the game

                    # print(fingers_left,fingers_right)
                    if fingers_right.count(1) == 3 and fingers_left.count(1) == 3 and fingers_right[1] == 1 and fingers_right[
                        2] == 1 and fingers_left[1] == 1 and fingers_left[1] == 1:
                        fixedx = left_x + int(abs(right_x - left_x) / 2)
                        fixedy = int(abs(right_y + left_y) / 2)
                        rec = 35
                        pyautogui.press('space')

                    # Up and Down command
                if fixedy is not None:
                    if (mid_y - fixedy) <= -24:
                        pyautogui.press(df_sub["up"][mode_ctrl_state])
                        print('jump')
                    elif (mid_y - fixedy) >= 40:
                        pyautogui.press(df_sub["down"][mode_ctrl_state])
                        print('down')
                center_arrow = 10
                cv2.circle(img, (width_hf, height_hf), 2, (0, 255, 255), 2)
                cv2.line(img, (width_hf, height_hf - center_arrow), (width_hf, height_hf + center_arrow), (0, 255, 0), 2)
                cv2.line(img, (width_hf - center_arrow, height_hf), (width_hf + center_arrow, height_hf), (0, 255, 0), 2)
                # Lines to be crossed to detect up and down movement
                # if rec is not None:
                #     cv2.line(img, (0, fixedy), (width, fixedy), (0, 0, 0), 2)
                #     cv2.line(img, (0, fixedy - 24), (width, fixedy - 24), (0, 0, 0), 2)
                #     cv2.line(img, (0, fixedy + rec), (width, fixedy + rec), (0, 0, 0), 2)

                cv2.imshow('Subway Surfers', img)
                cv2.waitKey(1)
            # jump
            elif mode == 5:
                img = cv2.resize(img, (440, 330))
                height, width, channel = img.shape
                width_hf = int(width / 2)
                height_hf = int(height / 2)
                img = pose_detect.findPose(img, draw=False)
                lmList, bboxInfo = pose_detect.findPosition(img, bboxWithHands=False, draw=False)
                # Extracting Shoulder Landmarks
                if lmList:
                    right_x = lmList[11][1] - 7
                    right_y = lmList[11][2]
                    cv2.circle(img, (right_x, right_y), 5, (0, 0, 0), 2)
                    left_x = lmList[12][1] + 7
                    left_y = lmList[12][2]
                    cv2.circle(img, (left_x, left_y), 5, (0, 0, 0), 2)
                    mid_x = left_x + int(abs(right_x - left_x) / 2)
                    mid_y = int(abs(right_y + left_y) / 2)

                hands, img = hand_detect.findHands(img, draw=True, flipType=False)
                if len(hands) == 2:
                    if hands[0]['type'] == "Left":
                        hands_l, hands_r = hands[0], hands[1]
                    else:
                        hands_l, hands_r = hands[1], hands[0]

                    lmlist_l, lmlist_r = hands_l['lmList'], hands_r['lmList']

                    fingers_left = hand_detect.fingersUp(hands_l)
                    fingers_right = hand_detect.fingersUp(hands_r)  # Command to Start the game

                    # print(fingers_left,fingers_right)
                    if fingers_right.count(1) == 3 and fingers_left.count(1) == 3 and fingers_right[1] == 1 and \
                            fingers_right[
                                2] == 1 and fingers_left[1] == 1 and fingers_left[1] == 1:
                        fixedx = left_x + int(abs(right_x - left_x) / 2)
                        fixedy = int(abs(right_y + left_y) / 2)
                        rec = 35
                        pyautogui.press('space')

                    # Up and Down command
                if fixedy is not None:
                    if (mid_y - fixedy) <= -24:
                        pyautogui.press(df_sub["up"][mode_ctrl_state])
                        print('jump')
                    elif (mid_y - fixedy) >= 40:
                        pyautogui.press(df_sub["down"][mode_ctrl_state])
                        print('down')

                center_arrow = 10
                cv2.circle(img, (width_hf, height_hf), 2, (0, 255, 255), 2)
                cv2.line(img, (width_hf, height_hf - center_arrow), (width_hf, height_hf + center_arrow), (0, 255, 0), 2)
                cv2.line(img, (width_hf - center_arrow, height_hf), (width_hf + center_arrow, height_hf), (0, 255, 0), 2)
                # Lines to be crossed to detect up and down movement
                # if rec is not None:
                #     cv2.line(img, (0, fixedy), (width, fixedy), (0, 0, 0), 2)
                #     cv2.line(img, (0, fixedy - 24), (width, fixedy - 24), (0, 0, 0), 2)
                #     cv2.line(img, (0, fixedy + rec), (width, fixedy + rec), (0, 0, 0), 2)

                cv2.imshow('Subway Surfers', img)
                cv2.waitKey(1)


        if exit_status ==0:
            cap.release()
            cv2.destroyAllWindows()
            break
