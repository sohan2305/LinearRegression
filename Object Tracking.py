import cv2
import numpy as np

def setValues(x):
    print("")

#Creating the trackbars needed for adjusting the marker colour

cv2.namedWindow("Color Detectors")
cv2.createTrackbar("Upper Hue", "Color Detectors", 153, 180, setValues)
cv2.createTrackbar("Upper Saturation", "Color Detectors", 255, 255, setValues)
cv2.createTrackbar("Upper Value", "Color Detectors", 255, 255, setValues)
cv2.createTrackbar("Lower Hue", "Color Detectors", 64, 180, setValues)
cv2.createTrackbar("Lower Saturation", "Color Detectors", 72, 255, setValues)
cv2.createTrackbar("Lower Value", "Color Detectors", 49, 255, setValues)

def get_frame(cap, scaling_factor):
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=scaling_factor,
                       fy= scaling_factor, interpolation = cv2.INTER_AREA)
    return frame

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    scaling_factor = 0.7

    #Iterate until the user presses ESC key
    while True:
        frame = get_frame(cap, scaling_factor)

        #Convert the HSV colorspace
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        u_hue = cv2.getTrackbarPos("Upper Hue","Color Detectors")
        u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color Detectors")
        u_value = cv2.getTrackbarPos("Upper Value", "Color Detectors")
        l_hue = cv2.getTrackbarPos("Lower Hue", "Color Detectors")
        l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color Detectors")
        l_value = cv2.getTrackbarPos("Lower Value", "Color Detectors")

        #Define 'color' range in HSV colorspace

        Upper_hsv = np.array([u_hue,u_saturation, u_value])
        Lower_hsv = np.array([l_hue, l_saturation, l_value])
        #Threshold the HSV image to get only selected color

        mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)

        #Bitwise - AND mask and original image

        res = cv2.bitwise_and(frame, frame, mask=mask)
        res = cv2.medianBlur(res,5)
        cv2.imshow('Original image', frame)
        cv2.imshow('Color Detector', res)

        #Check if the user pressed the ESC key

        c = cv2.waitKey(5)
        if c == 27:
            break
    cv2.destroyAllWindows()