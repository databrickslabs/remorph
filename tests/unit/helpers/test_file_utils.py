import os
import tempfile
import unittest
from pathlib import Path

from databricks.labs.remorph.helpers.file_utils import dir_walk, is_sql_file, make_dir, remove_bom


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

    def test_dir_walk(self):
        """Test 1 - correct structure for single file"""
        path = Path("test_dir")
        path.mkdir()
        (Path(path) / "test_file.txt").touch()
        result = list(dir_walk(path))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], path)
        self.assertEqual(len(result[0][1]), 0)
        self.assertEqual(len(result[0][2]), 1)
        os.remove(Path(path) / "test_file.txt")
        os.rmdir(path)

        """Test 2 - correct structure for nested directories and files"""
        path = Path("test_dir")
        path.mkdir()
        (Path(path) / "test_file.txt").touch()
        (Path(path) / "nested_dir").mkdir()
        (Path(path) / "nested_dir" / "nested_file.txt").touch()
        result = list(dir_walk(path))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], path)
        self.assertEqual(len(result[0][1]), 1)
        self.assertEqual(len(result[0][2]), 1)
        self.assertEqual(result[1][0], Path(path) / "nested_dir")
        self.assertEqual(len(result[1][1]), 0)
        self.assertEqual(len(result[1][2]), 1)
        os.remove(Path(path) / "test_file.txt")
        os.remove(Path(path) / "nested_dir" / "nested_file.txt")
        os.rmdir(Path(path) / "nested_dir")
        os.rmdir(path)

        """Test 3 - empty directory"""
        path = Path("empty_dir")
        path.mkdir()
        result = list(dir_walk(path))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], path)
        self.assertEqual(len(result[0][1]), 0)
        self.assertEqual(len(result[0][2]), 0)
        os.rmdir(path)
