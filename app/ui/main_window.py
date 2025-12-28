import os
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QDockWidget, QMessageBox, QWidget, QVBoxLayout
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from app.core.course_manager import CourseManager
from app.ui.sidebar import Sidebar
from app.ui.content_area import ContentArea
from app.models.file_item import FileItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Learn")
        self.resize(1200, 800)
        
        self.course_manager = CourseManager()
        self.current_course = None
        
        self.setDockOptions(QMainWindow.DockOption.AnimatedDocks | QMainWindow.DockOption.AllowNestedDocks)
        
        self._init_ui()
        self._create_menu()

    def _init_ui(self):
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.item_selected.connect(self.on_item_selected)
        
        self.dock = QDockWidget("Course Content", self)
        self.dock.setWidget(self.sidebar)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        
        # Content Area
        self.content_area = ContentArea(course_manager=self.course_manager)
        self.setCentralWidget(self.content_area)
        
        # Connect video signals for state saving
        player = self.content_area.get_video_player()
        player.state_changed.connect(self.on_video_state_changed)

    def _create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        
        open_action = QAction("&Open Course Folder", self)
        open_action.triggered.connect(self.open_course)
        file_menu.addAction(open_action)
        
        view_menu = menu_bar.addMenu("&View")
        toggle_sidebar_action = self.dock.toggleViewAction()
        view_menu.addAction(toggle_sidebar_action)

    def open_course(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Course Directory")
        if folder:
            self._load_course_folder(folder)

    def _load_course_folder(self, folder: str):
        try:
            self.current_course = self.course_manager.load_course(folder)
            self.sidebar.load_course(self.current_course)
            self.setWindowTitle(f"Local Learn - {os.path.basename(folder)}")
            
            # Check last played
            last_video, timestamp = self.course_manager.get_last_played(self.current_course)
            if last_video and os.path.exists(last_video):
                reply = QMessageBox.question(self, "Resume Learning", 
                                             f"Do you want to continue from {os.path.basename(last_video)}?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if reply == QMessageBox.StandardButton.Yes:
                    # Find item and select it
                    self.sidebar.select_item_by_path(last_video)
                    # Trigger loading manually as select_item_by_path might just highlight UI
                    # But sidebar signal won't emit if set programmatically usually, depends on implementation.
                    # QListWidget.setCurrentItem doesn't emit itemClicked.
                    # So we call logic manually.
                    item = FileItem(last_video)
                    self.on_item_selected(item, start_pos=timestamp)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load course: {e}")

    def on_item_selected(self, file_item: FileItem, start_pos=0):
        self.content_area.show_content(file_item)
        if file_item.is_video() and start_pos > 0:
            self.content_area.get_video_player().set_position(start_pos)

    def on_video_state_changed(self, state: int):
        # QMediaPlayer.PlaybackState.PausedState is what we look for.
        # Enums are: StoppedState(0), PlayingState(1), PausedState(2)
        if state == 2: # Paused
             if self.current_course and self.content_area.current_file and self.content_area.current_file.is_video():
                pos = self.content_area.get_video_player().get_position()
                self.course_manager.save_progress(self.current_course, self.content_area.current_file.path, pos)

    def closeEvent(self, event):
        # Save current state if video is playing
        if self.current_course and self.content_area.current_file and self.content_area.current_file.is_video():
            pos = self.content_area.get_video_player().get_position()
            self.course_manager.save_progress(self.current_course, self.content_area.current_file.path, pos)
        event.accept()
