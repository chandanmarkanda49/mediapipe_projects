import cv2        #importing all libraries needed
import mediapipe as mp 
import pyautogui
import numpy as np 

mp_hands = mp.solutions.hands  
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence = 0.7,
                       min_tracking_confidence = 0.7   , 
                        )

cap = cv2.VideoCapture(0) # 0 means the first webcame option available
screen_width , screen_height = pyautogui.size()


if not cap.isOpened():
    print("Error: Camera nahi khul raha hai!")
    exit()

while cap.isOpened() :   #main loop in which logic is written ~= void loop
    ret, frame = cap.read()
    if not ret :
        print("Frame read nahi ho raha!")
        break
    frame = cv2.flip(frame , 1 )
    h,w ,c = frame.shape     #height , width and color channel is saved in respective variables 
    rgb_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame) 

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks :
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_finger_tip.x * w)
            y = int(index_finger_tip.y * h)   #it returns the pixels value of the screen matlab screen kr pixels ke beech ka distance
            screen_x = np.interp(x , [0,w], [0,screen_width])
            screen_y = np.interp(y , [0,h], [0,screen_height])

            pyautogui.moveTo(screen_x , screen_y , duration = 0.01) #method to move mouse
            mp_drawing.draw_landmarks(frame , hand_landmarks , mp_hands.HAND_CONNECTIONS) #draws the landmarks on frame 

    cv2.imshow("webcam_feed" , frame)   

    if cv2.waitKey(1) & 0XFF == ord('s') :
        break

cap.release()
cv2.destroyAllWindows()
