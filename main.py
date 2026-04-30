import sys
import os
from PyQt5.QtWidgets import QApplication
from src.gui import AircraftControlApp

def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    
    # Create and show the main application window
    window = AircraftControlApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()