import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("PyQt5 Test")
    window.setGeometry(100, 100, 300, 100)

    layout = QVBoxLayout()
    label = QLabel("Hello from PyQt5!")
    layout.addWidget(label)

    window.setLayout(layout)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()