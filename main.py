import sys
import os

# Ensure the package is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from app.ui.main_window import MainWindow
from app.core.theme_manager import ThemeManager

def main():
    app = QApplication(sys.argv)
    
    # Load saved theme preference
    theme_manager = ThemeManager()
    app.setStyleSheet(theme_manager.get_current_stylesheet())
    window = MainWindow()
    
    if "--no-focus" in sys.argv:
        window.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        window.show()
    else:
        window.show()
        
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
