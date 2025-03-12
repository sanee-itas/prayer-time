import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                            QWidget, QLabel, QGridLayout)
from PyQt5.QtCore import Qt, QTimer

class PrayerTimesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Masjid Bilal Canton (MBC)")
        self.setGeometry(0, 0, 800, 480)  # Common resolution for Pi displays

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.central_widget.setStyleSheet("background-color: #800000;")  # Red border background

        # Left panel (stacked white and green vertically)
        self.left_panel = QWidget()
        self.left_panel_layout = QVBoxLayout(self.left_panel)
        self.left_panel.setStyleSheet("background-color: #800000;")  # Transparent to show red border

        # White section (clock and info)
        self.white_section = QWidget()
        self.white_section.setStyleSheet("background-color: #F5F5F5; padding: 10px;")
        self.white_layout = QVBoxLayout(self.white_section)
        self.white_layout.setAlignment(Qt.AlignCenter)

        self.clock_label = QLabel()
        self.clock_label.setStyleSheet("font-size: 72px; font-weight: bold; color: black;")
        self.update_clock()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

        self.title_label = QLabel("Masjid Bilal Canton (MBC)")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        self.date_label = QLabel("Wednesday\n12 March, 2025\n12 Ramadan, 1446")
        self.date_label.setStyleSheet("font-size: 18px; color: black; text-align: center;")
        self.date_label.setAlignment(Qt.AlignCenter)
        self.support_label = QLabel("Support Us")
        self.support_label.setStyleSheet("font-size: 16px; color: blue; text-decoration: underline;")

        self.white_layout.addWidget(self.clock_label)
        self.white_layout.addWidget(self.title_label)
        self.white_layout.addWidget(self.date_label)
        self.white_layout.addWidget(self.support_label)
        self.white_layout.addStretch()

        # Green section (next prayer)
        self.green_section = QWidget()
        self.green_section.setStyleSheet("background-color: #32CD32; padding: 10px;")
        self.green_layout = QVBoxLayout(self.green_section)
        self.green_layout.setAlignment(Qt.AlignCenter)

        next_prayer_index = self.get_next_prayer(self.get_prayer_data())
        next_prayer = self.get_prayer_data()[next_prayer_index]
        next_prayer_label = QLabel(next_prayer["name"])
        next_prayer_label.setStyleSheet("font-size: 36px; color: white; font-weight: bold;")
        start_label = QLabel(f"Start\n{next_prayer['start']}")
        start_label.setStyleSheet("font-size: 48px; color: black; font-weight: bold;")
        iqama_label = QLabel(f"Iqama\n{next_prayer['iqama']}")
        iqama_label.setStyleSheet("font-size: 48px; color: black; font-weight: bold;")

        self.green_layout.addWidget(next_prayer_label)
        self.green_layout.addWidget(start_label)
        self.green_layout.addWidget(iqama_label)
        self.green_layout.addStretch()

        # Add white and green sections to left panel
        self.left_panel_layout.addWidget(self.white_section)
        self.left_panel_layout.addWidget(self.green_section)

        # Right panel (prayer times table)
        self.right_panel = QWidget()
        self.right_panel.setStyleSheet("background-color: #4682B4;")
        self.table_layout = QGridLayout(self.right_panel)
        self.table_layout.setHorizontalSpacing(5)
        self.table_layout.setVerticalSpacing(5)

        self.table_layout.addWidget(QLabel("Tomorrow"), 0, 1)
        self.table_layout.addWidget(QLabel("Start"), 0, 2)
        self.table_layout.addWidget(QLabel("Iqama"), 0, 3)

        prayers = self.get_prayer_data()
        for i, prayer in enumerate(prayers):
            name_label = QLabel(prayer["name"])
            name_label.setStyleSheet("color: white; font-size: 20px; background-color: #4682B4; padding: 5px;")
            start_label = QLabel(prayer["start"])
            start_label.setStyleSheet(f"color: {'#FFD700' if i == next_prayer_index else '#32CD32'}; font-size: 20px; text-align: right; padding: 5px; background-color: #4682B4;")
            iqama_label = QLabel(prayer["iqama"] if prayer["iqama"] else "")
            iqama_label.setStyleSheet(f"color: {'#FFD700' if i == next_prayer_index else '#32CD32'}; font-size: 20px; text-align: right; padding: 5px; background-color: #4682B4;")

            self.table_layout.addWidget(name_label, i + 1, 1)
            self.table_layout.addWidget(start_label, i + 1, 2)
            self.table_layout.addWidget(iqama_label, i + 1, 3)

        # Add panels to main layout
        self.main_layout.addWidget(self.left_panel, 1)  
        self.main_layout.addWidget(self.right_panel, 1)

    def update_clock(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.clock_label.setText(current_time)

    def get_prayer_data(self):
        return [
            {"name": "Fajr", "start": "6:34", "iqama": "6:54"},
            {"name": "Shurooq", "start": "7:51", "iqama": ""},
            {"name": "Zuhr", "start": "1:44", "iqama": "2:00"},
            {"name": "Asr", "start": "5:50", "iqama": "6:15"},
            {"name": "Maghrib", "start": "7:38", "iqama": "7:53"},
            {"name": "Isha", "start": "8:54", "iqama": "9:09"},
            {"name": "Jum'ah", "start": "", "iqama": "2:10", "khutbah": "2:10"}
        ]

    def get_next_prayer(self, prayers):
        now = datetime.now()
        current_time = now.hour * 60 + now.minute
        for i, prayer in enumerate(prayers):
            if prayer["start"]:
                time_obj = datetime.strptime(prayer["start"], '%H:%M')
                prayer_minutes = time_obj.hour * 60 + time_obj.minute
                if prayer_minutes > current_time:
                    return i
        return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PrayerTimesApp()
    window.show()
    sys.exit(app.exec_())