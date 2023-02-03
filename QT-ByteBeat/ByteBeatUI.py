import argparse
import os
import time
import RPi.GPIO as GPIO
import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore as graphCore
from qtbytebeat import Ui_Form
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QStringListModel
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets as qtw
from Stylesheet import stylesheet
from Uart import Uart
from TinySQL import TinySQL
from PlayByteBeat import PlayByteBeat


# Define button connections on the raspberry pi 4
left_button_gpio = 23
right_button_gpio = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_button_gpio, GPIO.IN)
GPIO.setup(right_button_gpio, GPIO.IN)


class WorkerPlayer(QObject):
    finished = pyqtSignal()
    emit_graph_data = pyqtSignal(bool, int, bool, list)

    def __init__(self):
        super().__init__()
        # PlayByteBeat class
        self.byte_beat = PlayByteBeat()

        # Current en next Formula
        self.byte_beat.current_formula = 't'
        self.byte_beat.next_formula = ''

        # Current formula is byte or float beat
        self.is_byte_beat = True

        # Play states
        self.play = False
        self.byte_beat.t = 1

    def switch_play_pause(self):
        if self.byte_beat.current_formula != self.byte_beat.next_formula:
            is_valid, is_byte_beat = self.byte_beat.is_valid_formula(self.byte_beat.next_formula)
            if is_valid is True:
                self.byte_beat.current_formula = self.byte_beat.next_formula
                self.is_byte_beat = is_byte_beat
                if self.play is False:
                    self.play = not self.play
                time.sleep(0)
                return

        self.play = not self.play
        time.sleep(0)

    def switch_reverse(self):
        self.byte_beat.reverse = not self.byte_beat.reverse
        time.sleep(0)

    def stop_player(self):
        self.play = False
        self.byte_beat.reverse = False
        self.byte_beat.t = 1
        time.sleep(0)

    def run(self):
        while True:
            if self.play is True:
                self.byte_beat.compute(self.is_byte_beat)
                self.byte_beat.to_pyaudio(self.is_byte_beat)
                self.emit_graph_data.emit(self.is_byte_beat,
                                          self.byte_beat.t,
                                          self.byte_beat.reverse,
                                          self.byte_beat.byte_beat_values)
            time.sleep(0)


class WorkerSensors(QObject):
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
    button_right = pyqtSignal(dict)
    button_left_last_value = 0
    button_right_last_value = 0
    change_play_state = pyqtSignal(dict)

    def __init__(self, uart):
        super().__init__()
        self.uart = uart
        self.right_button_last_press_time = 0
        self.right_button_pressed = False
        self.reverse_emitted = False
        self.stop_emitted = False

    def on_right_button_release(self):
        delta = time.time() - self.right_button_last_press_time
        if 0 < delta < 0.4:
            # short press
            return {"play_pause": True, "pressed": False}
        if 0.4 < delta < 1:
            # medium press
            return {"reverse": True, "pressed": False}
        if delta > 1:
            # long press
            return {"stop": True, "pressed": False}

    # noinspection PyUnresolvedReferences
    def run(self):
        while True:
            try:
                message = self.uart.read()

                if message is not None:
                    if message['pico_0'] is not None:
                        self.button_1.emit(message['pico_0']['btn0'])
                        self.button_2.emit(message['pico_0']['btn1'])
                        self.potmeter_1.emit(message['pico_0']['adc0'])
                        self.potmeter_2.emit(message['pico_0']['adc1'])

                    if message['pico_1'] is not None:
                        self.button_3.emit(message['pico_1']['btn0'])
                        self.button_4.emit(message['pico_1']['btn1'])
                        self.potmeter_3.emit(message['pico_1']['adc0'])
                        self.potmeter_4.emit(message['pico_1']['adc1'])

                if GPIO.input(left_button_gpio) != self.button_left_last_value:
                    self.button_left.emit(GPIO.input(left_button_gpio))
                    self.button_left_last_value = GPIO.input(left_button_gpio)

                if GPIO.input(right_button_gpio) == 1 and self.right_button_pressed is False:
                    self.right_button_pressed = True
                    self.right_button_last_press_time = time.time()
                    self.button_right.emit({"pressed": True})
                elif GPIO.input(right_button_gpio) == 0 and self.right_button_pressed is True:
                    value = self.on_right_button_release()
                    self.button_right.emit(value)
                    self.right_button_pressed = False
                    self.reverse_emitted = False
                    self.stop_emitted = False
                    if 0 < time.time() - self.right_button_last_press_time < 0.4:
                        self.change_play_state.emit({'play_pause': True})

                if self.right_button_pressed is True:
                    if GPIO.input(right_button_gpio) == 1 and 0.4 < time.time() - self.right_button_last_press_time < 1:
                        if self.reverse_emitted is False:
                            self.reverse_emitted = True
                            self.change_play_state.emit({'reverse': True})
                    elif GPIO.input(right_button_gpio) == 1 and 1 < time.time() - self.right_button_last_press_time:
                        if self.stop_emitted is False:
                            self.stop_emitted = True
                            self.change_play_state.emit({'stop': True})

            except Exception as error:
                if self.debug:
                    print(error, flush=True)

            # We get two times 15 samples/s times two pico's
            time.sleep(0.07)


