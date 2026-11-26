import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class SessionCounter(QWidget):
    def __init__(self, sessions: int):
        super().__init__()

        self.complete_count = 0
        self.incomplete = "⚪️"
        self.complete = "🟢"

        self.session_widget_style = """
            QLabel { 
            background-color: blue
            border-radius: 10px 
        }
        """

        # Build UI
        self._layout = QHBoxLayout()
        self._layout.setSpacing(10)

        self.session_widgets = []
        for i in range(sessions):
            _widget = self._create_session_widget()
            self._layout.addWidget(_widget)
            self.session_widgets.append(_widget)

        self.setLayout(self._layout)

    def _create_session_widget(self):
        session_label = QLabel(self.incomplete)
        # session_label.setStyleSheet(self.session_widget_style)
        # session_label.setFixedSize(self.size, self.size)
        return session_label

    def update_status_labels(self):
         # Clear all widgets
        for i, w in enumerate(self.session_widgets):
            w.setText(self.complete if i < self.complete_count else self.incomplete)

    def increment_completed(self):
        if self.complete_count < len(self.session_widgets):
            self.complete_count += 1
        self.update_status_labels()

    def set_completed_session(self, count: int):
        if count > len(self.session_widgets):
            return

        self.complete_count = count
        self.update_status_labels()      

class TimerWidget(QWidget):
    """
        Main clock widget with start and stop functionality
    """
    def __init__(self, sessions: int = 4, session_duration: int = 30):
        super().__init__()
        self.timer_layout = QVBoxLayout()
        self.time = QTime(0, 0, 0)
        self.time_format = "hh:mm:ss"
        self.max_time_minutes = 60 * 6
        self.duration = (0,0,0)
        self.overtime = False
        self.overtime_style = "QLCDNumber {background-color: blue}"
        self.default_style = "QLCDNumber {background-color: red}"

        # Session counter widget
        self.session_counter = SessionCounter(sessions=4)

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
        self.timer_layout.addWidget(self.session_counter)
        self.timer_layout.addLayout(self.btn_layout)
        self.setLayout(self.timer_layout)

        # Set duration
        self.set_time_minutes(session_duration if session_duration else 0)


    def set_time_minutes(self, minutes: int):
        self.time.setHMS(0, minutes, 0)
        self.lcd.display(self.time.toString(self.time_format))
        
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



class AnimationScreen(QWidget):
    def __init__(self):
        super().__init__()


class Tasks(QWidget):
    def __init__(self):
        super().__init()

class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # main layout
        self.main_layout = QGridLayout()
        self.animation_screen = AnimationScreen()
        self.timer_widget = TimerWidget()

        self.main_layout.addWidget(self.timer_widget, 0, 0)
        self.main_layout.addWidget(self.animation_screen, 0, 1)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # REsize
        self.resize(500, 300)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerApp()
    window.show()
    sys.exit(app.exec_())