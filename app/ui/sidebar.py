from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QLabel, QHeaderView
from PyQt6.QtCore import pyqtSignal, QDir
from PyQt6.QtGui import QFileSystemModel
from app.models.course import Course
from app.models.file_item import FileItem
import os

class Sidebar(QWidget):
    item_selected = pyqtSignal(FileItem)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.header = QLabel("Course Content")
        self.header.setStyleSheet("padding: 10px; font-weight: bold; background-color: #eee;")
        self.layout.addWidget(self.header)

        self.model = QFileSystemModel()
        self.model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)
        self.model.setNameFilters(FileItem.get_supported_extensions())
        self.model.setNameFilterDisables(False) # Hide files that don't match

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setHeaderHidden(True)
        # Hide Size, Type, Date columns, keep Name
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)
        
        self.tree_view.clicked.connect(self._on_item_clicked)
        self.layout.addWidget(self.tree_view)

    def load_course(self, course: Course):
        root_path = course.root_path
        self.model.setRootPath(root_path)
        self.tree_view.setRootIndex(self.model.index(root_path))

    def _on_item_clicked(self, index):
        path = self.model.filePath(index)
        if not self.model.isDir(index):
            file_item = FileItem(path)
            self.item_selected.emit(file_item)
    
    def select_item_by_path(self, path: str):
        index = self.model.index(path)
        if index.isValid():
            self.tree_view.setCurrentIndex(index)
            self.tree_view.scrollTo(index)
