'''
create a code to stream an USB camera over wifi.
The host device that the program will run is a Jetson Nano.
The port that camera is connected is video0 (via USB)
The host computer IP address is 192.168.10.251
The port that the program will stream is 5000


The streamed video shall be compressed and in 640x480 resolution
The streaming rate will be constant bit rate of 1 Mbps
The streaming compression shall be done using H.264 codec
The streaming shall be done using wifi connection using UDP protocol

The streamed video shall be received by a computer in the same network

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
    print('Camera can be opened successfully')
    

# now, call the function to open the camera
# open_camera()

# now, create a function which will stream the video using the desired requirements above, 
# open the video on the host computer, 
# and display the video on the host computer 
# and print a message that the streaming is successful
def stream_video():
    # create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    # bind the socket
    s.bind((host, port))
    print('Socket bind complete')

    # listen to the socket
    s.listen(10)
    print('Socket now listening')

    # accept the connection
    conn, addr = s.accept()

    # open the video on the host computer
    cap = cv2.VideoCapture(0)

    # start the loop to stream the video
    while True:
        ret, frame = cap.read()
        # compress the frame
        frame = cv2.resize(frame, resolution)
        # encode the frame
        data = pickle.dumps(frame)
        # get the size of the frame
        message_size = struct.pack("L", len(data))
        # send the frame size
        conn.sendall(message_size + data)

        # display the frame
        cv2.imshow('Streaming Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # close the socket
    s.close()

# now, call the function to stream the video
stream_video()


# now provide a collection of error messages that may occur for failed streaming

# error 1: the host computer is not connected to the network
# error 2: streaming is not successful based on confirm_streaming function


