from abc import ABCMeta, abstractmethod
from PyQt6.QtWidgets import QWidget

class QtABCMeta(type(QWidget), ABCMeta):
    pass

class BaseViewer(QWidget, metaclass=QtABCMeta):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    @abstractmethod
    def load_file(self, path: str):
        pass

    def cleanup(self):
        """Optional cleanup when switching away"""
        pass
