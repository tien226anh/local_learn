from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QStyle, QLabel, QWidget
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, pyqtSignal, Qt, QTime
from .base_viewer import BaseViewer

class ClickableVideoWidget(QVideoWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Allow this widget to receive focus
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setFocus()  # Take focus on click
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
    video_ended = pyqtSignal()  # Emitted when video finishes playing

    def __init__(self, parent=None):
        super().__init__(parent)
        # Make this widget focusable
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        
        self.video_widget = ClickableVideoWidget()
        self.video_widget.clicked.connect(self._on_video_clicked)
        self.layout.addWidget(self.video_widget)
        
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)
        
        # Connect signals
        self.media_player.positionChanged.connect(self._on_position_changed)
        self.media_player.playbackStateChanged.connect(self._on_state_changed)
        self.media_player.durationChanged.connect(self._on_duration_changed)
        self.media_player.mediaStatusChanged.connect(self._on_media_status_changed)

        # Controls Container
        self.controls_container = QWidget()
        self.controls_container.setFixedHeight(30) # Strictly limit height
        self.controls_container.setStyleSheet("background-color: #222;") # Remove internal padding from stylesheet
        self.layout.addWidget(self.controls_container)

        # Controls Layout
        self.controls_layout = QHBoxLayout(self.controls_container)
        self.controls_layout.setContentsMargins(5, 0, 5, 0) # Minimal padding
        self.controls_layout.setSpacing(8)

        # Play/Pause Button
        self.play_button = QPushButton()
        self.play_button.setFixedSize(24, 24) # Slightly larger for clickability, but remove style padding
        # Override global style to remove padding/borders/min-width
        self.play_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
                min-width: 0px;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: #333;
                border-radius: 12px;
            }
        """)
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.clicked.connect(self.toggle_playback)
        self.controls_layout.addWidget(self.play_button)

        # Current Time Label
        self.current_time_label = QLabel("00:00")
        self.current_time_label.setFixedWidth(40) # Compact label
        self.current_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.controls_layout.addWidget(self.current_time_label)

        # Slider
        self.slider = ClickableSlider(Qt.Orientation.Horizontal)
        self.slider.setFixedHeight(14) # Compact slider widget
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)
        self.controls_layout.addWidget(self.slider)

        # Total Time Label
        self.total_time_label = QLabel("00:00")
        self.total_time_label.setFixedWidth(40)
        self.total_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.controls_layout.addWidget(self.total_time_label)

        # Volume Button (speaker icon)
        self.volume_button = QPushButton()
        self.volume_button.setFixedSize(24, 24)
        self.volume_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
                min-width: 0px;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: #333;
                border-radius: 12px;
            }
        """)
        self.volume_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))
        self.volume_button.clicked.connect(self.toggle_mute)
        self.controls_layout.addWidget(self.volume_button)

        # Volume Slider
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setFixedWidth(80)
        self.volume_slider.setFixedHeight(14)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)  # Default full volume
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        self.controls_layout.addWidget(self.volume_slider)
        
        self._is_muted = False
        self._previous_volume = 100

    def _on_video_clicked(self):
        """Handle click on video area - set focus and toggle playback."""
        self.setFocus()  # Set focus on VideoPlayer so it receives key events
        self.toggle_playback()

    def toggle_playback(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def toggle_mute(self):
        """Toggle audio mute on/off."""
        if self._is_muted:
            self.volume_slider.setValue(self._previous_volume)
            self._is_muted = False
        else:
            self._previous_volume = self.volume_slider.value() if self.volume_slider.value() > 0 else 100
            self.volume_slider.setValue(0)
            self._is_muted = True

    def _on_volume_changed(self, value):
        """Handle volume slider changes."""
        # QAudioOutput volume is 0.0 to 1.0
        self.audio_output.setVolume(value / 100.0)
        
        # Update icon based on volume level
        if value == 0:
            self.volume_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolumeMuted))
        else:
            self.volume_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))

    def _format_time(self, ms: int) -> str:
        seconds = (ms // 1000) % 60
        minutes = (ms // 60000) % 60
        hours = (ms // 3600000)
        
        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return f"{minutes:02}:{seconds:02}"

    def _on_position_changed(self, pos):
        if not self.slider.isSliderDown():
            self.slider.setValue(pos)
        
        self.current_time_label.setText(self._format_time(pos))
        self.position_changed.emit(pos)

    def _on_state_changed(self, state):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            
        self.state_changed.emit(state.value if hasattr(state, 'value') else state)

    def _on_duration_changed(self, duration):
        self.slider.setRange(0, duration)
        self.total_time_label.setText(self._format_time(duration))

    def _on_media_status_changed(self, status):
        """Handle media status changes to detect end of video."""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.video_ended.emit()

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

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts for video control."""
        key = event.key()
        
        # Volume control: Up/Down arrows (+/- 5%)
        if key == Qt.Key.Key_Up:
            new_vol = min(100, self.volume_slider.value() + 5)
            self.volume_slider.setValue(new_vol)
            event.accept()
        elif key == Qt.Key.Key_Down:
            new_vol = max(0, self.volume_slider.value() - 5)
            self.volume_slider.setValue(new_vol)
            event.accept()
        
        # Seeking: Left/Right arrows (+/- 5 seconds)
        elif key == Qt.Key.Key_Left:
            new_pos = max(0, self.media_player.position() - 5000)
            self.media_player.setPosition(new_pos)
            event.accept()
        elif key == Qt.Key.Key_Right:
            new_pos = min(self.media_player.duration(), self.media_player.position() + 5000)
            self.media_player.setPosition(new_pos)
            event.accept()
        
        # Space for play/pause
        elif key == Qt.Key.Key_Space:
            self.toggle_playback()
            event.accept()
        
        else:
            super().keyPressEvent(event)
