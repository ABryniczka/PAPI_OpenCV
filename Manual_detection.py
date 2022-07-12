import numpy as np
import cv2 as cv
from Calibration import Std_Resolutions, change_Res, check_frame_resolution

def create_points_of_boxes(width_, height_, box_pixels_width_, box_pixels_height_):  # Left Up(x,y); Right Down (x, y)
    center_width, center_height = int(width_ / 2), int(height_ / 2)
    box_ = np.array(([[center_width - (2 * box_pixels_width_), center_height - (box_pixels_height_ // 2),
                       center_width - box_pixels_width_, center_height + (box_pixels_height_ // 2)],
                      [center_width - box_pixels_width_, center_height - (box_pixels_height_ // 2),
                       center_width, center_height + (box_pixels_height_ // 2)],
                      [center_width, center_height - (box_pixels_height_ // 2), center_width + box_pixels_width_,
                       center_height + (box_pixels_height_ // 2)],
                      [center_width + box_pixels_width_, center_height - (box_pixels_height_ // 2),
                       center_width + (2 * box_pixels_width_), center_height + (box_pixels_height_ // 2)]]))

    # Dajemy floor division '//' poniewaz rectangle_shape rząda wartości (int) w boxie
    return box_

def rectangle_shape(capture_, box_, color_, thickens_):
    for x in range(0, len(box_[0])):
        cv.rectangle(capture_, (box_[x][0], box_[x][1]), (box_[x][2], box_[x][3]), color_, thickness=thickens_)

def Number_of_pixels(image):
    pix_rows = image.shape[0]
    pix_columns = image.shape[1]
    return pix_rows * pix_columns

def find_Color(mask_array, threshold, num_of_pixels):
    counter = 0
    for row in mask_array:
        for value in row:

            if value == 255:
                counter += 1

                if counter >= (num_of_pixels * threshold):
                    return True

                else:
                    continue
            else:
                continue

    return False

def create_text(frame_, i, box, Red_, White_, Pink_):

    ''' 
    if (Red_[i] is True) and (White_[i] is False):
        cv.putText(frame_, "Red", (box[i][0] + 50, box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    elif (White_[i] is True) and (Red_[i] is False):
        cv.putText(frame_, "White", (box[i][0] + 50, box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    elif (Red_[i] and White_[i]) is True:
        cv.putText(frame_, "Calibrate", (box[i][0] + 50, box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    elif (Red_[i] and White_[i]) is False:
        cv.putText(frame_, "Blank", (box[i][0] + 50, box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
    else:
        cv.putText(frame_, "Nie dziala", (box[i][0] + 50, box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    '''

    if (Pink_[i] is True) and (White_[i] is False) and (Red_[i] is False):
        cv.putText(frame_, "Pink", (box[i][0], box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (147, 20, 255), 2)

    elif (Red_[i] is True) and (White_[i] is False) and (Pink_[i] is False):
        cv.putText(frame_, "Red", (box[i][0], box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    elif (White_[i] is True) and (Red_[i] is False) and (Pink_[i] is False):
        cv.putText(frame_, "White", (box[i][0], box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    elif ((Red_[i] and White_[i]) is True) and (Pink_[i] is False):
        cv.putText(frame_, "Calib R-W", (box[i][0], box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    elif ((Red_[i] and Pink_[i]) is True) and (White_[i] is False):
        cv.putText(frame_, "Calib R-P", (box[i][0], box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    elif ((Pink_[i] and White_[i]) is True) and (Red_[i] is False):
        cv.putText(frame_, "Calib P-W", (box[i][0], box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    elif (Red_[i] and White_[i] and Pink_[i]) is True:
        cv.putText(frame_, "Calib x3", (box[i][0], box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    elif (Red_[i] and White_[i] and Pink_[i]) is False:
        cv.putText(frame_, "Blank", (box[i][0], box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
    else:
        cv.putText(frame_, "Nie dziala", (box[i][0], box[i][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


def loading_data(name):
    # Values_trial
    data = np.load('Trackbar_values/'+str(name)+'.npz')
    values_white = data['values_white']
    values_pink = data['values_pink']
    values_red = data['values_red']
    return values_white, values_pink, values_red

def main_manual(chose_Res):
    Trackbar_values_name = 'Values'
    values_white, values_pink, values_red = loading_data(Trackbar_values_name)
    link1 = "Papi_videos\ORLY_PAPI.mp4"
    link2 = 'https://192.168.1.20:8080/video'
    capture = cv.VideoCapture(link2)

    capture = change_Res(capture,chose_Res)

    while (capture.isOpened()):
        
        ret, frame = capture.read()
    
        if ret is not True: #Zapętlamy jeden wybrany film
            print('No video, starting new loop')
            capture.set(cv.CAP_PROP_POS_FRAMES, 0) #Loop
            continue

        frame = check_frame_resolution(frame, chose_Res)
        #frame[0:190, 0:400] = 0 #Usuwam napis 'Canard' dla 720p

        #START--------------Tworzenie maski dla 3 kolorow

        scale = 0.8
        #0.Zamiana na HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        #1.WHITE
        min_White = values_white[:3]
        max_White = values_white[3:]
        mask_white = cv.inRange(hsv, min_White, max_White)
        cropped_white = cv.bitwise_and(frame, frame, mask=mask_white)
        cropped_white = cv.resize(cropped_white, (int(cropped_white.shape[1]*scale),int(cropped_white.shape[0]*scale)), interpolation=cv.INTER_AREA)

        #2.PINK
        min_Pink = values_pink[:3]
        max_Pink = values_pink[3:]
        mask_pink = cv.inRange(hsv, min_Pink, max_Pink)
        cropped_pink = cv.bitwise_and(frame, frame, mask=mask_pink)
        cropped_pink = cv.resize(cropped_pink, (int(cropped_pink.shape[1]*scale),int(cropped_pink.shape[0]*scale)), interpolation=cv.INTER_AREA)

        #3.RED
        low_min_red = values_red[0][:3]
        low_max_red = values_red[0][3:]
        up_min_red = values_red[1][:3]
        up_max_red = values_red[1][3:]
        mask_red_low = cv.inRange(hsv, low_min_red, low_max_red)
        mask_red_up = cv.inRange(hsv, up_min_red, up_max_red)
        mask_red = cv.bitwise_or(mask_red_low, mask_red_up)
        cropped_red = cv.bitwise_and(frame, frame, mask=mask_red)
        cropped_red = cv.resize(cropped_red, (int(cropped_red.shape[1]*scale),int(cropped_red.shape[0]*scale)), interpolation=cv.INTER_AREA)

        #END----------------Tworzenie maski dla 3 kolorow

        #START----------------Tworzenie boxów i kratek na glownym framie
        Box_pixels_width, Box_pixels_height = 100, 100
        box = create_points_of_boxes(Std_Resolutions[chose_Res][0], Std_Resolutions[chose_Res][1],Box_pixels_width, Box_pixels_height)
        rectangle_shape(frame, box, (0, 255, 0), 1)

        # Up:Down, Left:Right
        crop_Red = np.array((mask_red[box[0][1]:box[0][3], box[0][0]:box[0][2]],  # crop_1
                             mask_red[box[1][1]:box[1][3], box[1][0]:box[1][2]],  # crop_2
                             mask_red[box[2][1]:box[2][3], box[2][0]:box[2][2]],  # crop_3
                             mask_red[box[3][1]:box[3][3], box[3][0]:box[3][2]])) # crop_4

        crop_White = np.array((mask_white[box[0][1]:box[0][3], box[0][0]:box[0][2]],  # crop_1
                               mask_white[box[1][1]:box[1][3], box[1][0]:box[1][2]],  # crop_2
                               mask_white[box[2][1]:box[2][3], box[2][0]:box[2][2]],  # crop_3
                               mask_white[box[3][1]:box[3][3], box[3][0]:box[3][2]])) # crop_4

        crop_Pink = np.array((mask_pink[box[0][1]:box[0][3], box[0][0]:box[0][2]],  # crop_1
                              mask_pink[box[1][1]:box[1][3], box[1][0]:box[1][2]],  # crop_2
                              mask_pink[box[2][1]:box[2][3], box[2][0]:box[2][2]],  # crop_3
                              mask_pink[box[3][1]:box[3][3], box[3][0]:box[3][2]])) # crop_4

        small_Red = np.array((cv.resize(crop_Red[0], (25, 25), cv.INTER_AREA),
                              cv.resize(crop_Red[1], (25, 25), cv.INTER_AREA),
                              cv.resize(crop_Red[2], (25, 25), cv.INTER_AREA),
                              cv.resize(crop_Red[3], (25, 25), cv.INTER_AREA)))

        small_White = np.array((cv.resize(crop_White[0], (25, 25), cv.INTER_AREA),
                                cv.resize(crop_White[1], (25, 25), cv.INTER_AREA),
                                cv.resize(crop_White[2], (25, 25), cv.INTER_AREA),
                                cv.resize(crop_White[3], (25, 25), cv.INTER_AREA)))

        small_Pink = np.array((cv.resize(crop_Pink[0], (25, 25), cv.INTER_AREA),
                               cv.resize(crop_Pink[1], (25, 25), cv.INTER_AREA),
                               cv.resize(crop_Pink[2], (25, 25), cv.INTER_AREA),
                               cv.resize(crop_Pink[3], (25, 25), cv.INTER_AREA)))

        #STOP----------------Tworzenie boxów i kratek na glownym framie

        #START----------------Sprawdzanie kolorow w boxach

        Red = ((find_Color(small_Red[0], 0.4, Number_of_pixels(small_Red[0])),
                find_Color(small_Red[1], 0.4, Number_of_pixels(small_Red[1])),
                find_Color(small_Red[2], 0.4, Number_of_pixels(small_Red[2])),
                find_Color(small_Red[3], 0.4, Number_of_pixels(small_Red[3]))))
        

        White = ((find_Color(small_White[0], 0.3, Number_of_pixels(small_White[0])),
                  find_Color(small_White[1], 0.3, Number_of_pixels(small_White[1])),
                  find_Color(small_White[2], 0.3, Number_of_pixels(small_White[2])),
                  find_Color(small_White[3], 0.3, Number_of_pixels(small_White[3]))))

        Pink = ((find_Color(small_Pink[0], 0.2, Number_of_pixels(small_Pink[0])),
                 find_Color(small_Pink[1], 0.2, Number_of_pixels(small_Pink[1])),
                 find_Color(small_Pink[2], 0.2, Number_of_pixels(small_Pink[2])),
                 find_Color(small_Pink[3], 0.2, Number_of_pixels(small_Pink[3]))))

        #STOP-----------------Sprawdzanie kolorow w boxach
        
        #START----------------Writing a comment
        
        create_text(frame, 0, box, Red, White, Pink)
        create_text(frame, 1, box, Red, White, Pink)
        create_text(frame, 2, box, Red, White, Pink)
        create_text(frame, 3, box, Red, White, Pink)

        #STOP-----------------Writing a comment

        cv.imshow('White_frame',cropped_white)
        cv.imshow('Pink_frame',cropped_pink)
        cv.imshow('Red_frame',cropped_red)
        cv.imshow('Main_frame', frame)

        k = cv.waitKeyEx(1) & 0xFF

        if  k == ord('q') or k == ord('Q'):
                    print('User break program running')
                    break

    capture.release()
    cv.destroyAllWindows

if __name__ == '__main__':
    main_manual('480p')