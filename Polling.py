import math
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

start = 0
end = 500
top = 0
bottom = 300


class PollingWidget(QWidget):
    vote_list = [0,20,40,50,200]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Polling")
        self.setGeometry(start, top, end, bottom)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        def generate_rainbow_rgb(num_colors):
            colors = []
            for i in range(num_colors):
                # Map progress to [0, 1] range (i / num_colors)
                t = i / num_colors

                # Adjust red, green, and blue channels with sine and cosine for smooth transitions
                r = int(255 * (0.5 * (math.sin(2 * math.pi * t + 0) + 1)))  # Red
                g = int(255 * (0.5 * (math.sin(2 * math.pi * t + 2 * math.pi / 3) + 1)))  # Green
                b = int(255 * (0.5 * (math.sin(2 * math.pi * t + 4 * math.pi / 3) + 1)))  # Blue

                # Append the RGB tuple to the list
                colors.append((r, g, b))
            return colors

        i = 0
        colors = generate_rainbow_rgb(len(self.vote_list))
        for vote in self.vote_list:
            painter.setBrush(QColor(colors[i][0], colors[i][1], colors[i][2]))
            index_adjust = int((bottom-50)/len(self.vote_list))
            v_adjust = index_adjust*i
            bar_size = index_adjust - int(index_adjust/2)
            if vote < 500:
                painter.drawRect(0, bar_size + v_adjust, vote, bar_size)
            else:
                painter.drawRect(0,bar_size + v_adjust , 500, bar_size)
            i += 1

    def set_value(self):
        for i in range(0, len(self.vote_list)):
            self.vote_list[i] += 5
        self.repaint()


app = QApplication(sys.argv)
window = PollingWidget()
timer = QTimer()

def start_timer():
    global window
    timer.timeout.connect(lambda: window.set_value())
    timer.start(100)

def start_poll_ui():
    global app
    window.show()
    start_timer()
    sys.exit(app.exec())


if __name__ == "__main__":
    start_poll_ui()


