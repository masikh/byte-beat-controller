import argparse
import os
import time
import RPi.GPIO as GPIO
from qtbytebeat import Ui_Form
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtWidgets as qtw
from Stylesheet import stylesheet
from Uart import Uart

left_button_gpio = 23
right_button_gpio = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_button_gpio, GPIO.IN)
GPIO.setup(right_button_gpio, GPIO.IN)


class Worker(QObject):
    finished = pyqtSignal()
    button_1 = pyqtSignal(bool)
    button_2 = pyqtSignal(bool)
    button_3 = pyqtSignal(bool)
    button_4 = pyqtSignal(bool)
    potmeter_1 = pyqtSignal(int)
    potmeter_2 = pyqtSignal(int)
    potmeter_3 = pyqtSignal(int)
    potmeter_4 = pyqtSignal(int)
    button_left = pyqtSignal(bool)
    button_right = pyqtSignal(bool)

    def __init__(self, uart, debug):
        super().__init__()
        self.uart = uart
        self.debug = debug

    # noinspection PyUnresolvedReferences
    def run(self):
        while True:
            try:
                if self.debug:
                    message = self.uart.mock()
                else:
                    message = self.uart.read()

                if message is not None:
                    self.button_1.emit(message['48']['btn0'])
                    self.button_2.emit(message['48']['btn1'])
                    self.potmeter_1.emit(message['48']['adc0'])
                    self.potmeter_2.emit(message['48']['adc1'])

                    self.button_3.emit(message['49']['btn0'])
                    self.button_4.emit(message['49']['btn1'])
                    self.potmeter_3.emit(message['49']['adc0'])
                    self.potmeter_4.emit(message['49']['adc1'])
                else:
                    # Something went wrong, give the uart time to clean up...
                    sleep(1)

                if GPIO.input(left_button_gpio) == 1:
                    self.button_left.emit(True)
                else:
                    self.button_left.emit(False)

                if GPIO.input(right_button_gpio) == 1:
                    self.button_right.emit(True)
                else:
                    self.button_right.emit(False)

            except Exception as error:
                if self.debug:
                    print(error, flush=True)

            # We get two times 15 samples/s times two pico's
            time.sleep(0.07)


class ByteBeatUI(qtw.QWidget, Ui_Form):
    def __init__(self, device_file, debug, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device_file = device_file
        self.debug = debug
        self.setupUi(self)
        # self.showMaximized()

        # Set initial button values
        self.button_1.setEnabled(False)
        self.button_2.setEnabled(False)
        self.button_3.setEnabled(False)
        self.button_4.setEnabled(False)

        # Set potmeter ranges
        self.potmeter_1.setRange(0, 4095)
        self.potmeter_2.setRange(0, 4095)
        self.potmeter_3.setRange(0, 4095)
        self.potmeter_4.setRange(0, 4095)

        # Set Raspberry PI push-buttons
        self.button_left.setEnabled(False)
        self.button_right.setEnabled(False)

        # Autocorrect and interpret
        self.byte_beat_formula = ''
        self.formula_editor.textEdited.connect(self.interpret_bytebeat_formula)

        # Start pico read out and set button/dail values
        self.uart = Uart(self.device_file, debug=self.debug)

        # Setup Qthread and worker object
        self.thread = QThread()
        self.worker = Worker(self.uart, self.debug)
        self.get_sensor_data()

    def interpret_bytebeat_formula(self, formula):
        self.byte_beat_formula = formula.replace(' ', '')
        self.formula_editor.setText(self.byte_beat_formula)

    # noinspection PyUnresolvedReferences
    def get_sensor_data(self):
        # Move worker to the thread
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.button_1.connect(self.update_button_1)
        self.worker.button_2.connect(self.update_button_2)
        self.worker.button_3.connect(self.update_button_3)
        self.worker.button_4.connect(self.update_button_4)
        self.worker.potmeter_1.connect(self.update_potmeter_1)
        self.worker.potmeter_2.connect(self.update_potmeter_2)
        self.worker.potmeter_3.connect(self.update_potmeter_3)
        self.worker.potmeter_4.connect(self.update_potmeter_4)
        self.worker.button_left.connect(self.update_left_button)
        self.worker.button_right.connect(self.update_right_button)

        # Start the thread
        self.thread.start()

    def update_button_1(self, status):
        self.button_1.setEnabled(status)

    def update_button_2(self, status):
        self.button_2.setEnabled(status)

    def update_button_3(self, status):
        self.button_3.setEnabled(status)

    def update_button_4(self, status):
        self.button_4.setEnabled(status)

    def update_potmeter_1(self, value):
        self.potmeter_1.setValue(value)

    def update_potmeter_2(self, value):
        self.potmeter_2.setValue(value)

    def update_potmeter_3(self, value):
        self.potmeter_3.setValue(value)

    def update_potmeter_4(self, value):
        self.potmeter_4.setValue(value)

    def update_left_button(self, status):
        self.button_left.setEnabled(status)

    def update_right_button(self, status):
        self.button_right.setEnabled(status)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device_file", help="Serial device (/dev/serial0)", type=str, default='/dev/serial0')
    parser.add_argument("-D", "--debug", help="Enable debug mode", default=False, action="store_true")
    args = parser.parse_args()
    device_file = args.device_file
    debug = args.debug

    app = qtw.QApplication([])
    app.setStyleSheet(stylesheet)
    cwd = os.getcwd()
    QtCore.QDir.addSearchPath('bg', f'{cwd}')
    widget = ByteBeatUI(device_file=device_file, debug=debug)
    widget.show()

    app.exec()


