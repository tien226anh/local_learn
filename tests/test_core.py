import unittest
import os
import shutil
import tempfile
import json
from local_learn_app.core.state_manager import StateManager
from local_learn_app.core.course_manager import CourseManager
from local_learn_app.models.file_item import FileType, FileItem

class TestCoreLogic(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.state_manager = StateManager()
        self.course_manager = CourseManager()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_file_item_type(self):
        f = FileItem("video.mp4")
        self.assertEqual(f.file_type, FileType.VIDEO)
        f = FileItem("image.jpg")
        self.assertEqual(f.file_type, FileType.IMAGE)
        f = FileItem("notes.txt")
        self.assertEqual(f.file_type, FileType.TEXT)
        f = FileItem("unknown.xyz")
        self.assertEqual(f.file_type, FileType.UNKNOWN)

    def test_state_manager(self):
        # Test load empty
        state = self.state_manager.load_state(self.test_dir)
        self.assertEqual(state, {})

        # Test save and load
        data = {'last_played_video': 'video1.mp4', 'timestamp': 100}
        self.state_manager.save_state(self.test_dir, data)
        
        loaded = self.state_manager.load_state(self.test_dir)
        self.assertEqual(loaded, data)

        # Test update
        self.state_manager.update_last_played(self.test_dir, 'video2.mp4', 200)
        loaded = self.state_manager.load_state(self.test_dir)
        self.assertEqual(loaded['last_played_video'], 'video2.mp4')
        self.assertEqual(loaded['timestamp'], 200)

    def test_course_manager_scan(self):
        # Create dummy files
        os.makedirs(os.path.join(self.test_dir, "subdir"))
        open(os.path.join(self.test_dir, "vid1.mp4"), 'w').close()
        open(os.path.join(self.test_dir, "img1.png"), 'w').close()
        open(os.path.join(self.test_dir, "subdir", "doc1.txt"), 'w').close()
        open(os.path.join(self.test_dir, "ignore.me"), 'w').close()

        course = self.course_manager.load_course(self.test_dir)
        items = course.get_items()
        
        self.assertEqual(len(items), 3) # vid1, img1, doc1
        names = sorted([i.name for i in items])
        self.assertEqual(names, ['doc1.txt', 'img1.png', 'vid1.mp4'])

    def test_course_manager_state_integration(self):
        course = self.course_manager.load_course(self.test_dir)
        # Should be empty state initially
        vid, time = self.course_manager.get_last_played(course)
        self.assertIsNone(vid)
        
        # Save progress
        self.course_manager.save_progress(course, "vid1.mp4", 5000)
        
        vid, time = self.course_manager.get_last_played(course)
        self.assertEqual(vid, "vid1.mp4")
        self.assertEqual(time, 5000)

if __name__ == '__main__':
    unittest.main()
