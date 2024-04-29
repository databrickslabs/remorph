import codecs
import os
import tempfile
from pathlib import Path

import pytest

from databricks.labs.remorph.helpers.file_utils import (
    dir_walk,
    is_sql_file,
    make_dir,
    refactor_hexadecimal_chars,
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
    with tempfile.TemporaryDirectory() as temp_dir:
        new_dir_path = temp_dir.join("new_dir")

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


def test_dir_walk_single_file():
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


def test_dir_walk_nested_files():
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


def test_dir_walk_empty_dir():
    path = Path("empty_dir")
    path.mkdir()
    result = list(dir_walk(path))

    assert len(result) == 1
    assert result[0][0] == path
    assert len(result[0][1]) == 0
    assert len(result[0][2]) == 0
    safe_remove_dir(path)


def test_refactor_hexadecimal_chars():
    input_string = "SELECT * FROM test \x1b[4mWHERE\x1b[0m"
    output_string = "SELECT * FROM test --> WHERE <--"
    assert refactor_hexadecimal_chars(input_string) == output_string

    input_string2 = "SELECT \x1b[4marray_agg(\x1b[0mafter_state order by timestamp asc) FROM dual"
    output_string2 = "SELECT --> array_agg( <--after_state order by timestamp asc) FROM dual"
    assert refactor_hexadecimal_chars(input_string2) == output_string2
