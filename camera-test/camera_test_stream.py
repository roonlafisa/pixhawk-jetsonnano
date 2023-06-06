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

    # create a title for the window
    cv2.namedWindow('Video Stream')
    cv2.setWindowTitle('Video Stream', 'Raw Video Stream')

    while True:
        ret, frame = cap.read()
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    # print a message that the camera is can be opened
    print('Camera opened successfully')
    

# now, call the function to open the camera
# open_camera()

# now, create a function to stream the video from the host computer to open network using UDP protocol over wifi, 
# the host and port was previously defined
def stream_video():
    # create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    # bind the socket
    s.bind((host, port))

    # listen to the socket 
    s.listen(10)
    print('Socket now listening')

    # accept the connection
    conn, addr = s.accept()
    print('Connection accepted')

    # create a video capture object
    cap = cv2.VideoCapture(0)

    # set the resolution
    cap.set(3, resolution[0])
    cap.set(4, resolution[1])

    # set the bit rate
    cap.set(5, bit_rate)
    
    # create a title for the window
    cv2.namedWindow('Video Stream')
    cv2.setWindowTitle('Video Stream', 'Streamed Video')

    # start the loop to stream the video, as well as open the video on host computer
    while True:
        ret, frame = cap.read()
        # serialize the frame
        data = pickle.dumps(frame)

        # send the serialized frame
        conn.sendall(struct.pack("Q", len(data))+data)

        # display the frame
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    # print a message that the video is streamed
    print('Video streamed successfully')


# now, call the function to stream the video
stream_video()
