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
        self.header.setObjectName("sidebarHeader")  # For theme styling
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

    def select_next_item(self) -> bool:
        """
        Select the next video file in the tree view.
        Returns True if a next item was found and selected, False otherwise.
        """
        current_index = self.tree_view.currentIndex()
        if not current_index.isValid():
            return False
        
        # Get the next sibling or traverse to find next file
        next_index = self._find_next_file(current_index)
        
        if next_index and next_index.isValid():
            self.tree_view.setCurrentIndex(next_index)
            self.tree_view.scrollTo(next_index)
            # Emit the selection signal
            path = self.model.filePath(next_index)
            if not self.model.isDir(next_index):
                file_item = FileItem(path)
                self.item_selected.emit(file_item)
                return True
        return False

    def _find_next_file(self, current_index):
        """Find the next file after current_index in tree traversal order."""
        # Try next sibling first
        next_index = current_index.siblingAtRow(current_index.row() + 1)
        
        while True:
            if next_index.isValid():
                # If it's a directory, go into it
                if self.model.isDir(next_index):
                    # Get first child
                    child = self.model.index(0, 0, next_index)
                    if child.isValid():
                        if not self.model.isDir(child):
                            return child
                        next_index = child
                        continue
                    # Empty directory, try next sibling
                    next_index = next_index.siblingAtRow(next_index.row() + 1)
                else:
                    # It's a file
                    return next_index
            else:
                # No more siblings, go to parent's next sibling
                parent = current_index.parent()
                if not parent.isValid() or parent == self.tree_view.rootIndex():
                    return None  # Reached the end
                current_index = parent
                next_index = parent.siblingAtRow(parent.row() + 1)
