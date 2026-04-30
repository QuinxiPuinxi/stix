import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel('Control Panel')
        button = QPushButton('Start')
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)

class CharacteristicsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel('Characteristics Panel')
        button = QPushButton('Show Characteristics')
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)

class ConnectionPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel('Connection Panel')
        button = QPushButton('Connect')
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_widget = QWidget()
    main_layout = QHBoxLayout()
    main_layout.addWidget(ControlPanel())
    main_layout.addWidget(CharacteristicsPanel())
    main_layout.addWidget(ConnectionPanel())
    main_widget.setLayout(main_layout)
    main_widget.setWindowTitle('Flight Surface Controllers GUI')
    main_widget.show()
    sys.exit(app.exec_())