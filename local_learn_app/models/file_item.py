import os
from enum import Enum

class FileType(Enum):
    VIDEO = "video"
    IMAGE = "image"
    TEXT = "text"
    UNKNOWN = "unknown"

class FileItem:
    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(path)
        self.file_type = self._determine_type()

    def _determine_type(self) -> FileType:
        ext = os.path.splitext(self.path)[1].lower()
        if ext in ['.mp4', '.mkv', '.avi', '.mov', '.webm']:
            return FileType.VIDEO
        elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            return FileType.IMAGE
        elif ext in ['.txt', '.md', '.py', '.json', '.html', '.css', '.js']:
            return FileType.TEXT
        return FileType.UNKNOWN

    def is_video(self) -> bool:
        return self.file_type == FileType.VIDEO

    def is_image(self) -> bool:
        return self.file_type == FileType.IMAGE

    def is_text(self) -> bool:
        return self.file_type == FileType.TEXT
