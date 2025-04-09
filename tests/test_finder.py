import unittest
import os
from utils.finder import get_file_path_from_output

class TestFinder(unittest.TestCase):
    def setUp(self):
        self.output_dir = "output"
        self.test_file = "test_file.txt"
        os.makedirs(self.output_dir, exist_ok=True)
        with open(os.path.join(self.output_dir, self.test_file), "w") as f:
            f.write("Test content.")

    def tearDown(self):
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                os.remove(os.path.join(self.output_dir, file))
            os.rmdir(self.output_dir)

    def test_get_file_path_from_output(self):
        path = get_file_path_from_output(self.test_file, self.output_dir)
        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))

    def test_get_file_path_from_output_not_found(self):
        path = get_file_path_from_output("non_existent_file.txt", self.output_dir)
        self.assertIsNone(path)

if __name__ == "__main__":
    unittest.main()
