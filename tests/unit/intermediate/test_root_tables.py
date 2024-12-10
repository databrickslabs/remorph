import pytest

from databricks.labs.remorph.intermediate.root_tables import RootTableLocator


@pytest.fixture(autouse=True)
def setup_file(tmpdir):
    file = tmpdir.join("test.sql")
    file.write(
        """create table table1 select * from table2 inner join
         table3 on table2.id = table3.id  where table2.id in (select id from table4);
        create table table2 select * from table4;
        create table table5 select * from table3 join table4 on table3.id = table4.id ;
            """
    )
    return file


def test_generate_lineage(tmpdir):
    root_table_identifier = RootTableLocator("snowflake", str(tmpdir))
    dag = root_table_identifier.generate_lineage()
    roots = ["table2", "table3", "table4"]

    assert len(dag.nodes["table4"].parents) == 0
    assert len(dag.identify_immediate_children("table3")) == 2
    assert dag.identify_immediate_parents("table1") == roots
    assert dag.identify_root_tables(0) == {"table3", "table4"}
    assert dag.identify_root_tables(2) == {"table1"}
    assert dag.identify_immediate_parents("none") == []


def test_generate_lineage_sql_file(setup_file):
    root_table_identifier = RootTableLocator("snowflake", str(setup_file))
    dag = root_table_identifier.generate_lineage(engine="sqlglot")
    roots = ["table2", "table3", "table4"]

    assert len(dag.nodes["table4"].parents) == 0
    assert len(dag.identify_immediate_children("table3")) == 2
    assert dag.identify_immediate_parents("table1") == roots
    assert dag.identify_root_tables(0) == {"table3", "table4"}
    assert dag.identify_root_tables(2) == {"table1"}
    assert dag.identify_immediate_children("none") == []


def test_non_sqlglot_engine_raises_error(tmpdir):
    root_table_identifier = RootTableLocator("snowflake", str(tmpdir))
    with pytest.raises(ValueError):
        root_table_identifier.generate_lineage(engine="antlr")
