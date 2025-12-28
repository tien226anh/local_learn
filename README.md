# Local Learn

**Local Learn** is a Python-based desktop application designed to help you organize and learn from local video courses. It provides a structured interface to browse course content, play videos with advanced state tracking, and view/edit accompanying materials.

## Features

- **Course Organization**:
  - **Tree View Sidebar**: Navigate complex folder structures to find your content.
  - **Resume Capability**: Automatically remembers the last video played and the exact timestamp.
  - **Format Support**: Handles Videos (`.mp4`, `.mkv`, etc.), Images (`.jpg`, `.png`), and Text (`.txt`, `.md`, `.py`).

- **Video Player**:
  - **State Persistence**: Saves progress on pause, app exit, or video switch.
  - **Controls**: Play/Pause button, Seek Slider.
  - **Click-to-Interact**: Click video area to toggle Play/Pause; Click slider track to jump to position.

- **Content Viewers**:
  - **Image Viewer**: Scrollable view for diagrams and slides.
  - **Text Editor**: Read and edit notes or code files directly within the app.

## Installation

### Prerequisites
- Python 3.12+
- Poetry (Dependency Manager)

### Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   poetry install
   ```

## Usage

### Running from Source
```bash
poetry run python main.py
```

### Building Standalone Executable
To build a single-file executable for your OS (Linux/Windows):
```bash
poetry run pyinstaller main.py --name=local_learn --onefile --windowed --clean --noconfirm
```
The executable will be available in the `dist/` directory.

## Development

### Directory Structure
```
local_learn/
├── app/
│   ├── core/          # Business logic (State, Course management)
│   ├── models/        # Data models
│   └── ui/            # PyQt6 Widgets and Windows
│       └── viewers/   # Specific file viewers (Video, Image, Text)
├── tests/             # Unit tests
├── main.py            # Entry point
└── pyproject.toml     # Dependencies
```

### Running Tests
```bash
poetry run python -m unittest discover tests
```
