from unittest.mock import create_autospec

import pytest
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.intermediate.infer_schema import InferSchema


@pytest.fixture(autouse=True)
def setup_file(tmpdir):
    file = tmpdir.join("test.sql")
    file.write(
        """SELECT a.col1, sum(b.col2) as col2, to_date(col11) 
        FROM tb1 AS a INNER JOIN tb2 AS b ON a.col7 = b.col8
        LEFT JOIN tbl3 ON a.col9 = col10"""
    )
    second_file = tmpdir.join("test2.sql")
    second_file.write("""SELECT a.col1 from table10 as a;""")
    return file


def test_generate_schema_dir(tmpdir):
    ws = create_autospec(WorkspaceClient)
    infer_schema = InferSchema(ws, "snowflake", str(tmpdir))

    result = infer_schema.generate_schema()

    # Assert the result is as expected
    expected_result = {
        "table10": "CREATE TABLE table10 (col1 string);",
        "tb1": "CREATE TABLE tb1 (col1 string, col7 string, col9 string);",
        "tb2": "CREATE TABLE tb2 (col2 string, col8 string);",
        "tbl3": "CREATE TABLE tbl3 (col10 string, col11 string);",
    }
    assert result == expected_result


def test_generate_schema_file(setup_file):
    ws = create_autospec(WorkspaceClient)
    infer_schema = InferSchema(ws, "snowflake", str(setup_file))

    result = infer_schema.generate_schema()

    # Assert the result is as expected
    expected_result = {
        "tb1": "CREATE TABLE tb1 (col1 string, col7 string, col9 string);",
        "tb2": "CREATE TABLE tb2 (col2 string, col8 string);",
        "tbl3": "CREATE TABLE tbl3 (col10 string, col11 string);",
    }
    assert result == expected_result


def test_non_sqlglot_engine_raises_error_infer_schema(tmpdir):
    ws = create_autospec(WorkspaceClient)
    infer_schema = InferSchema(ws, "snowflake", str(tmpdir))
    with pytest.raises(ValueError):
        infer_schema.generate_schema(engine="antlr")
