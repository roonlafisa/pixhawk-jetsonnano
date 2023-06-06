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

# now, call the function to open the camera
# open_camera()

# now, create a function which will stream the video using the desired requirements above
def compress_video():
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

    # start the loop to stream the video
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = conn.recv(4*1024)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += conn.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    conn.close()

# now, call the function to stream the video
compress_video()

# now, create a function to confirm that the video is streamed successfully
# this function will be used to test the streaming and generate error message
def confirm_streaming():
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

    # start the loop to stream the video
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = conn.recv(4*1024)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += conn.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    conn.close()

# open a window to show currently streaming video
confirm_streaming()

# now provide a collection of error messages that may occur for failed streaming

# error 1: the host computer is not connected to the network
# error 2: streaming is not successful based on confirm_streaming function


