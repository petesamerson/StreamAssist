import math
import sys

from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QColor, QFont, QPolygon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

width = 300
height = 300


class AnimationWidget(QWidget):
    rotation = float(10)
    color_index = 0

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mic Animation")
        self.setGeometry(0, 0, width, height)

    class Triangle:
        poly = None
        def __init__(self, center_x, center_y, size):
            divide_size = int(size/3)
            self.poly = QPolygon([
                QPoint(center_x + divide_size*2, center_y + divide_size),
                QPoint(center_x + divide_size,center_y + size),
                QPoint(center_x + size,center_x + size)
            ])

    triangles = []


    def paintEvent(self, event):
        global range
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

        colors = generate_rainbow_rgb(width)
        font = QFont("Arial", 16)
        painter.setFont(font)
        painter.translate(width/2, height/2)

        # for i in range(20,width):
        #     if i % 20 == 0:
        color = QColor(colors[self.color_index][0], colors[self.color_index][1], colors[self.color_index][2])
        painter.setBrush(color)
        painter.setPen(color)
        angle_radians = math.radians(self.rotation)
        self.triangles.append(self.Triangle(
            int(width/2 + math.sin(angle_radians)*100),
            int(height/2 + math.cos(angle_radians)*100),
            20
        ))
        print(
            [
                int(width/2 + math.sin(angle_radians)*100),
                int(height/2 + math.cos(angle_radians)*100),
                20,
                color.blue()
            ]
        )

        for tri in self.triangles:
            if tri is self.Triangle:
                painter.drawPolygon(tri.poly)


    def update_rotation_pos(self):
        self.rotation += 10
        if self.rotation > 360:
            self.rotation = 0

        self.color_index += 5
        if self.color_index > 200:
            self.color_index = 0
        self.repaint()





app = QApplication(sys.argv)
window = AnimationWidget()
timer = QTimer()

def start_timer():
    global window
    timer.timeout.connect(lambda: window.update_rotation_pos())
    timer.start(100)

def start_animation_ui():
    global app
    window.show()
    start_timer()
    sys.exit(app.exec())


if __name__ == "__main__":
    start_animation_ui()
