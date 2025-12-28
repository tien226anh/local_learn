from PyQt6.QtWidgets import QStackedWidget, QLabel, QWidget, QVBoxLayout
from app.models.file_item import FileItem
from .viewers.video_player import VideoPlayer
from .viewers.image_viewer import ImageViewer
from .viewers.text_editor import TextEditor

class ContentArea(QWidget):
    def __init__(self, course_manager, parent=None):
        super().__init__(parent)
        self.course_manager = course_manager
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        # 0: Empty/Welcome
        self.welcome_label = QLabel("Select a file to view")
        self.welcome_label.setStyleSheet("font-size: 18px; color: #666;")
        self.stack.addWidget(self.welcome_label)
        
        # 1: Video Player
        self.video_player = VideoPlayer()
        self.stack.addWidget(self.video_player)
        
        # 2: Image Viewer
        self.image_viewer = ImageViewer()
        self.stack.addWidget(self.image_viewer)
        
        # 3: Text Editor
        self.text_editor = TextEditor()
        self.stack.addWidget(self.text_editor)
        
        self.current_viewer = None
        self.current_file = None

    def show_content(self, file_item: FileItem):
        # Cleanup previous
        if self.current_viewer:
            self.current_viewer.cleanup()
            
        self.current_file = file_item
        
        if file_item.is_video():
            self.current_viewer = self.video_player
            self.stack.setCurrentWidget(self.video_player)
            self.video_player.load_file(file_item.path)
            
            # Check for saved progress
            # Ideally MainWindow coordinates this, but ContentArea has access to course_manager via init?
            # Or passed in load_content?
            # Let's let MainWindow handle logic or expose signal.
            # But here we have access to logic if we pass course_manager.
            
        elif file_item.is_image():
            self.current_viewer = self.image_viewer
            self.stack.setCurrentWidget(self.image_viewer)
            self.image_viewer.load_file(file_item.path)
            
        elif file_item.is_text():
            self.current_viewer = self.text_editor
            self.stack.setCurrentWidget(self.text_editor)
            self.text_editor.load_file(file_item.path)
            
        else:
            self.current_viewer = None
            self.stack.setCurrentIndex(0)

    def get_video_player(self):
        return self.video_player
