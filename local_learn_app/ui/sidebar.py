from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from local_learn_app.models.course import Course
from local_learn_app.models.file_item import FileItem

class Sidebar(QWidget):
    item_selected = pyqtSignal(FileItem)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.header = QLabel("Course Content")
        self.header.setStyleSheet("padding: 10px; font-weight: bold; background-color: #eee;")
        self.layout.addWidget(self.header)

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        self.layout.addWidget(self.list_widget)
        
        self._course_items = {} # map item id (row) to FileItem? or store in data

    def load_course(self, course: Course):
        self.list_widget.clear()
        self._course_items = {}
        
        for item in course.get_items():
            list_item = QListWidgetItem(item.name)
            # Store FileItem in UserRole data
            list_item.setData(Qt.ItemDataRole.UserRole, item)
            self.list_widget.addItem(list_item)

    def _on_item_clicked(self, item: QListWidgetItem):
        file_item = item.data(Qt.ItemDataRole.UserRole)
        if file_item:
            self.item_selected.emit(file_item)
    
    def select_item_by_path(self, path: str):
        # iterate and select
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            file_item = item.data(Qt.ItemDataRole.UserRole)
            if file_item and file_item.path == path:
                self.list_widget.setCurrentItem(item)
                return
