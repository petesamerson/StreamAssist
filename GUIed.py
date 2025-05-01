import sys
from io import BytesIO
from pydoc_data.topics import topics

import requests
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QMessageBox, \
    QGraphicsColorizeEffect, QSizePolicy, QTextEdit

import GlobalVariables
import test
from test import curMessage

start = 300
top = 300
bottom = 300
end = 300

def launch_gui():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Stream Assist Alp-ha")
    window.setGeometry(start, top, bottom, end)
    with open("guied_format.css", "r") as file:
        window.setStyleSheet(file.read())

    layout = QVBoxLayout()
    image_label = QLabel(window)
    pixmap = QPixmap("thumbnail_pikminsux.jpg")
    # scaledPixmap = pixmap.scaled(start, top, bottom, end)
    scaledPixmap = pixmap.scaled(window.width(), window.height(), Qt.KeepAspectRatio)  # Keep aspect ratio

    tint = QGraphicsColorizeEffect()
    tint.setColor(QColor(255, 255, 255))
    tint.setStrength(0.2)
    image_label.setPixmap(scaledPixmap)
    image_label.setAlignment(Qt.AlignCenter)
    image_label.setGeometry(0,0,window.width(), window.height())
    # imageLabel.setGraphicsEffect(tint)
    # layout.addWidget(imageLabel)

    text_label = QTextEdit("I CAN STILL TEXT", window)
    text_label.setAlignment(Qt.AlignCenter)
    text_label.setGeometry(0,0,window.width(), window.height())
    text_label.setStyleSheet("background-color: transparent")
    text_label.raise_()
    # text_label.setWordWrap(True)
    text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)



    # layout.addWidget(text_label, 0, Qt.AlignCenter)
    # text_label.move(0, -150)

    button = QPushButton("Challenge",window)
    def on_click():
        QMessageBox.information(window, "Message", "Die Facist!")
    button.clicked.connect(on_click)
    button.move(int(text_label.x()), (int(text_label.height()) + int(button.height())))
    # layout.addWidget(button)

    # window.setLayout(layout)
    window.show()

    def update_text():
        text_label.setHtml(f'''
            <div style = "text-align: center;">
                <span style="background-color: black"> {test.curMessage}</span>
            </div>
        ''')
        text_label.setAlignment(Qt.AlignCenter)

    def update_cover():
        if(GlobalVariables.album_art != ""):
            response = requests.get(GlobalVariables.album_art)
            image_data = BytesIO(response.content)
            pixmap.loadFromData(image_data.read())
            scaledPixmap = pixmap.scaled(window.width(), window.height(), Qt.KeepAspectRatio)  # Keep aspect ratio
            image_label.setPixmap(scaledPixmap)
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setGeometry(0,0,window.width(), window.height())

    def update_spotify_gui():
        update_text()
        update_cover()

    timer = QTimer()
    timer.timeout.connect(update_spotify_gui)
    timer.start(1000)

    sys.exit(app.exec_())

if __name__ == "__main__":
    launch_gui()