class ByteBeatUI(qtw.QWidget, Ui_Form):
    def __init__(self, pico_0, pico_1, debug, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pico_0 = pico_0
        self.pico_1 = pico_1
        self.debug = debug
        self.setupUi(self)

        # Setup database
        self.slots = []
        self.db = TinySQL('bytebeat.db')
        if self.db.is_new_db:
            [self.db.insert_row(f'slot {i}') for i in range(1, 21)]
        self.slots = self.db.read_all_rows()

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

        # Start pico read out and set button/dail values
        self.uart = Uart(pico_0=self.pico_0, pico_1=self.pico_1, debug=self.debug)

        # Setup Qthread and worker object for sensor reading
        self.sensor_thread = QThread()
        self.worker_sensor = WorkerSensors(self.uart)
        self.get_sensor_data()

        # Setup Qthread and worker object for player
        self.player_thread = QThread()
        self.worker_player = WorkerPlayer()
        self.start_player()

        # Connect a return pressed on the line edit to the qlistview
        self.formula_selector_model = QStringListModel(self.slots)
        self.formula_selector.setModel(self.formula_selector_model)
        self.formula_selector.clicked.connect(self.add_selected_formula_to_editor)
        self.formula_editor.returnPressed.connect(self.add_to_formula_selector)
        self.formula_editor.textChanged.connect(self.check_editted_formula)
        self.formula_selector.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.update_left_button(False, init=True)

        # Set input focus on formula-editor (so we don't need an extra computer, but just a keyboard)
        self.formula_editor.setFocus()

        # Playing states
        self.stop = False
        self.change_play_state({'stop': self.stop})
        self.update_right_button({'stop': True, 'pressed': False})

        # Show frequency plot
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', (255, 255, 255, 0))
        pg.setConfigOption('leftButtonPan', False)
        self.plot_window = self.frequency_plot.addPlot()
        # self.plot_window.hideAxis('left')
        self.plot_window.hideAxis('bottom')
        self.plot_window.setMenuEnabled(False)
        self.plot_window.setMouseEnabled(x=False, y=False)
        self.curve = self.plot_window.plot(pen='y')
        self.graph_buffer = np.empty(0)

    def right_button_clicked(self):
        self.worker_player.play = True

    def add_selected_formula_to_editor(self, index):
        text = index.data()
        self.formula_editor.setText(text)
        self.worker_player.next_formula = text

    def add_to_formula_selector(self):
        current_index = self.formula_selector.currentIndex()
        text = self.formula_editor.text()
        is_valid, is_byte_beat = self.worker_player.byte_beat.is_valid_formula(text)
        if is_valid is True:
            self.formula_selector_model.setData(self.formula_selector_model.index(current_index.row()), text)
            self.worker_player.byte_beat.next_formula = text
            self.db.update_row(current_index.row() + 1, text)

        if text == '':
            text = f'slot {current_index.row() + 1}'
            self.formula_selector_model.setData(self.formula_selector_model.index(current_index.row()), text)
            self.formula_editor.setText(text)
            self.db.update_row(current_index.row() + 1, text)

    def check_editted_formula(self):
        text = self.formula_editor.text()
        is_valid, is_byte_beat = self.worker_player.byte_beat.is_valid_formula(text)
        if is_valid is False:
            self.formula_editor.setStyleSheet("color: red;")
        else:
            self.formula_editor.setStyleSheet("color: black;")

    # noinspection PyUnresolvedReferences
    def get_sensor_data(self):
        # Move worker to the thread
        self.worker_sensor.moveToThread(self.sensor_thread)

        # Connect signals and slots
        self.sensor_thread.started.connect(self.worker_sensor.run)
        self.worker_sensor.finished.connect(self.sensor_thread.quit)
        self.worker_sensor.finished.connect(self.worker_sensor.deleteLater)
        self.sensor_thread.finished.connect(self.sensor_thread.deleteLater)

        self.worker_sensor.button_1.connect(self.update_button_1)
        self.worker_sensor.button_2.connect(self.update_button_2)
        self.worker_sensor.button_3.connect(self.update_button_3)
        self.worker_sensor.button_4.connect(self.update_button_4)
        self.worker_sensor.potmeter_1.connect(self.update_potmeter_1)
        self.worker_sensor.potmeter_2.connect(self.update_potmeter_2)
        self.worker_sensor.potmeter_3.connect(self.update_potmeter_3)
        self.worker_sensor.potmeter_4.connect(self.update_potmeter_4)
        self.worker_sensor.button_left.connect(self.update_left_button)
        self.worker_sensor.button_right.connect(self.update_right_button)
        self.worker_sensor.change_play_state.connect(self.change_play_state)
        self.right_button_pressed = False

        # Start the thread
        self.sensor_thread.start()

    def start_player(self):
        # Move worker to the thread
        self.worker_player.moveToThread(self.player_thread)

        # Connect signals and slots
        self.player_thread.started.connect(self.worker_player.run)
        self.worker_player.finished.connect(self.player_thread.quit)
        self.worker_player.finished.connect(self.worker_player.deleteLater)
        self.player_thread.finished.connect(self.player_thread.deleteLater)
        self.worker_player.emit_graph_data.connect(self.update_graph)

        # Start the thread
        self.player_thread.start()

    def update_graph(self, is_byte_beat, t, reverse, data):
        data = np.array(data)
        seconds = 2
        time_delta = 1 + 256 * 4 * 8 * seconds
        if len(self.graph_buffer) == 0:
            self.graph_buffer = np.zeros(time_delta)

        if reverse is True:
            self.graph_buffer = np.concatenate((data, self.graph_buffer))
            if len(self.graph_buffer) > time_delta:
                self.graph_buffer = self.graph_buffer[:time_delta]
        else:
            self.graph_buffer = np.concatenate((self.graph_buffer, data))
            if len(self.graph_buffer) > time_delta:
                self.graph_buffer = self.graph_buffer[-time_delta:]

        self.curve.setData(self.graph_buffer)
        self.plot_window.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted

    def update_button_1(self, status):
        self.button_1.setEnabled(status)
        self.worker_player.byte_beat.OB_value = status

    def update_button_2(self, status):
        self.button_2.setEnabled(status)
        self.worker_player.byte_beat.BB_value = status

    def update_button_3(self, status):
        self.button_3.setEnabled(status)
        self.worker_player.byte_beat.GB_value = status

    def update_button_4(self, status):
        self.button_4.setEnabled(status)
        self.worker_player.byte_beat.RB_value = status

    def update_potmeter_1(self, value):
        self.potmeter_1.setValue(value)
        self.worker_player.byte_beat.OP_value = value

    def update_potmeter_2(self, value):
        self.potmeter_2.setValue(value)
        self.worker_player.byte_beat.BP_value = value

    def update_potmeter_3(self, value):
        self.potmeter_3.setValue(value)
        self.worker_player.byte_beat.GP_value = value

    def update_potmeter_4(self, value):
        self.potmeter_4.setValue(value)
        self.worker_player.byte_beat.RP_value = value

    def update_left_button(self, status, init=False):
        self.button_left.setEnabled(status)
        if status is True or init is True:
            row_count = self.formula_selector_model.rowCount()
            if init is True:
                first_index = self.formula_selector_model.index(row_count - 1)
                self.formula_selector.setCurrentIndex(first_index)

            current_index = self.formula_selector.currentIndex()
            next_index = current_index.sibling(current_index.row() + 1, 0)

            if current_index.row() + 1 == row_count:
                next_index = current_index.sibling(0, 0)
            self.formula_selector.setCurrentIndex(next_index)
            self.formula_selector.scrollTo(next_index)

            # Update formula_editor
            selected_text = self.formula_selector_model.data(next_index, 0)
            self.formula_editor.setText(selected_text)
            self.worker_player.byte_beat.next_formula = selected_text

    def update_right_button(self, status):
        self.button_right.setEnabled(status['pressed'])
        if status['pressed'] is False:
            if 'play_pause' in status and status['play_pause']:
                self.worker_player.switch_play_pause()

            if 'reverse' in status and status['reverse']:
                self.worker_player.switch_reverse()

            if 'stop' in status and status['stop']:
                self.worker_player.stop_player()

    def change_play_state(self, status):
        if 'stop' in status:
            self.play = False
            self.reverse = False
            self.stop = True
        elif 'play_pause' in status:
            self.play = not self.play
            if self.play:
                self.stop = False
        elif 'reverse' in status:
            self.reverse = not self.reverse

        if self.stop:
            self.play_status.setText('||')
        elif self.play and not self.reverse:
            self.play_status.setText('>')
        elif self.play and self.reverse:
            self.play_status.setText('<')
        elif not self.play and not self.reverse:
            self.play_status.setText('>|')
        elif not self.play and self.reverse:
            self.play_status.setText('|<')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p0", "--pico_0", help="Serial device pico0 (/dev/ttyAMA0)", type=str, default='/dev/ttyAMA0')
    parser.add_argument("-p1", "--pico_1", help="Serial device pico1 (/dev/ttyAMA1)", type=str, default='/dev/ttyAMA1')
    parser.add_argument("-D", "--debug", help="Enable debug mode", default=False, action="store_true")
    args = parser.parse_args()
    pico_0 = args.pico_0
    pico_1 = args.pico_1
    debug = args.debug

    app = qtw.QApplication([])
    app.setStyleSheet(stylesheet)
    cwd = os.getcwd()
    QtCore.QDir.addSearchPath('bg', f'{cwd}')
    widget = ByteBeatUI(pico_0, pico_1, debug)
    widget.show()

    app.exec()
