import pytest
from databricks.labs.remorph.mixins.root_table import Node, DAG, RootTableIdentifier


@pytest.fixture
def node():
    return Node("test")


def test_add_child(node):
    child_node = Node("child")
    node.add_child(child_node)
    assert node.children[0] == child_node
    assert child_node.parents[0] == node


def test_get_degree(node):
    assert node.get_degree() == 0
    child_node = Node("child")
    node.add_child(child_node)
    assert node.get_degree() == 1


@pytest.fixture
def dag():
    return DAG()


def test_add_node(dag):
    dag.add_node("test")
    assert "test" in dag.nodes


def test_add_edge(dag):
    dag.add_edge("parent", "child")
    assert "parent" in dag.nodes
    assert "child" in dag.nodes
    assert dag.nodes["child"] in dag.nodes["parent"].children


@pytest.fixture
def identifier():
    return RootTableIdentifier("test_folder")


def test_identify_root_tables(identifier):
    identifier.dag.add_edge("parent", "child")
    assert identifier.identify_root_tables(0) == {"parent"}
