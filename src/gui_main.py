import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QFormLayout
from PyQt5.QtCore import Qt

class Yak130ControlSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Yak-130 Control System')
        self.setGeometry(100, 100, 800, 600)

        # Create the central widget and set it as the main widget
        self.central_widget = QTabWidget(self)
        self.setCentralWidget(self.central_widget)

        self.init_connection_panel()
        self.init_characteristics_panel()
        self.init_control_panel()
        self.init_telemetry_display()

    def init_connection_panel(self):
        connection_panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Connection Panel'))
        # Add connection logic here
        self.connect_btn = QPushButton('Connect')
        layout.addWidget(self.connect_btn)
        connection_panel.setLayout(layout)
        self.central_widget.addTab(connection_panel, 'Connection')

    def init_characteristics_panel(self):
        characteristics_panel = QWidget()
        layout = QFormLayout()
        layout.addWidget(QLabel('Aircraft Characteristics Panel'))
        # Add characteristics inputs here
        self.characteristic_input = QLabel('Specifications go here')
        layout.addWidget(self.characteristic_input)
        characteristics_panel.setLayout(layout)
        self.central_widget.addTab(characteristics_panel, 'Characteristics')

    def init_control_panel(self):
        control_panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Control Panel'))
        self.slider = QSlider(Qt.Horizontal)
        layout.addWidget(self.slider)
        self.slider.setRange(0, 100)
        layout.addWidget(QLabel('Control Sliders'))
        control_panel.setLayout(layout)
        self.central_widget.addTab(control_panel, 'Control')

    def init_telemetry_display(self):
        telemetry_panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Telemetry Display'))
        self.telemetry_info = QLabel('Telemetry data will be shown here')
        layout.addWidget(self.telemetry_info)
        telemetry_panel.setLayout(layout)
        self.central_widget.addTab(telemetry_panel, 'Telemetry')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Yak130ControlSystem()
    window.show()
    sys.exit(app.exec_())