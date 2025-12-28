from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, pyqtSignal
from .base_viewer import BaseViewer

class VideoPlayer(BaseViewer):
    # Signal to emit progress or pause state if needed
    position_changed = pyqtSignal(int)
    state_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)
        
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)
        
        self.media_player.positionChanged.connect(self._on_position_changed)
        self.media_player.playbackStateChanged.connect(self._on_state_changed)

    def _on_position_changed(self, pos):
        self.position_changed.emit(pos)

    def _on_state_changed(self, state):
        self.state_changed.emit(state.value if hasattr(state, 'value') else state)

    def load_file(self, path: str):
        self.media_player.setSource(QUrl.fromLocalFile(path))
        self.media_player.play()

    def pause(self):
        self.media_player.pause()

    def get_position(self) -> int:
        return self.media_player.position()

    def set_position(self, position: int):
        self.media_player.setPosition(position)

    def cleanup(self):
        self.media_player.stop()
