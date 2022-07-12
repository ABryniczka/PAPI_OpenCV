import numpy as np
import cv2 as cv
import os
import datetime
from imutils.video import FPS

#from camera import Camera_properties

#START-------------------Resolution and Camera Parameters-------------------------#
Std_Resolutions = {
    "480p": (640,480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

Video_capture_properties = {

    '10': 'CAP_PROP_BRIGHTNESS', #Brightness of the image.
    '11': 'CAP_PROP_CONTRAST', #Contrast of the image.
    '12': 'CAP_PROP_SATURATION', #Saturation of the image.
    '13': 'CAP_PROP_HUE', #Hue of the image.
    '14': 'CAP_PROP_GAIN', #Gain of the image.
    '15': 'CAP_PROP_EXPOSURE', #Exposure.
    '17': 'CAP_PROP_WHITE_BALANCE', #White Balance (Unsuported)
    '20': 'CAP_PROP_SHARPNESS',
    '21': 'CAP_PROP_AUTO_EXPOSURE',
    '22': 'CAP_PROP_GAMMA ',
    '23': 'CAP_PROP_TEMPERATURE',
    '30': 'CAP_PROP_ISO_SPEED'
    
}

def change_Res(capture_, chose_Res_):
    width, height = Std_Resolutions[chose_Res_]
    capture_.set(3, width)
    capture_.set(4, height)
    return capture_

def check_frame_resolution(frame_, chose_Res_):
    width, height = Std_Resolutions[chose_Res_]
    if (frame_.shape[1] != width) | (frame_.shape[0] != height):
        #print('Zmieniamy')
        frame_ = cv.resize(frame_, Std_Resolutions[chose_Res_], interpolation=cv.INTER_AREA)
    else:
        pass
    return frame_

def change_video_properties(capture_, Video_capture_properties):
    for key, value in Video_capture_properties.items():
        print("{0} = {1}".format(key, value))
    option, value = input("Input number of property and value, (split by space): ").split()
    capture_ = capture_.set(int(option), int(value))
    return capture_

#END-------------------Resolution and Camera Parameters-------------------------#



#START-------------------Masking, Saving masking, Trackbary-------------------------#
    #1.Trackbary
def trackbary_init(title):
    def nothing(x):
            pass

    if title == 'White' or title == 'Pink':
        cv.namedWindow(title)
        cv.resizeWindow(title, 350, 250)

        if title == 'White':
            def_value = np.array(([0,0,24,179,125,255]))
        elif title == 'Pink':
            def_value = np.array(([130,40,29,175,255,255]))

        cv.createTrackbar('H min', title, 0, 179, nothing)
        cv.createTrackbar('S min', title, 0, 255, nothing)
        cv.createTrackbar('V min', title, 0, 255, nothing)
        cv.createTrackbar('H max', title, 0, 179, nothing)
        cv.createTrackbar('S max', title, 0, 255, nothing)
        cv.createTrackbar('V max', title, 0, 255, nothing)

        cv.setTrackbarPos('H min', title, def_value[0])
        cv.setTrackbarPos('S min', title, def_value[1])
        cv.setTrackbarPos('V min', title, def_value[2])
        cv.setTrackbarPos('H max', title, def_value[3])
        cv.setTrackbarPos('S max', title, def_value[4])
        cv.setTrackbarPos('V max', title, def_value[5])

    elif title == 'Red':
        cv.namedWindow(title)
        cv.resizeWindow(title, 350, 550)
        def_value_lower = np.array(([0,75,80,49,255,255]))
        def_value_upper = np.array(([175,0,0,179,255,255]))

        cv.createTrackbar('H_low min', title, 0, 179, nothing)
        cv.createTrackbar('S_low min', title, 0, 255, nothing)
        cv.createTrackbar('V_low min', title, 0, 255, nothing)
        cv.createTrackbar('H_low max', title, 0, 179, nothing)
        cv.createTrackbar('S_low max', title, 0, 255, nothing)
        cv.createTrackbar('V_low max', title, 0, 255, nothing)
        cv.createTrackbar('H_up min', title, 0, 179, nothing)
        cv.createTrackbar('S_up min', title, 0, 255, nothing)
        cv.createTrackbar('V_up min', title, 0, 255, nothing)
        cv.createTrackbar('H_up max', title, 0, 179, nothing)
        cv.createTrackbar('S_up max', title, 0, 255, nothing)
        cv.createTrackbar('V_up max', title, 0, 255, nothing)

        cv.setTrackbarPos('H_low min', title, def_value_lower[0])
        cv.setTrackbarPos('S_low min', title, def_value_lower[1])
        cv.setTrackbarPos('V_low min', title, def_value_lower[2])
        cv.setTrackbarPos('H_low max', title, def_value_lower[3])
        cv.setTrackbarPos('S_low max', title, def_value_lower[4])
        cv.setTrackbarPos('V_low max', title, def_value_lower[5])
        cv.setTrackbarPos('H_up min', title, def_value_upper[0])
        cv.setTrackbarPos('S_up min', title, def_value_upper[1])
        cv.setTrackbarPos('V_up min', title, def_value_upper[2])
        cv.setTrackbarPos('H_up max', title, def_value_upper[3])
        cv.setTrackbarPos('S_up max', title, def_value_upper[4])
        cv.setTrackbarPos('V_up max', title, def_value_upper[5])
    else:
        print('Ivalid input')

def trackbary_getvalue(title):
    if title == 'White' or title == 'Pink':
        H_min = cv.getTrackbarPos('H min', title)
        S_min = cv.getTrackbarPos('S min', title)
        V_min = cv.getTrackbarPos('V min', title)
        H_max = cv.getTrackbarPos('H max', title)
        S_max = cv.getTrackbarPos('S max', title)
        V_max = cv.getTrackbarPos('V max', title)
        values = np.array(([H_min, S_min, V_min, H_max, S_max, V_max]))

    elif title == 'Red':
        H_low_min = cv.getTrackbarPos('H_low min', title)
        S_low_min = cv.getTrackbarPos('S_low min', title)
        V_low_min = cv.getTrackbarPos('V_low min', title)
        H_low_max = cv.getTrackbarPos('H_low max', title)
        S_low_max = cv.getTrackbarPos('S_low max', title)
        V_low_max = cv.getTrackbarPos('V_low max', title)
        H_up_min = cv.getTrackbarPos('H_up min', title)
        S_up_min = cv.getTrackbarPos('S_up min', title)
        V_up_min = cv.getTrackbarPos('V_up min', title)
        H_up_max = cv.getTrackbarPos('H_up max', title)
        S_up_max = cv.getTrackbarPos('S_up max', title)
        V_up_max = cv.getTrackbarPos('V_up max', title)
        values = np.array(([[H_low_min, S_low_min, V_low_min, H_low_max, S_low_max, V_low_max],
                            [H_up_min, S_up_min, V_up_min, H_up_max, S_up_max, V_up_max]]))
    else:
        print('Ivalid input')

    return values
        
#STOP-------------------Masking, Saving masking, Trackbary-------------------------#

#START-------------------Saving videos-------------------------#

def video_recorder(chose_Res_, date):
    dimension = Std_Resolutions[chose_Res_]
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    videoWriter_ = cv.VideoWriter('Camera_videos\Video-'+str(date)+'.avi',fourcc, 30.0, dimension)
    return videoWriter_

#STOP-------------------Saving videos-------------------------#

def main_calibration(chose_Res):

    fps = FPS().start()
    trackbary_init('Red')
    trackbary_init('White')
    trackbary_init('Pink')
    
    
    #'https://192.168.0.105:8080/video'
    #user_choice = user_choice_stream_or_video()
    #print(user_choice)
    count = videowriter_counter = 0
    link1 = 'https://192.168.1.20:8080/video'
    link2 = "Papi_videos\ORLY_PAPI.mp4"
    link3 = "Papi_videos\Simulation_drone.mp4"
    capture = cv.VideoCapture(link1)

    capture = change_Res(capture,chose_Res) #Zmieniamy rozdzielczosc video
    start_record = False

    while (capture.isOpened()):

        #START-------------------Date_time-------------------------#
        date = datetime.datetime.now().strftime("%d_%m_%Y-%I_%M_%S")
        #END---------------------Date_time-------------------------#
        
        ret, frame = capture.read()
    
        if ret is not True: #Zapętlamy jeden wybrany film
            print('No video, starting new loop')
            capture.set(cv.CAP_PROP_POS_FRAMES, 0) #Loop
            continue

        frame = check_frame_resolution(frame, chose_Res)
        #frame[0:190, 0:400] = 0 #Usuwam napis 'Canard' dla 720p
        
        values_white = trackbary_getvalue('White')
        values_pink = trackbary_getvalue('Pink')
        values_red = trackbary_getvalue('Red')
        #print(values_white[0], values_pink[0], values_red[0][0], values_red[1][0])
        

        while (count<1):
            print(frame.shape[:], type(frame))
            count+=1

        #START--------------Tworzenie maski dla 3 kolorow
        scale = 0.8
        #0.Zamiana na HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        #1.WHITE
        'values = np.array(([H_min, S_min, V_min, H_max, S_max, V_max]))'
        min_White = values_white[:3]
        max_White = values_white[3:]
        mask_white = cv.inRange(hsv, min_White, max_White)
        cropped_white = cv.bitwise_and(frame, frame, mask=mask_white)
        cropped_white = cv.resize(cropped_white, (int(cropped_white.shape[1]*scale),int(cropped_white.shape[0]*scale)), interpolation=cv.INTER_AREA)

        #2.PINK
        'values = np.array(([H_min, S_min, V_min, H_max, S_max, V_max]))'
        min_Pink = values_pink[:3]
        max_Pink = values_pink[3:]
        mask_pink = cv.inRange(hsv, min_Pink, max_Pink)
        cropped_pink = cv.bitwise_and(frame, frame, mask=mask_pink)
        cropped_pink = cv.resize(cropped_pink, (int(cropped_pink.shape[1]*scale),int(cropped_pink.shape[0]*scale)), interpolation=cv.INTER_AREA)

        #3.RED
        """values = np.array(([[H_low_min, S_low_min, V_low_min, H_low_max, S_low_max, V_low_max],
                            [H_up_min, S_up_min, V_up_min, H_up_max, S_up_max, V_up_max]]))"""
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

    
        cv.imshow('Main_frame', frame)
        cv.imshow('White_frame', cropped_white)
        cv.imshow('Pink_frame', cropped_pink)
        cv.imshow('Red_frame', cropped_red)

        #START---Nagrywanie---------
        if start_record == True:
            videoWriter.write(frame)
        #END---Nagrywanie----------

        #---------- keyboards keys
        frame_rate = 1
        k = cv.waitKeyEx(frame_rate) & 0xFF 

        if  k == ord('q') or k == ord('Q'):
            print('User break program running')
            break

        elif k == ord('c'):
            continue

        elif k == ord('o'):
            dicts_video = {}
            dict_counter = 1

            for file in os.listdir("Camera_videos"):
                dicts_video[str(dict_counter)] = file
                dict_counter += 1
          
            for key, value in dicts_video.items():
                print(key, ' : ', value)

            nr_video = input("Inter number of video: ")
            path = 'Camera_videos\\'+dicts_video[nr_video]
            capture = cv.VideoCapture(path)
            print('Playing', dicts_video[nr_video])

        elif k == ord('v'):
            capture = cv.VideoCapture(0)
            capture = change_Res(capture,chose_Res)
            if capture is None or not capture.isOpened():
                print('Warning: unable to open video source')
            else:
                pass

        elif k == ord('r'):
            videowriter_counter += 1 
            if (videowriter_counter %2) == 0:
                print("Stop recording")
                start_record = False
                videoWriter.release()
            else:
                videoWriter = video_recorder(chose_Res, date) #Tworzy plik o danej nazwie
                print('Recording frames!')
                start_record = True

        elif k == ord('p'):
            print('Frame saved!')
            cv.imwrite('Camera_photos\Photo'+str(date)+'.jpg',frame)
        
        elif k == ord('\n') or k == ord('\r'):
            print(type(values_white))
            np.savez('Trackbar_values/Values', values_white=values_white, values_pink=values_pink, values_red=values_red)
            print('Zapisujemy ustawienia')
            break

        elif k == ord(','): #Przyspiesza tepo odtwarzania
            if frame_rate == 0:
                pass
            else:
                frame_rate -= 1
        elif k == ord('.'): #Zmniejsza tempo odtwarzania 
            frame_rate += 1
                
        fps.update()
        fps.stop()
        #print("[INFO] approx. FPS: {}".format(int(fps.fps())))
    

    capture.release()
    cv.destroyAllWindows

if __name__ == '__main__':
    main_calibration('480p')