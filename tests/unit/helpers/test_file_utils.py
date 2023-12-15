import os
import tempfile
import unittest

from databricks.labs.remorph.helpers.file_utils import is_sql_file, make_dir, remove_bom


class TestUtilsMethods(unittest.TestCase):
    def test_remove_bom(self):
        # Test UTF-8 BOM
        self.assertEqual(remove_bom("\ufeffTest"), "Test")

        # Test UTF-16 BE BOM
        self.assertEqual(remove_bom("\ufeffTest"), "Test")

        # Test UTF-32 BE BOM
        self.assertEqual(remove_bom("\ufeffTest"), "Test")

        # Test no BOM
        self.assertEqual(remove_bom("Test"), "Test")

    def test_is_sql_file(self):
        self.assertTrue(is_sql_file("test.sql"))
        self.assertTrue(is_sql_file("test.ddl"))
        self.assertFalse(is_sql_file("test.txt"))
        self.assertFalse(is_sql_file("test"))

    def test_make_dir(self):
        temp_dir = tempfile.TemporaryDirectory()
        new_dir_path = os.path.join(temp_dir.name, "new_dir")

        # Ensure the directory does not exist
        self.assertFalse(os.path.exists(new_dir_path))

        # Call the function to create the directory
        make_dir(new_dir_path)

        # Check if the directory now exists
        self.assertTrue(os.path.exists(new_dir_path))
