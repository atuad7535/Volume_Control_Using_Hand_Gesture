import cv2
import numpy as np
import pandas as pd
import time
import Hand_Module as hm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

'''
Mediapipe : https://google.github.io/mediapipe/solutions/hands.html

https://github.com/AndreMiras/pycaw For making changing volume
'''

new_frame_time = 0
prev_frame_time = 0
cap = cv2.VideoCapture(1)
detector = hm.hand_Detector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volume_range = volume.GetVolumeRange()  # Orignal range(0, -65) 0 is 100%
# volume.SetMasterVolumeLevel(0, None)
min_vol = volume_range[0]
max_vol = volume_range[1]
vol = 0
vol_bar = 400
vol_percent = 0

while True:

    ret, frame = cap.read()
    frame = detector.find_hands(frame)
    landmark_list = detector.find_position(
        frame)  # will take index value 4 and 8 which represents tip of thumb and tip of index finger

    if len(landmark_list) != 0:
        # print(landmark_list[4], landmark_list[8])

        x1, y1 = landmark_list[4][1], landmark_list[4][2]
        x2, y2 = landmark_list[8][1], landmark_list[8][2]

        # To Specify correct position of thumb and index finger
        cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 10, (255, 0, 255), cv2.FILLED)

        # Drawing center if line
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Drawing line between 2 points
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), cv2.FILLED)  # https://www.rapidtables.com/web/color/RGB_Color.html

        # Finding length of so that I can control my volume

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        if length < 60:
            cv2.circle(frame, (cx, cy), 10, (255, 69, 0), cv2.FILLED)

        # Setting hand range (60-330), volume range(-65,0)
        vol = np.interp(length, [60, 330], [min_vol, max_vol])
        vol_bar = np.interp(length, [60, 330], [400, 150])
        vol_percent = np.interp(length, [50, 300],[0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

    # Volume bar
    cv2.rectangle(frame, (50, 150), (85, 400), (255, 215, 0), 3)
    cv2.rectangle(frame, (50, int(vol_bar)), (85, 400), (255, 215, 0), cv2.FILLED)

    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    cv2.putText(frame, f'FPS: {int(vol_percent)} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
