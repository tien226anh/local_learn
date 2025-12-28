import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            print("Stopping current process...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
        
        print("Starting application...")
        self.process = subprocess.Popen(self.command)

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Change detected in {event.src_path}. Restarting...")
            self.start_process()

if __name__ == "__main__":
    # Command to run the application
    command = ["poetry", "run", "python", "main.py", "--no-focus"]
    
    event_handler = RestartHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()
    
    print("Watching for file changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.terminate()
    observer.join()
