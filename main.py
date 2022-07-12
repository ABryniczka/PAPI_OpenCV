from calibration_main import *
from Manual_detection import *
from Automatic_detection import *


def main():
    print('Aviailable resolution: \n')
    for key, value in Std_Resolutions.items():
        print(key, ' : ', value)

    Resolution = input("\nEnter resolution: ")+str('p')
    main_calibration(Resolution)
    cv.destroyAllWindows

    loop = True

    while loop:
        auto_manual = input('Automatic detection -> press (A) \nManual detection press -> (M):\n')

        if auto_manual is ('a' or 'A'):
            main_automatic(Resolution)

        elif auto_manual is ('m' or 'M'):
            main_manual(Resolution)

        elif auto_manual is ('q' or 'Q'):
            loop = False
            break

        else:
            print('Try again')
            continue
            
if __name__ == '__main__':
    main()
    