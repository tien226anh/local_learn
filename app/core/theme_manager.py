"""
Theme Manager for Local Learn application.
Handles theme preference loading, saving, and application.
"""
import json
import os
from typing import Optional
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal

from app.ui.styles import THEMES


class ThemeManager(QObject):
    """Manages application themes and user preferences."""
    
    theme_changed = pyqtSignal(str)  # Emits theme name when changed
    
    CONFIG_DIR = os.path.expanduser("~/.local_learn")
    CONFIG_FILE = "config.json"
    DEFAULT_THEME = "dark"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_theme = self.DEFAULT_THEME
        self._ensure_config_dir()
        self._load_preference()
    
    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist."""
        if not os.path.exists(self.CONFIG_DIR):
            try:
                os.makedirs(self.CONFIG_DIR)
            except OSError:
                pass  # Ignore if can't create
    
    def _get_config_path(self) -> str:
        """Get full path to config file."""
        return os.path.join(self.CONFIG_DIR, self.CONFIG_FILE)
    
    def _load_preference(self):
        """Load theme preference from config file."""
        config_path = self._get_config_path()
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    theme = config.get('theme', self.DEFAULT_THEME)
                    if theme in THEMES:
                        self._current_theme = theme
            except (json.JSONDecodeError, IOError):
                pass  # Use default on error
    
    def _save_preference(self):
        """Save current theme preference to config file."""
        config_path = self._get_config_path()
        try:
            # Load existing config to preserve other settings
            config = {}
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                except (json.JSONDecodeError, IOError):
                    pass
            
            config['theme'] = self._current_theme
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except IOError as e:
            print(f"Error saving theme preference: {e}")
    
    def get_current_theme(self) -> str:
        """Get the current theme name."""
        return self._current_theme
    
    def get_current_stylesheet(self) -> str:
        """Get the stylesheet for the current theme."""
        return THEMES.get(self._current_theme, THEMES[self.DEFAULT_THEME])
    
    def set_theme(self, theme: str):
        """
        Set the application theme.
        
        Args:
            theme: Theme name ('dark' or 'light')
        """
        if theme not in THEMES:
            return
        
        if theme == self._current_theme:
            return
        
        self._current_theme = theme
        self._save_preference()
        
        # Apply to application
        app = QApplication.instance()
        if app:
            app.setStyleSheet(THEMES[theme])
        
        self.theme_changed.emit(theme)
    
    def get_available_themes(self) -> list:
        """Get list of available theme names."""
        return list(THEMES.keys())
