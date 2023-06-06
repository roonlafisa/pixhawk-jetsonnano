'''
this code is an extension of the code in camera_test_stream.py
this code will be used to capture the video from the host computer camera to the capture computer
'''

# import the necessary packages
import cv2, socket, pickle, struct, time, os 

# define variables
host = '192.168.10.193'
port = 5000

# create a function to capture the video from the host computer
def capture_video():
    # create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    # bind the socket
    s.bind(('0.0.0.0', port))
    print('Socket bind complete')

    # listen to the socket
    s.listen(10)
    print('Socket now listening')

    # accept the connection
    conn, addr = s.accept()

    # create a folder to store the captured video
    os.mkdir('captured_video')

    # start the loop to capture the video
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

        # now, load the frame
        frame = pickle.loads(frame_data)

        # write the frame to the folder
        cv2.imwrite('captured_video/' + str(time.time()) + '.jpg', frame)

        # display the frame
        cv2.imshow('Captured Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # close the connection
    s.close()

# now, call the function to capture the video
capture_video()

# both client and server is in socket now listening state, what is the problem?
# the problem is that the client is not sending any data to the server
# the client can ping the server, but the server cannot ping the client
# the client is not sending any data to the server. how to solve this problem?
# the client is not sending any data to the server because the client is not connected to the server. how to connect?  

