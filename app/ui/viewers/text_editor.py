from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox
from .base_viewer import BaseViewer

class TextEditor(BaseViewer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_path = None
        
        self.layout = QVBoxLayout(self)
        
        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)
        
        self.btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_file)
        self.btn_layout.addWidget(self.save_btn)
        self.btn_layout.addStretch()
        
        self.layout.addLayout(self.btn_layout)

    def load_file(self, path: str):
        self.current_path = path
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.text_edit.setPlainText(content)
        except Exception as e:
            self.text_edit.setPlainText(f"Error loading file: {e}")

    def save_file(self):
        if not self.current_path:
            return
            
        try:
            content = self.text_edit.toPlainText()
            with open(self.current_path, 'w', encoding='utf-8') as f:
                f.write(content)
            QMessageBox.information(self, "Success", "File saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {e}")

    def cleanup(self):
        self.text_edit.clear()
        self.current_path = None
