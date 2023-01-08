import json
import serial


class Uart:
    def __init__(self, device_file, debug=False):
        self.debug = debug
        self.device_file = device_file
        self.serial = None
        self.open_serial()
        self.i = 0
        self.j = 1023
        self.k = 2047
        self.l = 4095

    def mock(self):
        self.i = (self.i + 10) % 4095
        self.j = (self.j + 10) % 4095
        self.k = (self.k + 10) % 4095
        self.l = (self.l + 10) % 4095

        return {
            '48': {'adc0': self.i, 'adc1': self.j, 'btn0': 0 < self.i < 3070, 'btn1': 0 < self.j < 3070, 'sr': '2/s', 'cid': 48},
            '49': {'adc0': self.k, 'adc1': self.l, 'btn0': 0 < self.k < 3070, 'btn1': 0 < self.l < 3070, 'sr': '2/s', 'cid': 49}
        }

    def open_serial(self):
        try:
            self.serial = serial.Serial(self.device_file, 115200, timeout=0.05)
        except Exception as error:
            if self.debug:
                print(error, flush=True)

    def close_serial(self):
        try:
            self.serial.close()
        except Exception as error:
            if self.debug:
                print(error, flush=True)

    def read(self):
        try:
            result = {}
            self.serial.write((48).to_bytes(1, byteorder='little'))
            input0 = self.serial.read_until()
            result['48'] = json.loads(input0.decode('utf-8'))

            self.serial.write((49).to_bytes(1, byteorder='little'))
            input_1 = self.serial.read_until()
            result['49'] = json.loads(input_1.decode('utf-8'))
            return result
        except serial.SerialException as error:
            if self.debug:
                print(error, flush=True)
            self.close_serial()
            self.open_serial()
            return None
        except Exception as error:
            if self.debug:
                print(error, flush=True)
            self.close_serial()
            self.open_serial()
            return None


if __name__ == '__main__':
    uart = Uart('/dev/serial0', debug=True)
    while True:
        uart.read()
