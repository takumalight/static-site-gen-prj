import unittest
import os
from main import *

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        test_file_1_path = os.path.join(os.path.dirname(__file__), 'testing_specimens', 'markdown_testfile_1.md')
        test_file_2_path = os.path.join(os.path.dirname(__file__), 'testing_specimens', 'markdown_testfile_2.md')

        # Test with a file that has a title
        title = extract_title(test_file_1_path)
        self.assertEqual(title, "This is the file heading")

        # Test with a file that has no title
        with self.assertRaises(Exception):
            extract_title(test_file_2_path)
    
    def test_generate_page(self):
        test_file_1_path = os.path.join(os.path.dirname(__file__), 'testing_specimens', 'markdown_testfile_1.md')
        test_file_2_path = os.path.join(os.path.dirname(__file__), 'testing_specimens', 'markdown_testfile_2.md')
        template_path = os.path.join(os.path.dirname(__file__), '..', 'template.html')
        dest_path = os.path.join(os.path.dirname(__file__), 'testing_specimens', 'output.html')

        # Test with a file that has a title
        generate_page(test_file_1_path, template_path, dest_path)
        with open(dest_path, 'r') as f:
            content = f.read()
            self.assertIn("This is the file heading", content)
            self.assertIn("<h1>This is the file heading</h1>", content)

        # Test with a file that has no title
        with self.assertRaises(Exception):
            generate_page(test_file_2_path, template_path, dest_path)