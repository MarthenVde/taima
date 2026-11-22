import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class TimerWidget(QWidget):
    """
        Main clock widget with start and stop functionality
    """
    def __init__(self):
        super().__init__()
        self.timer_layout = QVBoxLayout()
        self.time = QTime(0, 0, 0)
        self.time_format = "hh:mm:ss"
        self.max_time_minutes = 60 * 6
        self.duration = (0,0,0)
        self.overtime = False
        self.overtime_style = "QLCDNumber {background-color: blue}"
        self.default_style = "QLCDNumber {background-color: red}"

        # setup lcd screen
        self.lcd = QLCDNumber()
        self.lcd.setDigitCount(8)
        self.lcd.display(self.time.toString(self.time_format))
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.setStyleSheet(self.default_style)

        # create start and stop buttons
        self.stop_button = QPushButton("Stop")
        self.start_button  = QPushButton("Start")
        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.start_button)
        self.btn_layout.addWidget(self.stop_button)

        # Connect buttons
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        # Setup timer
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.on_tick)

        # Setup layout
        self.timer_layout.addWidget(self.lcd)
        self.timer_layout.addLayout(self.btn_layout)
        self.setLayout(self.timer_layout)

        self.setFixedSize(320, 120)

    def set_duration(self, time: tuple):
        if len(time) != 3:
            raise Exception("Invalid time format: needs to be (h,m,s)")
        self.time.setHMS(time[0], time[1], time[2])
        self.lcd.display(self.time.toString(self.time_format))
        self.duration = time
        
    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def on_tick(self):
        self.time = self.time.addSecs(1 if self.overtime else -1)
        # Set display
        time_string = self.time.toString(self.time_format)
        
        if not self.overtime and time_string == "00:00:00":
            self.start_overtime_mode()

        self.lcd.display(time_string)

    def start_overtime_mode(self):
        self.lcd.setStyleSheet(self.overtime_style)
        self.overtime = True
        self.time.setHMS(self.duration[0], self.duration[1], self.duration[2])
        self.lcd.setStyleSheet(self.overtime_style)

class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # main layout
        self.main_layout = QGridLayout()
        self.timer_widget = TimerWidget()
        self.main_layout.addWidget(self.timer_widget, 0, 0)

        self.timer_widget.set_duration((0, 0, 5))

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerApp()
    window.show()
    sys.exit(app.exec_())