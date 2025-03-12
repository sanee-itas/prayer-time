import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                            QWidget, QLabel, QHBoxLayout)
from PyQt5.QtCore import Qt

class PrayerTimesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prayer Times")
        self.setGeometry(100, 100, 1024, 600)

        # Central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Set background color
        self.central_widget.setStyleSheet("background-color: #1A1A1A;")

        # Load title and prayer times
        self.load_title()
        self.load_prayer_times()

    def load_title(self):
        date_label = QLabel("12th March 2024")
        date_label.setStyleSheet("""
            color: white;
            font-size: 36px;
            font-weight: bold;
        """)
        date_label.setAlignment(Qt.AlignCenter)

        hijri_label = QLabel("12 Ramadhan 1446 AH")
        hijri_label.setStyleSheet("""
            color: #A0A0A0;
            font-size: 24px;
        """)
        hijri_label.setAlignment(Qt.AlignCenter)

        divider = QWidget()
        divider.setFixedSize(128, 4)
        divider.setStyleSheet("""
            background-color: #4CAF50;
            border-radius: 2px;
        """)

        self.main_layout.addWidget(date_label)
        self.main_layout.addWidget(hijri_label)
        self.main_layout.addWidget(divider, alignment=Qt.AlignCenter)
        self.main_layout.addSpacing(20)

    def get_next_prayer(self, prayer_times):
        now = datetime.now()
        current_time = now.hour * 60 + now.minute

        for i, prayer in enumerate(prayer_times):
            time_obj = datetime.strptime(prayer['time'], '%I:%M %p')
            prayer_minutes = time_obj.hour * 60 + time_obj.minute
            if prayer_minutes > current_time:
                return i
        return 0

    def load_prayer_times(self):
        prayer_times = [
            {'name': 'Fajr', 'time': '5:41 AM'},
            {'name': 'Dhuhr', 'time': '12:44 PM'},
            {'name': 'Asr', 'time': '3:55 PM'},
            {'name': 'Maghrib', 'time': '6:59 PM'},
            {'name': 'Isha', 'time': '7:39 PM'},
        ]

        next_prayer_index = self.get_next_prayer(prayer_times)

        for i, prayer in enumerate(prayer_times):
            prayer_widget = QWidget()
            is_next_prayer = (i == next_prayer_index)
            prayer_widget.setStyleSheet("""
                padding: 10px;
            """)
            
            prayer_layout = QHBoxLayout(prayer_widget)
            prayer_layout.setContentsMargins(10, 10, 10, 10)

            # Prayer name label
            name_label = QLabel(prayer['name'])
            name_label.setStyleSheet("""
                color: {color};
                font-size: 28px;
                font-weight: bold;
            """.format(color="#4CAF50" if is_next_prayer else "white"))

            # Prayer time label
            time_label = QLabel(prayer['time'])
            time_label.setStyleSheet("""
                color: {color};
                font-size: 28px;
                font-weight: bold;
            """.format(color="#4CAF50" if is_next_prayer else "white"))

            # Add stretch on both sides and between (space-around effect)
            prayer_layout.addStretch(1)  # Space before name
            prayer_layout.addWidget(name_label)
            prayer_layout.addStretch(1)  # Space between name and time
            prayer_layout.addWidget(time_label)
            prayer_layout.addStretch(1)  # Space after time

            # Add to main layout
            self.main_layout.addWidget(prayer_widget)
            self.main_layout.setStretchFactor(prayer_widget, 1)
            self.main_layout.addSpacing(10)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PrayerTimesApp()
    window.show()
    sys.exit(app.exec_())