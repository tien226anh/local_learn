from PyQt6.QtWidgets import QLabel, QVBoxLayout, QScrollArea
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from .base_viewer import BaseViewer

class ImageViewer(BaseViewer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.scroll_area = QScrollArea()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setWidgetResizable(True)
        
        self.layout.addWidget(self.scroll_area)

    def load_file(self, path: str):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            self.label.setPixmap(pixmap)
        else:
            self.label.setText("Failed to load image")

    def cleanup(self):
        self.label.clear()
