import json
import serial
import time


ser = serial.Serial('/dev/tty.usbserial-A50285BI', 115200, timeout=0.5)


def update():
    while True:
        tic = time.perf_counter()
        ser.write(48).to_bytes(1, byteorder='little')
        input0 = ser.read_until()
        message0 = json.loads(input0.decode('utf-8'))

        ser.write(49).to_bytes(1, byteorder='little')
        input1 = ser.read_until()
        message1 = json.loads(input1.decode('utf-8'))

        toc = time.perf_counter()

        print(f'{message0} SR-PI: {1/(toc - tic):0.4f}/seconds                        \r', end='')


if __name__ == '__main__':
    update()
