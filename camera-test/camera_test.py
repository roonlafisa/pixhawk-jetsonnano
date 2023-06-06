'''
create a code to stream an USB camera over wifi.
The device that the program will run is a Jetson Nano.
The port that camera is connected is video0
The host computer IP address is 192.168.10.251
The port that the program will stream is 5000
The streamed video shall be uncompressed and in 640x480 resolution
The streamed video shall be received by a computer in the same network

'''

# import the necessary packages in one line
import cv2, socket, pickle, struct

# first, open the video on the host computer on a see the video
def open_camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# now, call the function to open the camera
open_camera()