import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextBrowser

class PrayerTimesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prayer Times")
        self.setGeometry(100, 100, 1024, 600)

        # Set up the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a QTextBrowser to display HTML
        self.browser = QTextBrowser()
        self.layout.addWidget(self.browser)

        # Load prayer times and update HTML
        self.load_prayer_times()

    def load_prayer_times(self):
        # Define prayer times
        prayer_times = [
            {'name': 'Fajr', 'time': '5:41 AM'},
            {'name': 'Dhuhr', 'time': '12:44 PM'},
            {'name': 'Asr', 'time': '3:55 PM'},
            {'name': 'Maghrib', 'time': '6:59 PM'},
            {'name': 'Isha', 'time': '7:39 PM'},
        ]

        # Render HTML
        html_content = self.generate_html(prayer_times)
        self.browser.setHtml(html_content)

    def generate_html(self, prayer_times):
        prayer_entries = ""
        for prayer in prayer_times:
            prayer_entries += f"""
            <div class="prayer-entry">
                <div class="prayer-name">{prayer['name']}</div>
                <div class="prayer-time">{prayer['time']}</div>
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Prayer Times</title>
            <style>
                /* Tailwind-like CSS */
                body {{
                    background-color: #1A1A1A; /* bg-secondary */
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    margin: 0;
                    font-family: Arial, sans-serif;
                }}
                .container {{
                    width: 1024px; /* w-[1024px] */
                    text-align: center;
                }}
                .date {{
                    font-size: 3rem; /* Increased font size */
                    font-weight: bold;
                    margin-bottom: 1rem; /* mb-4 */
                }}
                .hijri-date {{
                    font-size: 2.25rem; /* Increased font size */
                    color: #A0A0A0; /* text-gray-300 */
                }}
                .divider {{
                    width: 8rem; /* w-32 */
                    height: 0.25rem; /* h-1 */
                    background-color: #4CAF50; /* bg-primary */
                    margin: 1.5rem auto; /* mx-auto mt-6 */
                    border-radius: 9999px; /* rounded-full */
                }}
                .prayer-list {{
                    display: flex;
                    flex-direction: column;
                    gap: 2rem; /* space-y-8 */
                }}
                .prayer-entry {{
                    background-color: rgba(128, 128, 128, 0.3); /* bg-gray-800/30 */
                    border-radius: 0.5rem; /* rounded-lg */
                    padding: 1.5rem; /* p-6 */
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                }}
                .prayer-name {{
                    font-size: 2.5rem; /* Increased font size */
                    font-weight: bold;
                }}
                .prayer-time {{
                    font-size: 2.5rem; /* Increased font size */
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="date">12th March 2024</div>
                <div class="hijri-date">12 Ramadhan 1446 AH</div>
                <div class="divider"></div>
                <div class="prayer-list">
                    {prayer_entries}
                </div>
            </div>
        </body>
        </html>
        """
        return html

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PrayerTimesApp()
    window.show()
    sys.exit(app.exec_())