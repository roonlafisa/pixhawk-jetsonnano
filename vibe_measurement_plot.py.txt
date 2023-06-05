# Code to plot vibration data from pixhawk. To execute the code:
# 1. Replace '/dev/ttyTHS1' in the code with the appropriate serial port of your hardware. You can check the available serial ports on your system.
# 2. Adjust the baud rate (57600 in this example) to match the baud rate of your hardware setup.
# 3. Save the code to a file with a .py extension (e.g., vibration_monitor.py).
# 4. Open a terminal or command prompt.
# 5. Navigate to the directory where the script file is located.
# 6. Run the script by executing python3 vibration_monitor.py in the terminal.
# 7. The script will start monitoring the vibration data and display real-time plots.
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
from pymavlink import mavutil
import threading
from collections import deque

# Create synchronized deques to store vibration data and timestamps
timestamps = deque(maxlen=1000)
vibration_x = deque(maxlen=1000)
vibration_y = deque(maxlen=1000)
vibration_z = deque(maxlen=1000)

# Connect to the MAVLink-enabled device
# Replace '/dev/ttyTHS1' with the appropriate serial port of your hardware
# Adjust the baud rate (57600 in this example) to match your hardware setup
master = mavutil.mavlink_connection('/dev/ttyTHS1', baud=57600)

# Enable the VIBRATION message
master.mav.request_data_stream_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_ALL,
    10,  # Request the VIBRATION message at a rate of 10 Hz
    1,   # Enable the message
)

# Variables to handle discontinuity
last_timestamp = None
discontinuity_counter = 0
discontinuity_threshold = 5  # Threshold in seconds for discontinuity

# Create and open the CSV file in write mode
csv_file = open('vibration_data.csv', 'w')
csv_writer = csv.writer(csv_file)

# Write the header row to the CSV file
csv_writer.writerow(['Time', 'Vibration (X)', 'Vibration (Y)', 'Vibration (Z)'])

# Function to record vibration data
def record_vibration(msg):
    global last_timestamp, discontinuity_counter

    # Get the current timestamp
    current_timestamp = datetime.now()

    # Check for discontinuity
    if last_timestamp is not None and (current_timestamp - last_timestamp).total_seconds() > discontinuity_threshold:
        # Increment the discontinuity counter
        discontinuity_counter += 1

        if discontinuity_counter > discontinuity_threshold:
            print("Discontinuity persists. Exiting...")
            import sys
            sys.exit(0)

        # Skip recording this data point
        return

    # Reset the discontinuity counter
    discontinuity_counter = 0

    vibration_x.append(msg.vibration_x)
    vibration_y.append(msg.vibration_y)
    vibration_z.append(msg.vibration_z)

    # Get the timestamp from the message
    timestamp = current_timestamp.strftime('%H:%M:%S')
    timestamps.append(timestamp)

    # Update the last timestamp
    last_timestamp = current_timestamp

    # Write the vibration data to the CSV file
    csv_writer.writerow([timestamp, msg.vibration_x, msg.vibration_y, msg.vibration_z])
    csv_file.flush()  # Flush the buffer to write the data immediately

# Function to print the latest vibration data
def print_data():
    latest_index = len(timestamps) - 1
    print(f'Time: {timestamps[latest_index]} - Vibration (X): {vibration_x[latest_index]}, Vibration (Y): {vibration_y[latest_index]}, Vibration (Z): {vibration_z[latest_index]}')

# Function to update the plot with new data
def update_plot(frame):
    # Clear the plot and redraw
    plt.cla()

    # Plot the vibration data
    if timestamps and vibration_x and vibration_y and vibration_z:
        plt.plot(timestamps, vibration_x, color='r', label='Vibration (X)')
        plt.plot(timestamps, vibration_y, color='g', label='Vibration (Y)')
        plt.plot(timestamps, vibration_z, color='b', label='Vibration (Z)')

    # Format the x-axis labels as clock time
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(plt.FixedFormatter(timestamps))

    # Set y-axis limits
    plt.ylim(0, 60)

    # Add labels and legend
    plt.xlabel('Time')
    plt.ylabel('Vibration')
    plt.legend()

    # Add plot title
    plt.title('Vibration Data')

# Create the plot figure
fig = plt.figure()

# Start the animation to update the plot
ani = animation.FuncAnimation(fig, update_plot, interval=1000)

# Function to handle incoming MAVLink messages
def handle_mavlink_messages():
    while True:
        msg = master.recv_match(type='VIBRATION', blocking=True)
        if msg is not None:
            record_vibration(msg)
            print_data()

# Start a separate thread to handle MAVLink messages
message_thread = threading.Thread(target=handle_mavlink_messages)
message_thread.start()

# Show the plot
plt.show()

# Close the CSV file
csv_file.close()
