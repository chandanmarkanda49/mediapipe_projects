import time
import cv2        #importing all libraries needed
import mediapipe as mp 
import pyautogui as pg
import numpy as np 
import math

mp_hands = mp.solutions.hands  
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands( min_detection_confidence = 0.7,
                       min_tracking_confidence = 0.7  ,
                       max_num_hands = 1 , 
                        )


cap = cv2.VideoCapture(0) # 0 means the first webcame option available
screen_width ,  screen_height  = pg.size()
screen_width += 100 
screen_height += 100
# XY coordinates have 0, 0 origin at top left corner of the screen. X increases going right, Y increases going down.


if not cap.isOpened():
    print("Error: Camera nahi khul raha hai!")
    exit()

while cap.isOpened() :   #main loop in which logic is written ~= void loop
    ret, frame = cap.read()
    coordinates = str(pg.position())   
   
    if not ret :
        print("Frame read nahi ho raha!")
        break
    frame = cv2.flip(frame , 1 )
    h,w ,c = frame.shape     #height , width and color channel is saved in respective variables 
    rgb_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame) 
    cv2.putText(frame,coordinates,(10, 70), cv2.FONT_HERSHEY_PLAIN , 1 ,(0,255, 255, 0), 2) 

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks :
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            thumb_tip = hand_landmarks.landmark[4]
            ring_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            pinky_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
            mid_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            mid_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP] 
            
            
            x_i = int(index_finger_tip.x * w)
            y_i = int(index_finger_tip.y * h)  

            # x_p_t = int (pinky_finger_tip.x * w)
            # y_p_t = int( pinky_finger_tip.y * h)

            # x_p_m = int(pinky_finger_mcp.x * w)
            # y_p_m = int(pinky_finger_mcp.y * h) 

            # x_r_m = int(ring_finger_mcp.x * w)
            # y_r_m = int(ring_finger_mcp.y * h)

            # x_r_t = int(ring_finger_tip.x * w)
            # x_r_t = int(ring_finger_tip.y * h)

            # x_i_m = int(index_finger_mcp.x * w)
            # y_i_m = int(index_finger_mcp.y * h)

            p_t_m = math.hypot(ring_finger_mcp.x - ring_finger_tip.x , ring_finger_mcp.y - ring_finger_tip.y)
            r_t_m = math.hypot(pinky_finger_mcp.x - pinky_finger_tip.x , pinky_finger_mcp.y - pinky_finger_tip.y) 
            th_i_mcp = math.hypot(index_finger_mcp.x - thumb_tip.x, index_finger_mcp.y - index_finger_mcp.y)
            i_t_mcp = math.hypot(index_finger_mcp.x - index_finger_tip.x, index_finger_mcp.y - index_finger_tip.y)
            m_t_mcp = math.hypot(mid_finger_mcp.x - mid_finger_tip.x, mid_finger_mcp.y - mid_finger_tip.y )
            

            #it returns the pixels value of the screen matlab screen kr pixels ke beech ka distance
            screen_x = np.interp(x_i , [0,w], [0,screen_width])
            screen_y = np.interp(y_i , [0,h], [0,screen_height])
          
            mp_drawing.draw_landmarks(frame , hand_landmarks , mp_hands.HAND_CONNECTIONS) #draws the landmarks on frame 


            fingers = [
                1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y else 0 
                for tip in [8, 12 , 16 , 20 ]
             ]
            
            
            if p_t_m<0.10 and r_t_m<0.10:
                    cv2.putText(frame, "Mouse mode" , (10, 50), cv2.FONT_HERSHEY_PLAIN , 1 ,(0, 255,0), 2)  
                    # distace b/w thumb tip and index finger tip 
                    click_times = []
                    thumb_tip = hand_landmarks.landmark[4]
                    # dist = math.hypot(thumb_tip.x - index_finger_tip.x , thumb_tip.y - index_finger_tip.y)
                    freeze_cursor = False  #by default iss flag ko false rkh ke baad me true hoga to koi condition fulfill krvaynge
                    if th_i_mcp < 0.04  :
                        if not freeze_cursor :
                                freeze_cursor = True
                                print("state :" , freeze_cursor) #check krr rha hu iss baar logic chal rha hai ya nhi  
                                click_times.append(time.time())	 # double click check krr rhe hai
                                if m_t_mcp<0.10:
                                        if len(click_times) >= 2 and click_times[-1] - click_times[-2] < 0.4 :
                                                # pg.doubleClick()
                                                cv2.putText(frame, "DOUBLE CLICK" , (100, 50), cv2.FONT_HERSHEY_PLAIN , 1 ,(0,255, 255), 2)
									            # ye line frame prr print  hoti hai ( pixels  , font style , font scale , color code for rgb ,pixel thickness)
                                                click_times = []
                                        else:
                                                # pg.leftClick()
                                                cv2.putText(frame, "SINGLE CLICK" , (100, 50), cv2.FONT_HERSHEY_PLAIN , 1 ,(0,255, 255, 0), 2)                                                     
                    else:
                          if freeze_cursor : 
                                time.sleep(0.01) #thodi der ruk ke freeze cursor flag ko false krr dega  
                                freeze_cursor = False

                          if not freeze_cursor :
                            pg.moveTo(screen_x , screen_y , duration = 0.05) #method to move mouse
                
            ######  SCROLL FUNCTION #######
            # scroll mode
            # scroll_mode = False
            # if sum(fingers) == 4 :
            #     scroll_mode = True
            # else :
            #     scroll_mode = False
            # if scroll_mode :
            #     if index_finger_tip.y < 0.4 :
            #         pg.scroll(60) #scroll krega upward 60 pixels ko , pg mai sab code hai already , zyada dimaag lgana hi nhi hai 
            #         cv2.putText(frame, "Scrolling up" , (10, 50), cv2.FONT_HERSHEY_PLAIN , 1 ,(0,255,  0), 2)
                    
                    
            #     elif index_finger_tip.y > 0.6 :
            #         pg.scroll(-60)
            #         cv2.putText(frame, "Scroll down" , (10, 50), cv2.FONT_HERSHEY_PLAIN , 1 ,(0, 255,0), 2)
      
            # #####    SCREENSHOT  ########
            # last_screenshot_time = 0 
            # screenshot_duration = 3
            # if sum(fingers) == 0 :
            #     current_time = time.time()
            #     if current_time - last_screenshot_time > screenshot_duration : #iss if mai tabhi jayega jab time more than 2 seconds ho 
            #         pg.screenshot(f" screenSHOT_{int(current_time)}.png") #png file save krr dega ye 
            #         cv2.putText(frame, "Screenshot Taken" , (10, 50), cv2.FONT_HERSHEY_PLAIN , 1 ,(0, 255,0), 2)
            #         last_screenshot_time = current_time #yha pe last screenshot time ko update krr diya so that loop repeat ho ske 

    cv2.imshow("webcam_feed" , frame)   

    if cv2.waitKey(1) & 0XFF == ord('s') :
        break



#Mouse condition 









cap.release()
cv2.destroyAllWindows()
