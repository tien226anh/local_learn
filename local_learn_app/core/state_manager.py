import json
import os
from typing import Dict, Any

class StateManager:
    STATE_FILE_NAME = ".course_state.json"

    @staticmethod
    def get_state_file_path(course_path: str) -> str:
        return os.path.join(course_path, StateManager.STATE_FILE_NAME)

    def load_state(self, course_path: str) -> Dict[str, Any]:
        """
        Loads the course state from the JSON file.
        Returns an empty dict if file doesn't exist or is invalid.
        """
        state_path = self.get_state_file_path(course_path)
        if not os.path.exists(state_path):
            return {}
        
        try:
            with open(state_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def save_state(self, course_path: str, data: Dict[str, Any]):
        """
        Saves the course state to the JSON file.
        Merging with existing data is not handled here, it overwrites with 'data'.
        Higher level logic should handle merging if needed.
        """
        state_path = self.get_state_file_path(course_path)
        try:
            with open(state_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving state: {e}")

    def update_last_played(self, course_path: str, video_path: str, timestamp: int):
        """
        Helper to update just the last played info.
        """
        state = self.load_state(course_path)
        state['last_played_video'] = video_path
        state['timestamp'] = timestamp
        self.save_state(course_path, state)
