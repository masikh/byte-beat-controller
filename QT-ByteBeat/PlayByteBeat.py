import math
import numpy as np
import re
from pyaudio import PyAudio, paUInt8, paFloat32


class PlayByteBeat():
    def __init__(self):
        self.pa = PyAudio()
        self.audio_int = self.pa.open(format=paUInt8, channels=1, rate=8000, output=True)
        self.audio_float = self.pa.open(format=paFloat32, channels=1, rate=8000, output=True)
        self.current_formula = 't'
        self.next_formula = 't'

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
        self.pattern_OPi = re.compile('(OPi)(\[)(\d+)(])')
        self.pattern_OPf = re.compile('(OPf)(\[)(\d+)(])')
        self.pattern_BPi = re.compile('(BPi)(\[)(\d+)(])')
        self.pattern_BPf = re.compile('(BPf)(\[)(\d+)(])')
        self.pattern_GPi = re.compile('(GPi)(\[)(\d+)(])')
        self.pattern_GPf = re.compile('(GPf)(\[)(\d+)(])')
        self.pattern_RPi = re.compile('(RPi)(\[)(\d+)(])')
        self.pattern_RPf = re.compile('(RPf)(\[)(\d+)(])')
        self.pattern_OB = re.compile('OB')
        self.pattern_BB = re.compile('BB')
        self.pattern_GB = re.compile('GB')
        self.pattern_RB = re.compile('RB')

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
        formula = self.replace(formula)
        try:
            eval(formula, {'t': 10000})
            return True, True
        except Exception as error:
            self.error = error

        try:
            eval(formula, {"t": 10000, "sin": self.sin, "cos": self.cos, "tan": self.tan})
            return True, False
        except Exception as error:
            self.error = error

        return False, False

    def compute(self, is_byte_beat):
        self.byte_beat_values = []
        if abs(self.t) > self.four_hours:
            self.t = 1

        formula = self.replace(self.current_formula)
        for _i in range(0x80):
            try:
                if is_byte_beat is True:
                    value = eval(formula, {'t': self.t})
                    self.byte_beat_values.append(0xFF & value)
            except Exception as error:
                self.error = error

            try:
                if is_byte_beat is False:
                    self.byte_beat_values.append(eval(formula, {'t': self.t, 'sin': self.sin, 'cos': self.cos, 'tan': self.tan}))
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
    def norm_i(value, factor):
        """ Normalize value with factor, return int """
        normalized_value = (((value + 0.000000000001) / 4095) * (factor - 1)) + 1
        return round(normalized_value)  # Value between 1 and factor

    @staticmethod
    def norm_f(value, factor):
        """ Normalize value with factor, return float """
        value = round((value + 0.000000000001) / 50) * 50  # 50 is about the average sweep of a potmeter...
        return ((value + 0.000000000001) / 4095) * factor  # Value between virtually 0 and factor

    @staticmethod
    def button(value):
        if value is True:
            return 1
        return 0

    def replace(self, formula):
        # Substitute OPi[n] or OPf[n] for its normalized value based on OP_value and n, respectively for int or float.
        match = self.pattern_OPi.search(formula)
        if match:
            formula = self.pattern_OPi.sub(str(self.norm_i(self.OP_value, float(match.group(3)))), formula)
        match = self.pattern_OPf.search(formula)
        if match:
            formula = self.pattern_OPf.sub(str(self.norm_f(self.OP_value, float(match.group(3)))), formula)

        # Substitute BPi[n] or BPf[n] for its normalized value based on BP_value and n, respectively for int or float.
        match = self.pattern_BPi.search(formula)
        if match:
            formula = self.pattern_BPi.sub(str(self.norm_i(self.BP_value, float(match.group(3)))), formula)
        match = self.pattern_BPf.search(formula)
        if match:
            formula = self.pattern_BPf.sub(str(self.norm_f(self.BP_value, float(match.group(3)))), formula)

        # Substitute GPi[n] or GPf[n] for its normalized value based on GP_value and n, respectively for int or float.
        match = self.pattern_GPi.search(formula)
        if match:
            formula = self.pattern_GPi.sub(str(self.norm_i(self.GP_value, float(match.group(3)))), formula)
        match = self.pattern_GPf.search(formula)
        if match:
            formula = self.pattern_GPf.sub(str(self.norm_f(self.GP_value, float(match.group(3)))), formula)

        # Substitute RPi[n] or RPf[n] for its normalized value based on RP_value and n, respectively for int or float.
        match = self.pattern_RPi.search(formula)
        if match:
            formula = self.pattern_RPi.sub(str(self.norm_i(self.RP_value, float(match.group(3)))), formula)
        match = self.pattern_RPf.search(formula)
        if match:
            formula = self.pattern_RPf.sub(str(self.norm_f(self.RP_value, float(match.group(3)))), formula)

        match = self.pattern_OB.search(formula)
        if match:
            formula = self.pattern_OB.sub(str(self.button(self.OB_value)), formula)

        match = self.pattern_BB.search(formula)
        if match:
            formula = self.pattern_BB.sub(str(self.button(self.BB_value)), formula)

        match = self.pattern_GB.search(formula)
        if match:
            formula = self.pattern_GB.sub(str(self.button(self.GB_value)), formula)

        match = self.pattern_RB.search(formula)
        if match:
            formula = self.pattern_RB.sub(str(self.button(self.RB_value)), formula)

        return formula
