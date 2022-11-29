# Creating module from Hand_Tracking

'''
Hand marking indexes:  https://mediapipe.dev/images/mobile/hand_landmarks.png
'''


import cv2
import time
import mediapipe as mp


class hand_Detector:
    def __init__(self, mode=False, max_hands=1):
        self.mode = mode
        self.max_hands = max_hands

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=True):
        img_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(img_RGB)
        # print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:  # landmark will give information about x and y coordinates
            for hand_landmark in self.result.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame, hand_landmark, self.mp_hands.HAND_CONNECTIONS)

        return frame

    def find_position(self, frame, draw=True, hand_no=0):

        landmark_list = []
        if self.result.multi_hand_landmarks:
            my_hand = self.result.multi_hand_landmarks[hand_no]
            for id, landmark in enumerate(my_hand.landmark):
                # print(id, landmark)
                # To get the pixel
                height, width, channel = frame.shape
                coordinates_x, coordinates_y = int(landmark.x * width), int(landmark.y * height)
                landmark_list.append([id, coordinates_x, coordinates_y])
            # print()

        return landmark_list


def main():
    cap = cv2.VideoCapture(1)
    detector = hand_Detector()
    new_frame_time = 0
    prev_frame_time = 0
    while True:
        ret, frame = cap.read()
        frame = detector.find_hands(frame)
        landmark_list = detector.find_position(frame)
        if len(landmark_list) != 0:
            print(landmark_list[4])
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        cv2.putText(frame, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


