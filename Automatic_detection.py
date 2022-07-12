import numpy as np
import cv2 as cv
from Calibration import Std_Resolutions, change_Res, check_frame_resolution
from Manual_detection import loading_data
from imutils.video import FPS

def create_text(frame_, i, box, Red_, White_, Pink_):

    if (Pink_[i] is True) and (White_[i] is False) and (Red_[i] is False):
        cv.putText(frame_, "Pink", (int(box[i][2]-0.5*box[i][1]), int(box[i][3]-0.5*box[i][1])), cv.FONT_HERSHEY_SIMPLEX, 0.5, (147, 20, 255), 2)

    elif (Red_[i] is True) and (White_[i] is False) and (Pink_[i] is False):
        cv.putText(frame_, "Red", (int(box[i][2]-0.5*box[i][1]), int(box[i][3]-0.5*box[i][1])), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    elif (White_[i] is True) and (Red_[i] is False) and (Pink_[i] is False):
        cv.putText(frame_, "White", (int(box[i][2]-0.5*box[i][1]), int(box[i][3]-0.5*box[i][1])), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    elif ((Red_[i] and White_[i]) is True) and (Pink_[i] is False):
        cv.putText(frame_, "Calib R-W", (int(box[i][2]-0.5*box[i][1]), int(box[i][3]-0.5*box[i][1])), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    elif ((Red_[i] and Pink_[i]) is True) and (White_[i] is False):
        cv.putText(frame_, "Calib R-P", (int(box[i][2]-0.5*box[i][1]), int(box[i][3]-0.5*box[i][1])), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    elif ((Pink_[i] and White_[i]) is True) and (Red_[i] is False):
        cv.putText(frame_, "Calib P-W", (int(box[i][2]-0.5*box[i][1]), int(box[i][3]-0.5*box[i][1])), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    elif (Red_[i] and White_[i] and Pink_[i]) is True:
        cv.putText(frame_, "Calib x3", (int(box[i][2]-0.5*box[i][1]), int(box[i][3]-0.5*box[i][1])), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    elif (Red_[i] and White_[i] and Pink_[i]) is False:
        cv.putText(frame_, "Blank", (int(box[i][2]-0.5*box[i][1]), int(box[i][3]-0.5*box[i][1])), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
    else:
        cv.putText(frame_, "Nie dziala", (int(box[i][2]-0.5*box[i][1]), int(box[i][3]-0.5*box[i][1])), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


def trackbary_init(title):
    def nothing(_):
            pass

    cv.namedWindow(title)
    cv.resizeWindow(title, 350, 50)
    cv.createTrackbar('THR', title, 0, 255, nothing)
    cv.setTrackbarPos('THR', title, 60)

def trackbary_getvalue(title):
    THR = cv.getTrackbarPos('THR', title)
    return THR

def take_third(element):
    return element[2]

def main_automatic(chose_Res):
    #START------------Tworzenie maski dla 3 kolorow
    Trackbar_values_name = 'Values'
    values_white, values_pink, values_red = loading_data(Trackbar_values_name)

    min_White = values_white[:3]
    max_White = values_white[3:]

    min_Pink = values_pink[:3]
    max_Pink = values_pink[3:]

    low_min_red = values_red[0][:3]
    low_max_red = values_red[0][3:]
    up_min_red = values_red[1][:3]
    up_max_red = values_red[1][3:]
    #STOP-------------Tworzenie maski dla 3 kolorow

    link1 = "Papi_videos\ORLY_PAPI.mp4"
    link2 = 'https://192.168.0.105:8080/video'
    link3 = "Papi_videos\Simulation_drone.mp4"
    capture = cv.VideoCapture(link1)

    frameTime = 50
    fps = FPS().start()

    capture = change_Res(capture,chose_Res)

    trackbary_init('Threshold')

    scale = 0.6

    while (capture.isOpened()):
        
        ret, frame = capture.read()
    
        if ret is not True: #Zapętlamy jeden wybrany film
            print('No video, starting new loop')
            capture.set(cv.CAP_PROP_POS_FRAMES, 0) #Loop
            continue
        frame = check_frame_resolution(frame, chose_Res)
        frame[0:190, 0:400] = 0 #Usuwam napis 'Canard' dla 720p

      

        #START -------------Zmiana na gray -> threshold-----------------------
        Threshold_value = trackbary_getvalue('Threshold')

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        Blur = cv.medianBlur(gray_frame, 9)
        _, threshold = cv.threshold(Blur, Threshold_value, 255, cv.THRESH_BINARY)
        #STOP -------------Zmiana na gray -> threshold------------------------

        #START -------------Znajdowanie konturow-----------------------
        contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv.contourArea, reverse=True)[0:20]
        vector = []

        for cnt in contours:

            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.01 * peri, True)

            area = cv.contourArea(cnt) #Calculating area
            rect = cv.minAreaRect(cnt)
            #box = cv.boxPoints(rect)  # Mozemy jeszcze z nich wyluskac kat obrocenia naszego prostokata
            #box = np.int0(box)
            x, y = int(rect[0][0]), int(rect[0][1])  # Center points of rectangle
            w, h = int(rect[1][0]), int(rect[1][1])  # Width and Height od rectangle

            if (len(approx) > 6) and (area > 50) and (0.4 < (w / h) < 1.6) and (0.5*0.5*w*1.2 > area/peri > 0.5*0.5*w*0.8):
                if w>h:
                    vector.append([area, w, x, y])
                else:
                    vector.append([area, h, x, y])
        print(len(vector))
        vector = vector[0:4]
        vector = sorted(vector, key=take_third, reverse=True)
        #print(vector)


        '''
        for area, w_h, x, y in vector:
            cv.rectangle(frame, (int(x - 0.6 * w_h), int(y - 0.6 * w_h)), (int(x + 0.6 * w_h), int(y + 0.6 * w_h)),
                            (255, 255, 0), 1)
            
            if w > h:
                cv.rectangle(frame, (int(x - 0.6 * w), int(y - 0.6 * w)), (int(x + 0.6 * w), int(y + 0.6 * w)),
                            (255, 255, 0), 1)
            else:
                cv.rectangle(frame, (int(x - 0.6 * h), int(y - 0.6 * h)), (int(x + 0.6 * h), int(y + 0.6 * h)),
                            (255, 255, 0), 1)

            cv.putText(frame, str(int(area)), (x, y - max(w, h)), 0, 0.5, (0, 255, 0))
        '''
        
        #STOP -------------Znajdowanie konturow-----------------------

        #START --------------Tworzenie maski dla 3 kolorow-----------------------
        if len(vector) == 4:
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            #1.WHITE

            mask_white = cv.inRange(hsv, min_White, max_White)
            cropped_white = cv.bitwise_and(frame, frame, mask=mask_white)
            cropped_white = cv.resize(cropped_white, (int(cropped_white.shape[1]*scale),int(cropped_white.shape[0]*scale)), interpolation=cv.INTER_AREA)

            #2.PINK
            
            mask_pink = cv.inRange(hsv, min_Pink, max_Pink)
            cropped_pink = cv.bitwise_and(frame, frame, mask=mask_pink)
            cropped_pink = cv.resize(cropped_pink, (int(cropped_pink.shape[1]*scale),int(cropped_pink.shape[0]*scale)), interpolation=cv.INTER_AREA)

            #3.RED
            
            mask_red_low = cv.inRange(hsv, low_min_red, low_max_red)
            mask_red_up = cv.inRange(hsv, up_min_red, up_max_red)
            mask_red = cv.bitwise_or(mask_red_low, mask_red_up)
            cropped_red = cv.bitwise_and(frame, frame, mask=mask_red)
            cropped_red = cv.resize(cropped_red, (int(cropped_red.shape[1]*scale),int(cropped_red.shape[0]*scale)), interpolation=cv.INTER_AREA)

            #STOP ---------------Tworzenie maski dla 3 kolorow-----------------------

            #START---------------Tworzenie boxow-----------------------

            # Up:Down, Left:Right
            # 0 - area, 1 - width or height, 2 - x , 3 - y
            box = np.array(([vector[0][3] - int(0.6*vector[0][1]), vector[0][3] + int(0.6*vector[0][1]), vector[0][2] - int(0.6*vector[0][1]), vector[0][2] + int(0.6*vector[0][1])],
                            [vector[1][3] - int(0.6*vector[1][1]), vector[1][3] + int(0.6*vector[1][1]), vector[1][2] - int(0.6*vector[1][1]), vector[1][2] + int(0.6*vector[1][1])],
                            [vector[2][3] - int(0.6*vector[2][1]), vector[2][3] + int(0.6*vector[2][1]), vector[2][2] - int(0.6*vector[2][1]), vector[2][2] + int(0.6*vector[2][1])],
                            [vector[3][3] - int(0.6*vector[3][1]), vector[3][3] + int(0.6*vector[3][1]), vector[3][2] - int(0.6*vector[3][1]), vector[3][2] + int(0.6*vector[3][1])]))

        
            ''' 
            frame_box = np.array((frame[box[0][0]:box[0][1], box[0][2]:box[0][3]],
                                frame[box[1][0]:box[1][1], box[1][2]:box[1][3]],
                                frame[box[2][0]:box[2][1], box[2][2]:box[2][3]],
                                frame[box[3][0]:box[3][1], box[3][2]:box[3][3]]))

            frame_box[0] = cv.resize(frame_box[0], (int(frame_box[0].shape[1]*5),int(frame_box[0].shape[0]*5)), interpolation=cv.INTER_AREA)
            frame_box[1] = cv.resize(frame_box[1], (int(frame_box[1].shape[1]*5),int(frame_box[1].shape[0]*5)), interpolation=cv.INTER_AREA)
            frame_box[2] = cv.resize(frame_box[2], (int(frame_box[2].shape[1]*5),int(frame_box[2].shape[0]*5)), interpolation=cv.INTER_AREA)
            frame_box[3] = cv.resize(frame_box[3], (int(frame_box[3].shape[1]*5),int(frame_box[3].shape[0]*5)), interpolation=cv.INTER_AREA)    
            '''

            crop_Red = np.array((mask_red[box[0][0]:box[0][1], box[0][2]:box[0][3]],  # crop_1
                                mask_red[box[1][0]:box[1][1], box[1][2]:box[1][3]],  # crop_2
                                mask_red[box[2][0]:box[2][1], box[2][2]:box[2][3]],  # crop_3
                                mask_red[box[3][0]:box[3][1], box[3][2]:box[3][3]]), dtype="object") # crop_4

            crop_White = np.array((mask_white[box[0][0]:box[0][1], box[0][2]:box[0][3]],  # crop_1
                                mask_white[box[1][0]:box[1][1], box[1][2]:box[1][3]],  # crop_2
                                mask_white[box[2][0]:box[2][1], box[2][2]:box[2][3]],  # crop_3
                                mask_white[box[3][0]:box[3][1], box[3][2]:box[3][3]]), dtype="object") # crop_4

            crop_Pink = np.array((mask_pink[box[0][0]:box[0][1], box[0][2]:box[0][3]],  # crop_1
                                mask_pink[box[1][0]:box[1][1], box[1][2]:box[1][3]],  # crop_2
                                mask_pink[box[2][0]:box[2][1], box[2][2]:box[2][3]],  # crop_3
                                mask_pink[box[3][0]:box[3][1], box[3][2]:box[3][3]]), dtype="object") # crop_4
            
            #STOP----------------Tworzenie boxow-----------------------

            #START--------------------Znajdowanie kolorow-----------------
            def find_Color_automatic(crop_frame, color_thr):
                if crop_frame.sum() >= (crop_frame.size*255)*color_thr:
                    return True
                else:
                    return False

            Red = ((find_Color_automatic(crop_Red[0], 0.6),
                    find_Color_automatic(crop_Red[1], 0.6),
                    find_Color_automatic(crop_Red[2], 0.6),
                    find_Color_automatic(crop_Red[3], 0.6)))

            White = ((find_Color_automatic(crop_White[0], 0.8),
                    find_Color_automatic(crop_White[1], 0.8),
                    find_Color_automatic(crop_White[2], 0.8),
                    find_Color_automatic(crop_White[3], 0.8)))

            Pink =  ((find_Color_automatic(crop_Pink[0], 0.4),
                    find_Color_automatic(crop_Pink[1], 0.4),
                    find_Color_automatic(crop_Pink[2], 0.4),
                    find_Color_automatic(crop_Pink[3], 0.4)))

            create_text(frame, 0, vector, Red, White, Pink)
            create_text(frame, 1, vector, Red, White, Pink)
            create_text(frame, 2, vector, Red, White, Pink)
            create_text(frame, 3, vector, Red, White, Pink)
            
        else:
            pass
        #START---------------Rysowanie prostokatow------------------

        for area, w_h, x, y in vector:
            cv.rectangle(frame, (int(x - 0.6 * w_h), int(y - 0.6 * w_h)), (int(x + 0.6 * w_h), int(y + 0.6 * w_h)),
                            (255, 255, 0), 1)

        #STOP---------------Rysowanie prostokatow------------------

        
        #STOP--------------------Znajdowanie kolorow-----------------
        cv.imshow("frame", frame)
        cv.imshow("threshold", threshold)
        
        
        k = cv.waitKeyEx(frameTime) & 0xFF

        if  k == ord('q') or k == ord('Q'):
            print('User break program running')
            break

    capture.release()
    cv.destroyAllWindows

if __name__ == '__main__':
    main_automatic('720p')