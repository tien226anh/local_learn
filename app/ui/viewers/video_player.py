from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QStyle
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, pyqtSignal, Qt
from .base_viewer import BaseViewer

class ClickableVideoWidget(QVideoWidget):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class ClickableSlider(QSlider):
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            val = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width())
            self.setValue(val)
            self.sliderMoved.emit(val)
        super().mousePressEvent(event)

class VideoPlayer(BaseViewer):
    # Signal to emit progress or pause state if needed
    position_changed = pyqtSignal(int)
    state_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.video_widget = ClickableVideoWidget()
        self.video_widget.clicked.connect(self.toggle_playback)
        self.layout.addWidget(self.video_widget)
        
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)
        
        # Connect signals
        self.media_player.positionChanged.connect(self._on_position_changed)
        self.media_player.playbackStateChanged.connect(self._on_state_changed)
        self.media_player.durationChanged.connect(self._on_duration_changed)

        # Controls Layout
        self.controls_layout = QHBoxLayout()
        self.layout.addLayout(self.controls_layout)

        # Play/Pause Button
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.clicked.connect(self.toggle_playback)
        self.controls_layout.addWidget(self.play_button)

        # Slider
        self.slider = ClickableSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)
        # Using sliderPressed/Released could be better for smoother seeking, but sliderMoved is usually okay
        self.controls_layout.addWidget(self.slider)

    def toggle_playback(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def _on_position_changed(self, pos):
        # Update slider only if not being dragged might be needed, 
        # but for now let's just update. 
        # If user holds handle, this might fight. 
        # Ideally check self.slider.isSliderDown()
        if not self.slider.isSliderDown():
            self.slider.setValue(pos)
        
        self.position_changed.emit(pos)

    def _on_state_changed(self, state):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            
        self.state_changed.emit(state.value if hasattr(state, 'value') else state)

    def _on_duration_changed(self, duration):
        self.slider.setRange(0, duration)

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
