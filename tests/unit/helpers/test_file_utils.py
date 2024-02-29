import codecs
import os
import tempfile
from pathlib import Path

import pytest

from databricks.labs.remorph.helpers.file_utils import (
    dir_walk,
    get_sql_file,
    is_sql_file,
    make_dir,
    read_file,
    remove_bom,
)


@pytest.fixture(scope="module")
def setup_module(tmp_path_factory):
    test_dir = tmp_path_factory.mktemp("test_dir")
    sql_file = test_dir / "test.sql"
    sql_file.write_text("SELECT * FROM test;")
    non_sql_file = test_dir / "test.txt"
    non_sql_file.write_text("This is a test.")
    return test_dir, sql_file, non_sql_file


def test_remove_bom():
    test_string = "test_string"

    # Test no BOM
    assert remove_bom(test_string) == test_string

    # Test UTF-16 BOM
    # "******** UTF-16 ********"
    input_string = codecs.BOM_UTF16.decode("utf-16") + test_string
    assert remove_bom(input_string) == test_string

    # "******** UTF-16-BE ********"
    input_string = codecs.BOM_UTF16_BE.decode("utf-16-be") + test_string
    assert remove_bom(input_string) == test_string

    # "******** UTF-16-LE ********"
    input_string = codecs.BOM_UTF16_LE.decode("utf-16-le") + test_string
    assert remove_bom(input_string) == test_string

    # Test UTF-32 BOM
    # "******** UTF-32 ********"
    input_string = codecs.BOM_UTF32.decode("utf-32") + test_string
    assert remove_bom(input_string) == test_string

    # "******** UTF-32-BE ********"
    input_string = codecs.BOM_UTF32_BE.decode("utf-32-be") + test_string
    assert remove_bom(input_string) == test_string

    # "******** UTF-32-LE ********"
    input_string = codecs.BOM_UTF32_LE.decode("utf-32-le") + test_string
    assert remove_bom(input_string) == test_string

    # Test UTF8 BOM
    # "******** UTF-8 ********"
    input_string = codecs.BOM_UTF8.decode("utf-8") + test_string
    assert remove_bom(input_string) == test_string


def test_is_sql_file():
    assert is_sql_file("test.sql") is True
    assert is_sql_file("test.ddl") is True
    assert is_sql_file("test.txt") is False
    assert is_sql_file("test") is False


def test_make_dir():
    temp_dir = tempfile.TemporaryDirectory()
    new_dir_path = os.path.join(temp_dir.name, "new_dir")

    # Ensure the directory does not exist
    assert os.path.exists(new_dir_path) is False

    # Call the function to create the directory
    make_dir(new_dir_path)

    # Check if the directory now exists
    assert os.path.exists(new_dir_path) is True


def safe_remove_file(file_path: Path):
    if file_path.exists():
        file_path.unlink()


def safe_remove_dir(dir_path: Path):
    if dir_path.exists():
        dir_path.rmdir()


def test_dir_walk():
    # [TODO] - Refactor the tests using setup module
    """Test 1 - correct structure for single file"""
    try:
        path = Path("test_dir")
        path.mkdir()
        (path / "test_file.txt").touch()
        result = list(dir_walk(path))
        assert len(result) == 1
        assert result[0][0] == path
        assert len(result[0][1]) == 0
        assert len(result[0][2]) == 1
        safe_remove_file(path / "test_file.txt")
        safe_remove_dir(path)
    except Exception as e:
        safe_remove_file(path / "test_file.txt")
        safe_remove_dir(path)
        raise Exception("Error in Test 1 - correct structure for single file") from e

    """Test 2 - correct structure for nested directories and files"""
    try:
        path = Path("test_dir")
        path.mkdir()
        (path / "test_file.txt").touch()
        (path / "nested_dir").mkdir()
        (path / "nested_dir" / "nested_file.txt").touch()
        result = list(dir_walk(path))
        assert len(result) == 2
        assert result[0][0] == path
        assert len(result[0][1]) == 1
        assert len(result[0][2]) == 1
        assert result[1][0] == path / "nested_dir"
        assert len(result[1][1]) == 0
        assert len(result[1][2]) == 1
        safe_remove_file(path / "test_file.txt")
        safe_remove_file(path / "nested_dir" / "nested_file.txt")
        safe_remove_dir(path / "nested_dir")
        safe_remove_dir(path)
    except Exception as e:
        safe_remove_file(path / "test_file.txt")
        safe_remove_file(path / "nested_dir" / "nested_file.txt")
        safe_remove_dir(path / "nested_dir")
        safe_remove_dir(path)
        raise Exception("Error in Test 2 - correct structure for nested directories and files") from e

    """Test 3 - empty directory"""
    try:
        path = Path("empty_dir")
        path.mkdir()
        result = list(dir_walk(path))
        assert len(result) == 1
        assert result[0][0] == path
        assert len(result[0][1]) == 0
        assert len(result[0][2]) == 0
        safe_remove_dir(path)
    except Exception as e:
        safe_remove_dir(path)
        raise Exception("Error in Test 3 - empty directory") from e


def test_get_sql_file(setup_module):
    test_dir, sql_file, _ = setup_module
    sql_files = list(get_sql_file(test_dir))
    assert len(sql_files) == 1
    assert sql_files[0] == sql_file


def test_read_file(setup_module):
    _, sql_file, _ = setup_module
    content = read_file(sql_file)
    assert content == "SELECT * FROM test;"
