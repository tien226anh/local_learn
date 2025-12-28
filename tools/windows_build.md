# Building for Windows

To create a Windows executable (`.exe`) or installer (`.msi`) for Local Learn, you must perform the build process on a Windows environment. Cross-compiling from Linux is complex and generally not recommended for GUI applications relying on PyInstaller.

## Prerequisites (On Windows)
1.  **Python 3.12+**: Install from [python.org](https://www.python.org/).
2.  **Poetry**: Install Poetry using Powershell.
    ```powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    ```
3.  **Git**: Clone the repository.

## Steps

1.  **Install Dependencies**:
    ```powershell
    poetry install
    ```

2.  **Generate Executable**:
    Run the same PyInstaller command used on Linux. The config is cross-platform compatible.
    ```powershell
    poetry run pyinstaller main.py --name=local_learn --onefile --windowed --clean --noconfirm
    ```
    This will generate `dist\local_learn.exe`.

3.  **Create Installer (.msi)**:
    Since `pyinstaller` only creates an `.exe`, you can use a tool like **Inno Setup** or **WiX Toolset** to wrap it into an installer.

    **Using Inno Setup (Recommended for ease of use):**
    - Download and install [Inno Setup](https://jrsoftware.org/isinfo.php).
    - Create a new script using the Wizard.
    - Application Name: Local Learn
    - Application Exe: Browse to `dist\local_learn.exe`.
    - Compile the script to get `setup_local_learn.exe` (which acts like an installer).

    **Using WiX (Advanced):**
    - Create a `.wxs` file defining your components.
    - Run `candle` and `light` commands to generate `.msi`.
