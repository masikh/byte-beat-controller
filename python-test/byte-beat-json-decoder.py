import json
import serial

ser = serial.Serial('/dev/tty.usbmodem1101', baudrate=115200)

def read_serial():
    # Open the serial device

    # Initialize an empty string to store the data
    data = ''

    # Read characters from the serial device until an endline is received
    while True:
        c = ser.read().decode('utf-8')
        if c == '\n':
            break
        data += c

    # Parse the data as JSON
    json_data = json.loads(data)

    # Print the JSON data to stdout
    print(f'\r{json_data}                ', end='')


try:
    while True:
        read_serial()
except KeyboardInterrupt:
    # Close the serial device
    ser.close()
