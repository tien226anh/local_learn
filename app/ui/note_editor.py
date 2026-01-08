"""Markdown note editor panel for taking notes."""
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QShortcut, QKeySequence


class NoteEditor(QWidget):
    """A markdown editor widget for taking notes with manual save (Ctrl+S)."""
    
    content_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._notes_file_path = None
        self._init_ui()
        self._setup_shortcuts()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setObjectName("noteEditorHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 8, 12, 8)
        
        title = QLabel("📝 Notes")
        title.setObjectName("noteEditorTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Clear button
        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("noteClearBtn")
        clear_btn.clicked.connect(self.clear_notes)
        header_layout.addWidget(clear_btn)
        
        layout.addWidget(header)
        
        # Text editor
        self.editor = QTextEdit()
        self.editor.setObjectName("noteTextEdit")
        self.editor.setPlaceholderText("Write your notes here...\n\nSupports Markdown formatting.\nPress Ctrl+S to save.")
        self.editor.setAcceptRichText(False)
        
        # Set a nice monospace font for markdown editing
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.editor.setFont(font)
        
        self.editor.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.editor)
    
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts for the note editor."""
        # Ctrl+S to save when editor is focused
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self.editor)
        self.save_shortcut.activated.connect(self.save_notes)
    
    def _on_text_changed(self):
        self.content_changed.emit(self.editor.toPlainText())
    
    def set_course_path(self, course_path: str):
        """Set the course directory path and load existing notes."""
        if course_path:
            self._notes_file_path = os.path.join(course_path, ".notes.md")
            self._load_notes()
        else:
            self._notes_file_path = None
            self.editor.clear()
    
    def _load_notes(self):
        """Load notes from the course directory."""
        if self._notes_file_path and os.path.exists(self._notes_file_path):
            try:
                with open(self._notes_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor.blockSignals(True)
                self.editor.setPlainText(content)
                self.editor.blockSignals(False)
            except Exception as e:
                print(f"Failed to load notes: {e}")
    
    def save_notes(self):
        """Save notes to the course directory (Ctrl+S)."""
        if self._notes_file_path:
            try:
                content = self.editor.toPlainText()
                with open(self._notes_file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            except Exception as e:
                print(f"Failed to save notes: {e}")
    
    def clear_notes(self):
        self.editor.clear()
    
    def get_content(self) -> str:
        return self.editor.toPlainText()
    
    def set_content(self, content: str):
        self.editor.setPlainText(content)
