import math
import numpy as np
import threading
from pyaudio import PyAudio, paUInt8, paFloat32


class PlayByteBeat():
    def __init__(self, formula='t'):
        pa = PyAudio()
        self.audio_int = pa.open(format=paUInt8, channels=1, rate=8000, output=True)
        self.audio_float = pa.open(format=paFloat32, channels=1, rate=8000, output=True)
        self.formula = formula
        self.probe_formula = formula
        self.four_hours = 3600 * 4 * 8000  # 3600 (seconds) * 4 * 8khz samples
        self.t = 1
        self.reverse = False
        self.play = False
        self.stop = True
        self.byte_beat_values = []
        self.error = ""
        self.OP_value = 0
        self.BP_value = 0
        self.RP_value = 0
        self.GP_value = 0
        self.OB_value = 0
        self.BB_value = 0
        self.RB_value = 0
        self.GB_value = 0
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            valid_formula, is_byte_beat = self.is_valid_formula(self.probe_formula)
            if valid_formula:
                self.formula = self.probe_formula

            if not self.stop:
                self.compute()
                self.to_pyaudio(is_byte_beat)

    def reset_time(self):
        self.t = 1

    def increment(self):
        if not self.reverse:
            self.t += 1
        else:
            self.t -= 1

    def is_valid_formula(self, formula):
        """ Check if a formula is valid and if its byte-beat or float-beat

        :param formula:
        :return: (bool) valid, (bool) is_byte_beat
        """
        try:
            eval(formula, {"t": 1})
            return True, True
        except Exception as error:
            self.error = error

        try:
            eval(formula, {
                "t": 1,
                "sin": self.sin, "cos": self.cos, "tan": self.tan,
                "OP8": self.OP8, "OP10":self.OP10, "OP16": self.OP16,
                "BP8": self.BP8, "BP10":self.BP10, "BP16": self.BP16,
                "RP8": self.OP8, "RP10":self.OP10, "RP16": self.RP16,
                "GP8": self.GP8, "GP10":self.GP10, "GP16": self.OP16,
                "OB": self.OB, "BB": self.BB, "RB": self.RB, "GB": self.GB
            })
            return True, False
        except Exception as error:
            self.error = error

        return False, False

    def compute(self):
        self.byte_beat_values = []
        if abs(self.t) > self.four_hours:
            self.t = 1

        valid_formula, is_byte_beat = self.is_valid_formula(self.formula)
        if valid_formula:
            for _i in range(0x100):
                try:
                    if is_byte_beat is True:
                        value = eval(self.formula, {"t": self.t})
                        self.byte_beat_values.append(0xFF & value)
                except Exception as error:
                    self.error = error

                try:
                    if is_byte_beat is False:
                        self.byte_beat_values.append(eval(self.formula, {
                            "t": self.t,
                            "sin": self.sin, "cos": self.cos, "tan": self.tan,
                            "OP8": self.OP8, "OP10":self.OP10, "OP16": self.OP16,
                            "BP8": self.BP8, "BP10":self.BP10, "BP16": self.BP16,
                            "RP8": self.OP8, "RP10":self.OP10, "RP16": self.RP16,
                            "GP8": self.GP8, "GP10":self.GP10, "GP16": self.OP16,
                            "OB": self.OB, "BB": self.BB, "RB": self.RB, "GB": self.GB
                        }))
                except Exception as error:
                    self.error = error

                self.increment()

    def to_pyaudio(self, is_byte_beat):
        try:
            if is_byte_beat is True:
                self.audio_int.write(bytes(self.byte_beat_values))
            else:
                samples = (np.array([x for x in self.byte_beat_values])).astype(np.float32)
                output_bytes = (0.5 * samples).tobytes()
                self.audio_float.write(output_bytes)
        except Exception as error:
            print(f'play error: {error}')

    @staticmethod
    def cos(x):
        return math.cos(x)

    @staticmethod
    def sin(t):
        return math.sin(t)

    @staticmethod
    def tan(x):
        return math.tan(x)

    @staticmethod
    def OP8(x):
        normalized_value = (x / 4095) * 8
        return round(normalized_value)

    @staticmethod
    def OP10(x):
        normalized_value = (x / 4095) * 10
        return round(normalized_value)

    @staticmethod
    def OP16(x):
        normalized_value = (x / 4095) * 16
        return round(normalized_value)

    @staticmethod
    def BP8(x):
        normalized_value = (x / 4095) * 8
        return round(normalized_value)

    @staticmethod
    def BP10(x):
        normalized_value = (x / 4095) * 10
        return round(normalized_value)

    @staticmethod
    def BP16(x):
        normalized_value = (x / 4095) * 16
        return round(normalized_value)

    @staticmethod
    def RP8(x):
        normalized_value = (x / 4095) * 8
        return round(normalized_value)

    @staticmethod
    def RP10(x):
        normalized_value = (x / 4095) * 10
        return round(normalized_value)

    @staticmethod
    def RP16(x):
        normalized_value = (x / 4095) * 16
        return round(normalized_value)

    @staticmethod
    def GP8(x):
        normalized_value = (x / 4095) * 8
        return round(normalized_value)

    @staticmethod
    def GP10(x):
        normalized_value = (x / 4095) * 10
        return round(normalized_value)

    @staticmethod
    def GP16(x):
        normalized_value = (x / 4095) * 16
        return round(normalized_value)

    @staticmethod
    def OB(x):
        if x is False:
            return 0
        return 0

    @staticmethod
    def BB(x):
        if x is False:
            return 0
        return 0

    @staticmethod
    def RB(x):
        if x is False:
            return 0
        return 0

    @staticmethod
    def GB(x):
        if x is False:
            return 0
        return 0
