import concurrent.futures
import json
import serial


class Uart:
    def __init__(self, pico_0='/dev/ttyAMA0', pico_1='/dev/ttyAMA1', debug=False):
        self.debug = debug
        self.pico_0 = pico_0
        self.pico_1 = pico_1
        self.serial_0 = None
        self.serial_1 = None
        self.open_serial_0()
        self.open_serial_1()

    def open_serial_0(self):
        try:
            self.serial_0 = serial.Serial(self.pico_0, 115200, timeout=0.5)
        except Exception as error:
            if self.debug:
                print(error, flush=True)

    def open_serial_1(self):
        try:
            self.serial_1 = serial.Serial(self.pico_1, 115200, timeout=0.5)
        except Exception as error:
            if self.debug:
                print(error, flush=True)

    def close_serial_0(self):
        try:
            self.serial_0.close()
        except Exception as error:
            if self.debug:
                print(error, flush=True)

    def close_serial_1(self):
        try:
            self.serial_1.close()
        except Exception as error:
            if self.debug:
                print(error, flush=True)

    def read_pico_0(self):
        try:
            self.serial_0.write('0'.encode('utf-8'))
            input_0 = self.serial_0.read_until(b'}')
            return json.loads(input_0.decode('utf-8'))
        except Exception as error:
            if self.debug:
                print(error, flush=True)
            self.close_serial_0()
            self.open_serial_0()
            return None

    def read_pico_1(self):
        try:
            self.serial_1.write('1'.encode('utf-8'))
            input_1 = self.serial_1.read_until(b'}')
            return json.loads(input_1.decode('utf-8'))
        except Exception as error:
            if self.debug:
                print(error, flush=True)
            self.close_serial_1()
            self.open_serial_1()
            return None

    def read(self):
        try:
            result = {}
            with concurrent.futures.ThreadPoolExecutor() as executor:
                pico_0_future = executor.submit(self.read_pico_0)
                pico_1_future = executor.submit(self.read_pico_1)
                result['pico_0'] = pico_0_future.result()
                result['pico_1'] = pico_1_future.result()
            return result
        except Exception as error:
            if self.debug:
                print(f'{error}', flush=True)
            return None


if __name__ == '__main__':
    uart = Uart(pico_0='/dev/ttyAMA0', pico_1='/dev/ttyAMA1', debug=True)
    while True:
        data = uart.read()
        print(f'{data}\r', end='', flush=True)
