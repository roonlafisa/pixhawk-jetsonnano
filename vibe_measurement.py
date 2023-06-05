from pymavlink import mavutil

# Connect to the MAVLink-enabled device
master = mavutil.mavlink_connection('/dev/ttyTHS1', baud=57600)

# Enable the VIBRATION message
master.mav.request_data_stream_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_ALL,
    10,  # Request the VIBRATION message at a rate of 10 Hz
    1,   # Enable the message
)

# Continuously read and print the VIBRATION messages
while True:
    msg = master.recv_match(type='VIBRATION', blocking=True)
    if msg is not None:
        # Extract the vibration values from the message
        vibration_x = msg.vibration_x
        vibration_y = msg.vibration_y
        vibration_z = msg.vibration_z

        # Print the vibration values
        print("Vibration (X):", vibration_x)
        print("Vibration (Y):", vibration_y)
        print("Vibration (Z):", vibration_z)
