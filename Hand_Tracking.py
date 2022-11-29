import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture(1)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()    #hands.py ctrl+left mouse
mp_draw = mp.solutions.drawing_utils

new_frame_time = 0
prev_frame_time = 0
while True:

    ret, frame = cap.read()

    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    cv2.putText(frame, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    img_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_RGB)
    # print(result.multi_hand_landmarks)
    if result.multi_hand_landmarks:  # landmark will give information about x and y coordinates
        for hand_landmark in result.multi_hand_landmarks:
            for id, landmark in enumerate(hand_landmark.landmark):
                # print(id, landmark)
                # To get the pixel
                height, width, channel = frame.shape
                coordinates_x, coordinates_y = int(landmark.x * width), int(landmark.y * height)
                print(id, coordinates_x, coordinates_y)
            mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
