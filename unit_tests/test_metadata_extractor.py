import os
import unittest
from utils.metadata_extractor import metadata_extractor


class MetadataExtractor(unittest.TestCase):
    def test_metadata_extractor(self):
        path = os.getcwd()
        properties = metadata_extractor(r"{}/unit_tests/test_ge.py".format(path))
        self.assertIn("File Name", properties.keys())
        self.assertIn("Creation Date", properties.keys())
        self.assertIn("Last Edit Date", properties.keys())
        self.assertIn("File Size", properties.keys())
        self.assertIn("Hash Value", properties.keys())


if __name__ == "__main__":
    unittest.main()
