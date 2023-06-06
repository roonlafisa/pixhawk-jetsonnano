'''
Create a code to stream an USB camera over wifi so that clients can see the video over web browser.
* The host device that the program will run is a Jetson Nano.
* The port that camera is connected is video0 (via USB)
* The host computer IP address is defined in a variable
* The streamed video shall be compressed and in 640x480 resolution
* The streaming shall be done using wifi connection from the host computer
* The streamed video shall be received by a computer from any network using web browser

'''

# import the necessary packages in one line
from calendar import c
import cv2, socket, pickle, struct, time, os

# define variables
host = '192.168.10.193'
port = 5500
# kill the process that uses the port from previous runs, use port variable,
os.system('fuser -k 5000/tcp')


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

# now, create a function to stream the video from the host computer to open network using UDP protocol over wifi
# the streamed video can be accessed by any computer in the same network using web browser
# the host and port was previously defined

def stream_video():
    # create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    # bind the socket
    s.bind((host, port))

    # listen to the socket
    s.listen(5)
    print('Socket is listening')

    # accept the connection
    while True:
        client_socket, addr = s.accept()
        print('Got connection from', addr)

        # if the connection is accepted, start sending the video
        if client_socket:
            vid = cv2.VideoCapture(0)

            while(vid.isOpened()):
                img, frame = vid.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a))+a
                client_socket.sendall(message)

                cv2.imshow('Video Stream', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    client_socket.close()
                    break
        else:
            print('No connection')
            break
    cv2.destroyAllWindows()
    vid.release()
    return

# now, call the function to stream the video
stream_video()