import math
import numpy as np
from pyaudio import PyAudio, paUInt8, paFloat32


class PlayByteBeat():
    def __init__(self, formula, positive=True):
        pa = PyAudio()
        self.audio_int = pa.open(format=paUInt8, channels=1, rate=8000, output=True)
        self.audio_float = pa.open(format=paFloat32, channels=1, rate=8000, output=True)
        self.formula = formula
        self.probe_formula = formula
        self.four_hours = 3600 * 4 * 8000  # 3600 * 4 * 8khz samples
        self.t = 1
        self.positive = positive
        self.byte_beat_values = []
        self.error = ""

    def reset_time(self):
        self.t = 1

    def increment(self):
        if self.positive:
            self.t += 1
        else:
            self.t -= 1

    @staticmethod
    def cos(x):
        return math.cos(x)

    @staticmethod
    def sin(t):
        return math.sin(t)

    @staticmethod
    def tan(x):
        return math.tan(x)

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
            eval(formula, {"t": 1, "sin": self.sin, "cos": self.cos, "tan": self.tan})
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
                            "sin": self.sin,
                            "cos": self.cos,
                            "tan": self.tan
                        }))
                except Exception as error:
                    self.error = error

                self.increment()

    def play(self, is_byte_beat):
        try:
            if is_byte_beat is True:
                self.audio_int.write(bytes(self.byte_beat_values))
            else:
                samples = (np.array([x for x in self.byte_beat_values])).astype(np.float32)
                output_bytes = (0.5 * samples).tobytes()
                self.audio_float.write(output_bytes)
        except Exception as error:
            print(f'play error: {error}')
