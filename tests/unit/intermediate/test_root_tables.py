import pytest

from databricks.labs.remorph.intermediate.root_tables import RootTableIdentifier


@pytest.fixture(autouse=True)
def setup_file(tmpdir):
    file = tmpdir.join("test.sql")
    file.write(
        """create table table1 select * from table2
        inner join table3 on table2.id = table3.id
        where table2.id in (select id from table4)"""
    )
    return file


def test_generate_lineage(tmpdir):
    root_table_identifier = RootTableIdentifier("snowflake", str(tmpdir))
    dag = root_table_identifier.generate_lineage()
    roots = {"table2", "table3", "table4"}

    assert len(dag.nodes["table4"].parents) == 0
    assert len(dag.nodes["table3"].parents) == 0
    assert len(dag.nodes["table1"].parents) == 3
    assert {parent.name for parent in dag.nodes["table1"].parents} == roots


def test_generate_lineage_sql_file(setup_file):
    root_table_identifier = RootTableIdentifier("snowflake", str(setup_file))
    dag = root_table_identifier.generate_lineage(engine="sqlglot")
    roots = {"table2", "table3", "table4"}

    assert len(dag.nodes["table4"].parents) == 0
    assert len(dag.nodes["table3"].parents) == 0
    assert len(dag.nodes["table1"].parents) == 3
    assert {parent.name for parent in dag.nodes["table1"].parents} == roots
    assert dag.identify_root_tables(0) == roots
    assert dag.identify_root_tables(1) == {"table1"}


def test_non_sqlglot_engine_raises_error(tmpdir):
    root_table_identifier = RootTableIdentifier("snowflake", str(tmpdir))
    with pytest.raises(ValueError):
        root_table_identifier.generate_lineage(engine="antlr")
