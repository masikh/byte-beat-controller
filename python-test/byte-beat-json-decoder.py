import json
import serial
import time

# Set serial device
# ser = serial.Serial('/dev/tty.usbserial-A50285BI', 115200, timeout=0.1)

ser = serial.Serial(port='/dev/tty.usbserial-A50285BI',
                    baudrate=115200,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1)


def read():
    tic = time.perf_counter()
    count = 0
    while True:
        try:
        # ser.write(49).to_bytes(2, byteorder='little')
            ser.write('0'.encode('utf-8'))
            input = ser.read_until(b'}')
            input = input.decode('utf-8')
            count += 1
            toc = time.perf_counter()
            print(f'\r{input} SR-PI: {count/(toc - tic):0.4f}/seconds', end='')
        except Exception as error:
            pass



def update():
    while True:
        # Tic Toc, performance counter
        tic = time.perf_counter()

        # To pico 0
        # ser.write(48).to_bytes(1, byteorder='little')
        ser.write('0'.encode('utf-8'))
        input0 = ser.readline()
        print(input0)
        #message0 = json.loads(input0.decode('utf-8'))

        # To pico 1
        # ser.write(49).to_bytes(1, byteorder='little')
        ser.write('1'.encode('utf-8'))
        input1 = ser.readline()
        print(input1)
        #message1 = json.loads(input1.decode('utf-8'))

        toc = time.perf_counter()

        # standard out
        #print(f'{message0} {message1} SR-PI: {1/(toc - tic):0.4f}/seconds                        \r', end='')


if __name__ == '__main__':
    read()
