import pytest


@pytest.fixture()
def io_dir_pair(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    input_file = input_dir / "test.sql"
    input_file.write_text("SELECT * FROM test")

    output_dir = tmp_path / "output"

    yield input_dir, output_dir
