import pytest

from databricks.labs.remorph.mixins.root_table import DAG, Node, RootTableIdentifier


@pytest.fixture
def node():
    return Node("Parent")


@pytest.fixture
def dag():
    return DAG()


@pytest.fixture
def root_table_identifier(tmp_path):
    return RootTableIdentifier("snowflake", tmp_path)


def test_add_child(node):
    child_node = Node("child")
    node.add_child(child_node)
    assert node.children[0] == child_node
    assert child_node.parents[0] == node


def test_get_degree(node):
    assert node.get_degree() == 0
    child_node = Node("child")
    node.add_child(child_node)
    assert child_node.get_degree() == 1


def test_add_node(dag):
    dag.add_node("Parent")
    assert "parent" in dag.nodes


def test_add_edge(dag):
    dag.add_edge("parent", "child")
    assert "PARENT" in dag.nodes
    assert "CHILD" in dag.nodes
    assert dag.nodes["child".upper()] in dag.nodes["parent".upper()].children


def test_identify_root_tables(root_table_identifier):
    root_table_identifier.dag.add_edge("parent_node", "child_node")
    root_tables = root_table_identifier.identify_root_tables(0)
    assert "PARENT_NODE" in root_tables


def test_generate_lineage(root_table_identifier, tmpdir):
    tmpfile = tmpdir.join("test.sql")
    tmpfile.write(
        """create table table1 select * from table2
        inner join table3 on table2.id = table3.id
        where table2.id in (select id from table4)"""
    )
    root_table_identifier = RootTableIdentifier("snowflake", str(tmpdir))
    root_table_identifier.generate_lineage()
    roots = {"TABLE2", "TABLE3", "TABLE4"}

    assert len(root_table_identifier.dag.nodes["TABLE4"].parents) == 0
    assert len(root_table_identifier.dag.nodes["TABLE3"].parents) == 0
    assert len(root_table_identifier.dag.nodes["TABLE1"].parents) == 3
    assert {parent.name for parent in root_table_identifier.dag.nodes["TABLE1"].parents} == roots


def test_generate_lineage_sql_file(tmpdir):
    tmpfile = tmpdir.join("test.sql")
    tmpfile.write(
        """create table table1 select * from table2
        inner join table3 on table2.id = table3.id
        where table2.id in (select id from table4)"""
    )
    root_table_identifier = RootTableIdentifier("snowflake", str(tmpfile))
    root_table_identifier.generate_lineage()
    roots = {"TABLE2", "TABLE3", "TABLE4"}

    assert len(root_table_identifier.dag.nodes["TABLE4"].parents) == 0
    assert len(root_table_identifier.dag.nodes["TABLE3"].parents) == 0
    assert len(root_table_identifier.dag.nodes["TABLE1"].parents) == 3
    assert {parent.name for parent in root_table_identifier.dag.nodes["TABLE1"].parents} == roots
