'''
create a code to stream an USB camera over wifi.
The device that the program will run is a Jetson Nano.
The port that camera is connected is video0
The host computer IP address is 192.168.10.251
The port that the program will stream is 5000
The streamed video shall be uncompressed and in 640x480 resolution
The streaming rate will be constant bit rate of 1 Mbps
The streamed video shall be received by a computer in the same network

'''

# import the necessary packages in one line
import cv2, socket, pickle, struct

# define variables
host = '192.168.10.251'
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

# now, create a function to compress the video such that the streaming rate is 1 Mbps
def compress_video():
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    # bind the socket to the host and port
    s.bind((host, port))
    print('Socket bind complete')

    # listen to the socket
    s.listen(5)
    print('Socket now listening')

    # accept the connection
    conn, addr = s.accept()

    # start sending the video
    # create a VideoCapture object
    cap = cv2.VideoCapture(0)

    # set the resolution
    cap.set(3, resolution[0])
    cap.set(4, resolution[1])

    # define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, resolution)

    # now, send the video
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        data = pickle.dumps(frame)
        message_size = struct.pack('L', len(data))
        conn.sendall(message_size + data)

    # close the connection
    conn.close()

# now, call the function to compress the video
compress_video()

# now, create a function to see the compressed video
# this function will be used to test the compression
def see_compressed_video():
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    # bind the socket to the host and port
    s.bind((host, port))
    print('Socket bind complete')

    # listen to the socket
    s.listen(5)
    print('Socket now listening')

    # accept the connection
    conn, addr = s.accept()

    # now, receive the data and reconstruct the video
    data = b''
    payload_size = struct.calcsize('L')
    while True:
        while len(data) < payload_size:
            data += conn.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack('L', packed_msg_size)[0]
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # close the connection
    conn.close()

# now, call the function to see the compressed video
# see_compressed_video()