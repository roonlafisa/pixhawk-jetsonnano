'''
Create a code to stream an USB camera over wifi.
2. The host device that the program will run is a Jetson Nano.
3. The port that camera is connected is video0 (via USB)
4. The host computer IP address is defined in a variable
5. The port that the program will stream is 5000
6. Use fswebcam package to capture the video
7. Use mjpeg-streamer to stream the video
8. The streamed video shall be compressed and in 640x480 resolution
9. The streaming rate will be constant bit rate of 1 Mbps
10. The streaming shall be done using wifi connection using UDP protocol=
11. The streamed video shall be received by a computer in the same network



'''

# import the necessary packages in one line
from calendar import c
import cv2, socket, pickle, struct

# define variables
host = '192.168.10.193'
port = 5000
bit_rate = 1000000
resolution = (640, 480)

# first, create a function to open the video on the host computer on a see the video
# this function will be used to test the camera
def open_camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    # print a message that the camera is can be opened
    print('Camera opened successfully')
    

# now, call the function to open the camera
open_camera()

# now, compress the video
def compress_video():
    # create a VideoCapture object
    cap = cv2.VideoCapture(0)
    # set the resolution
    cap.set(3, resolution[0])
    cap.set(4, resolution[1])
    # set the bit rate
    cap.set(5, bit_rate)
    # now, read the video
    ret, frame = cap.read()
    # now, display the video
    cv2.imshow('Camera', frame)
    # now, save the video
    cv2.imwrite('test.jpg', frame)
    # now, release the camera
    cap.release()
    # now, destroy all windows
    cv2.destroyAllWindows()
    # print a message that the video is compressed
    print('Video compressed successfully')

# now, open the compressed video to see if it is compressed on a new window



