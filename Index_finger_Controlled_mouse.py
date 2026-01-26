import time
import cv2        #importing all libraries needed
import mediapipe as mp 
import pyautogui
import numpy as np 
import math

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
          
            mp_drawing.draw_landmarks(frame , hand_landmarks , mp_hands.HAND_CONNECTIONS) #draws the landmarks on frame 

            fingers = [
                1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y else 0 
                for tip in [8, 12 , 16 , 20 ]
             ]

            # distace b/w thumb tip and index finger tip 
            click_times = []
            thumb_tip = hand_landmarks.landmark[4]
            dist = math.hypot(thumb_tip.x - index_finger_tip.x , thumb_tip.y - index_finger_tip.y)
            freeze_cursor = False  #by default iss flag ko false rkh ke baad me true hoga to koi condition fulfill krvaynge
            if dist < 0.04 :
                if not freeze_cursor :
                    freeze_cursor = True
                    print("state :" , freeze_cursor) #check krr rha hu iss baar logic chal rha hai ya nhi  
                    click_times.append(time.time())
                    # double click check krr rhe hai 
                    if len(click_times) >= 2 and click_times[-1] - click_times[-2] < 0.4 :
                        pyautogui.doubleClick()
                        cv2.putText(frame, "DOUBLE CLICK" , (10, 50), cv2.FONT_HERSHEY_PLAIN , 1 ,(0,255, 255), 2)
                        # ye line frame prr print  hoti hai ( pixels  , font style , font scale , color code for rgb ,pixel thickness)
                        click_times = []
                        
                    else:
                        pyautogui.click()
                        cv2.putText(frame, "SINGLE CLICK" , (10, 50), cv2.FONT_HERSHEY_PLAIN , 1 ,(0,255, 255, 0), 2)
            else:
             if freeze_cursor : 
                 time.sleep(0.01) #thodi der ruk ke freeze cursor flag ko false krr dega  
                 freeze_cursor = False

            if not freeze_cursor :
             pyautogui.moveTo(screen_x , screen_y , duration = 0.05) #method to move mouse
            
            ######  SCROLL FUNCTION #######
            # scroll mode
            scroll_mode = False
            if sum(fingers) == 4 :
                scroll_mode = True
            else :
                scroll_mode = False
            if scroll_mode :
                if index_finger_tip.y < 0.4 :
                    pyautogui.scroll(60) #scroll krega upward 60 pixels ko , pyautogui mai sab code hai already , zyada dimaag lgana hi nhi hai 
                    cv2.putText(frame, "Scrolling up" , (10, 50), cv2.FONT_HERSHEY_PLAIN , 1 ,(0,255,  0), 2)
                    
                elif index_finger_tip.y > 0.6 :
                    pyautogui.scroll(-60)
                    cv2.putText(frame, "Scroll down" , (10, 50), cv2.FONT_HERSHEY_PLAIN , 1 ,(0,0, 255,), 2)

    cv2.imshow("webcam_feed" , frame)   

    if cv2.waitKey(1) & 0XFF == ord('s') :
        break

cap.release()
cv2.destroyAllWindows()
