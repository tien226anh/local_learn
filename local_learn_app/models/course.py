import os
from typing import List
from .file_item import FileItem

class Course:
    def __init__(self, root_path: str, items: List[FileItem] = None):
        self.root_path = root_path
        self.items: List[FileItem] = items or []

    def set_items(self, items: List[FileItem]):
        self.items = items
    
    def get_items(self) -> List[FileItem]:
        return self.items
    

