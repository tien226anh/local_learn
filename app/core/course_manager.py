import os
from typing import List
from app.models.course import Course
from app.models.file_item import FileItem
from .state_manager import StateManager

class CourseManager:
    def __init__(self):
        self.state_manager = StateManager()

    def load_course(self, path: str) -> Course:
        """
        Scans the directory and returns a Course object.
        Initializes state file if not present.
        """
        items = self._scan_directory(path)
        course = Course(path, items)
        
        # Ensure state file exists or is readable
        self.state_manager.load_state(path)
        
        return course

    def _scan_directory(self, root_path: str) -> List[FileItem]:
        items = []
        if not os.path.exists(root_path):
            return items

        for root, dirs, files in os.walk(root_path):
            dirs.sort()
            files.sort()
            
            for f in files:
                full_path = os.path.join(root, f)
                # Skip state file
                if f == StateManager.STATE_FILE_NAME:
                    continue
                    
                item = FileItem(full_path)
                if item.file_type != item.file_type.UNKNOWN:
                    items.append(item)
        return items

    def get_last_played(self, course: Course):
        state = self.state_manager.load_state(course.root_path)
        return state.get('last_played_video'), state.get('timestamp', 0)

    def save_progress(self, course: Course, video_path: str, timestamp: int):
        self.state_manager.update_last_played(course.root_path, video_path, timestamp)
