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
        start_label = QLabel(f"Start\n{next_prayer['start_tomorrow']}")
        start_label.setStyleSheet("font-size: 48px; color: black; font-weight: bold;")
        iqama_label = QLabel(f"Iqama\n{next_prayer['iqama_tomorrow']}")
        iqama_label.setStyleSheet("font-size: 48px; color: black; font-weight: bold;")

        self.green_layout.addWidget(next_prayer_label)
        self.green_layout.addWidget(start_label)
        self.green_layout.addWidget(iqama_label)
        self.green_layout.addStretch()

        # Add white and green sections to left panel
        self.left_panel_layout.addWidget(self.white_section)
        self.left_panel_layout.addWidget(self.green_section)

        # Right panel (prayer times table, integrated from PrayerTimesTable)
        self.right_panel = QWidget()
        self.right_panel.setStyleSheet("background-color: #800000;")  # Red background for gaps
        self.table_layout = QGridLayout(self.right_panel)
        self.table_layout.setHorizontalSpacing(10)  # Equal gaps between columns
        self.table_layout.setVerticalSpacing(10)    # Equal gaps between rows

        # Set column widths (stretch factors) for the entire layout
        self.table_layout.setColumnStretch(0, 4)  # Prayer name (40%)
        self.table_layout.setColumnStretch(1, 3)  # Start (30%)
        self.table_layout.setColumnStretch(2, 4)  # Iqama (40%)

        # Get prayer data and next prayer index
        prayers = self.get_prayer_data()
        next_prayer_index = self.get_next_prayer(prayers)

        # Row 1: Header Row
        header_date_label = QLabel("12 Ramadan, 1446")
        header_date_label.setStyleSheet("color: white; font-size: 14px; background-color: #4682B4; padding: 5px; text-align: left;")
        header_date_label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        header_start_label = QLabel("Start")
        header_start_label.setStyleSheet("color: white; font-size: 55px; background-color: #4682B4; text-align: center; padding: 5px;")
        header_start_label.setAlignment(Qt.AlignCenter)
        header_iqama_label = QLabel("Iqama")
        header_iqama_label.setStyleSheet("color: white; font-size: 55px; background-color: #4682B4; text-align: center; padding: 5px;")
        header_iqama_label.setAlignment(Qt.AlignCenter)

        self.table_layout.addWidget(header_date_label, 0, 0)
        self.table_layout.addWidget(header_start_label, 0, 1)
        self.table_layout.addWidget(header_iqama_label, 0, 2)

        # Rows 2, 4, 5, 6, 7: Fajr, Zuhr, Asr, Maghrib, Isha (3 columns)
        row_indices = [2, 4, 5, 6, 7]
        prayer_indices = [0, 2, 3, 4, 5]  # Fajr, Zuhr, Asr, Maghrib, Isha
        for row, prayer_idx in zip(row_indices, prayer_indices):
            prayer_data = prayers[prayer_idx]
            is_next_prayer = (prayer_idx == next_prayer_index)
            time_color = '#FFD700' if is_next_prayer else '#32CD32'

            # First column: Prayer name
            name_label = QLabel(prayer_data["name"])
            name_label.setStyleSheet("color: white; font-size: 55px; background-color: #4682B4; padding: 5px;")

            # Second column: Start (bold Tomorrow center, small Today bottom-right)
            start_widget = QWidget()
            start_widget.setStyleSheet("background-color: #32CD32; color: white;")
            start_layout = QVBoxLayout(start_widget)
            start_layout.setContentsMargins(5, 5, 5, 5)
            start_layout.setSpacing(0)

            start_layout.addStretch(1)
            start_bold_label = QLabel(prayer_data["start_tomorrow"])
            start_bold_label.setStyleSheet("color: white; font-size: 55px; font-weight: bold; text-align: center;")
            start_bold_label.setAlignment(Qt.AlignCenter)

            start_center_widget = QWidget()
            start_center_layout = QHBoxLayout(start_center_widget)
            start_center_layout.addStretch(1)
            start_center_layout.addWidget(start_bold_label)
            start_center_layout.addStretch(1)

            start_layout.addWidget(start_center_widget)
            start_layout.addStretch(1)

            start_small_label = QLabel(prayer_data["start_today"])
            start_small_label.setStyleSheet("color: white; font-size: 12px; text-align: right;")
            start_small_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)

            start_layout.addWidget(start_small_label)

            # Third column: Iqama (bold Tomorrow center, small Today bottom-right)
            iqama_widget = QWidget()
            iqama_widget.setStyleSheet("background-color: #32CD32; color: white;")
            iqama_layout = QVBoxLayout(iqama_widget)
            iqama_layout.setContentsMargins(5, 5, 5, 5)
            iqama_layout.setSpacing(0)

            iqama_layout.addStretch(1)
            iqama_bold_label = QLabel(prayer_data["iqama_tomorrow"])
            iqama_bold_label.setStyleSheet("color: white; font-size: 55px; font-weight: bold; text-align: center;")
            iqama_bold_label.setAlignment(Qt.AlignCenter)

            iqama_center_widget = QWidget()
            iqama_center_layout = QHBoxLayout(iqama_center_widget)
            iqama_center_layout.addStretch(1)
            iqama_center_layout.addWidget(iqama_bold_label)
            iqama_center_layout.addStretch(1)

            iqama_layout.addWidget(iqama_center_widget)
            iqama_layout.addStretch(1)

            iqama_small_label = QLabel(prayer_data["iqama_today"])
            iqama_small_label.setStyleSheet(f"color: {time_color}; font-size: 12px; text-align: right;")
            iqama_small_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)

            iqama_layout.addWidget(iqama_small_label)

            # Add widgets to the grid
            self.table_layout.addWidget(name_label, row - 1, 0)
            self.table_layout.addWidget(start_widget, row - 1, 1)
            self.table_layout.addWidget(iqama_widget, row - 1, 2)

        # Rows 3, 8: Shurooq, Jum'ah (2 columns)
        row_indices = [3, 8]
        prayer_indices = [1, 6]  # Shurooq, Jum'ah
        for row, prayer_idx in zip(row_indices, prayer_indices):
            prayer_data = prayers[prayer_idx]
            is_next_prayer = (prayer_idx == next_prayer_index)
            time_color = '#FFD700' if is_next_prayer else '#32CD32'

            # First column: Prayer name (spans 1 column)
            name_label = QLabel(prayer_data["name"])
            name_label.setStyleSheet("color: white; font-size: 55px; background-color: #4682B4; padding: 5px;")

            # Second column: Start (bold Tomorrow center, small Today bottom-right, spans 2 columns)
            start_widget = QWidget()
            start_widget.setStyleSheet("background-color: #32CD32;")
            start_layout = QVBoxLayout(start_widget)
            start_layout.setContentsMargins(5, 5, 5, 5)
            start_layout.setSpacing(0)

            start_layout.addStretch(1)
            start_bold_label = QLabel(prayer_data["start_tomorrow"] if prayer_data["start_tomorrow"] else prayer_data["iqama_tomorrow"])
            start_bold_label.setStyleSheet("color: white; font-size: 55px; font-weight: bold; text-align: center;")
            start_bold_label.setAlignment(Qt.AlignCenter)

            start_center_widget = QWidget()
            start_center_layout = QHBoxLayout(start_center_widget)
            start_center_layout.addStretch(1)
            start_center_layout.addWidget(start_bold_label)
            start_center_layout.addStretch(1)

            start_layout.addWidget(start_center_widget)
            start_layout.addStretch(1)

            start_small_label = QLabel(prayer_data["start_today"] if prayer_data["start_today"] else prayer_data["iqama_today"])
            start_small_label.setStyleSheet(f"color: {time_color}; font-size: 12px; text-align: right;")
            start_small_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)

            start_layout.addWidget(start_small_label)

            # Add widgets to the grid
            # Prayer name in Column 0, spans 1 column
            self.table_layout.addWidget(name_label, row - 1, 0, 1, 1)
            # Start time in Column 1, spans 2 columns (Columns 1 and 2)
            self.table_layout.addWidget(start_widget, row - 1, 1, 1, 2)

        # Set row heights
        self.table_layout.setRowMinimumHeight(0, 70)  # Header row (increased height)
        for row in [1, 3, 4, 5, 6]:  # Rows 2, 4, 5, 6, 7 (Fajr, Zuhr, Asr, Maghrib, Isha)
            self.table_layout.setRowMinimumHeight(row, 60)  # Increased for larger font
        self.table_layout.setRowMinimumHeight(2, 30)  # Row 3 (Shurooq)
        self.table_layout.setRowMinimumHeight(7, 30)  # Row 8 (Jum'ah)

        # Add panels to main layout
        self.main_layout.addWidget(self.left_panel, 1)  
        self.main_layout.addWidget(self.right_panel, 1)

    def update_clock(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.clock_label.setText(current_time)

    def get_prayer_data(self):
        return [
            {"name": "Fajr", "start_today": "6:32", "start_tomorrow": "6:34", "iqama_today": "6:52", "iqama_tomorrow": "6:54"},
            {"name": "Shurooq", "start_today": "7:49", "start_tomorrow": "7:51", "iqama_today": "", "iqama_tomorrow": ""},
            {"name": "Zuhr", "start_today": "1:42", "start_tomorrow": "1:44", "iqama_today": "1:58", "iqama_tomorrow": "2:00"},
            {"name": "Asr", "start_today": "5:48", "start_tomorrow": "5:50", "iqama_today": "6:13", "iqama_tomorrow": "6:15"},
            {"name": "Maghrib", "start_today": "7:36", "start_tomorrow": "7:38", "iqama_today": "7:51", "iqama_tomorrow": "7:53"},
            {"name": "Isha", "start_today": "8:52", "start_tomorrow": "8:54", "iqama_today": "9:07", "iqama_tomorrow": "9:09"},
            {"name": "Jum'ah", "start_today": "", "start_tomorrow": "", "iqama_today": "2:08", "iqama_tomorrow": "2:10"}
        ]

    def get_next_prayer(self, prayers):
        now = datetime.now()
        current_time = now.hour * 60 + now.minute
        for i, prayer in enumerate(prayers):
            if prayer["start_today"]:
                time_obj = datetime.strptime(prayer["start_today"], '%H:%M')
                prayer_minutes = time_obj.hour * 60 + time_obj.minute
                if prayer_minutes > current_time:
                    return i
        return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PrayerTimesApp()
    window.show()
    sys.exit(app.exec_())