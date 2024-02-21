import logging
from collections import defaultdict

from graphviz import Digraph
from sqlglot import exp

from databricks.labs.remorph.helpers.file_utils import (
    get_sql_file,
    is_sql_file,
    read_file,
)
from databricks.labs.remorph.snow.sql_transpiler import SQLTranspiler

logger = logging.getLogger(__name__)


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parents = []

    def add_child(self, node):
        self.children.append(node)
        node.parents.append(self)

    def get_degree(self):
        return len(self.parents)

    def __repr__(self):
        return f"Node({self.name}, {self.children})"


class DAG:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_name):
        if node_name not in self.nodes:
            self.nodes[node_name] = Node(node_name)

    def add_edge(self, parent_name, child_name):
        if parent_name not in self.nodes:
            self.add_node(parent_name)
        if child_name not in self.nodes:
            self.add_node(child_name)
        self.nodes[parent_name].add_child(self.nodes[child_name])

    def __repr__(self):
        return str(self.nodes.values())


class RootTableIdentifier:
    def __init__(self, source, input_path):
        self.source = source
        self.input_path = input_path
        self.root_tables = defaultdict(int)
        self.dag = DAG()

    def generate_lineage(self):
        # when input is sql file then parse the file
        if is_sql_file(self.input_path):
            filename = self.input_path
            sql_content = read_file(filename)
            self._parse_sql_content(sql_content, filename)
            return  # return after processing the file

        # when the input is a directory
        for filename in get_sql_file(self.input_path):
            print("***************")
            print(filename)
            logger.debug(f"Processing file: {filename}")
            sql_content = read_file(filename)
            self._parse_sql_content(sql_content, filename)

    def identify_root_tables(self, level):
        all_nodes = set(self.dag.nodes.values())
        child_nodes = {node for n in self.dag.nodes.values() for node in n.children}
        root_nodes = all_nodes - child_nodes

        # Now we have all root nodes. We need to find the ones at the specified level. We can do this by performing a
        # breadth-first search (BFS) from each root node and stopping at the specified level.

        root_tables_at_level = set()

        for root_node in root_nodes:
            queue = [(root_node, 0)]  # The queue for the BFS. Each element is a tuple (node, level).
            while queue:
                node, node_level = queue.pop(0)

                if node_level == level:
                    if not any(parent for parent in node.parents if parent.get_degree() == node_level):
                        root_tables_at_level.add(node.name)
                elif node_level < level:
                    for child in node.children:
                        queue.append((child, node_level + 1))

        # The list root_tables_at_level now contains all root tables at the specified level.
        # We can print them or return them as needed.

        return root_tables_at_level

    @staticmethod
    def _find_root_tables(expression) -> str:
        for table in expression.find_all(exp.Table, bfs=False):
            return str(table.name).upper()

    def _parse_sql_content(self, sql_content, file_name):
        parse_error_list = []
        parser = SQLTranspiler(self.source, sql_content, file_name, parse_error_list)

        parsed_expression = parser.parse()
        for expr in parsed_expression:
            child = str(file_name)
            if expr is not None:
                for create in expr.find_all(exp.Create, exp.Insert, exp.Merge, bfs=False):
                    child = self._find_root_tables(create)
                    self.dag.add_node(child)

                for select in expr.find_all(exp.Select, exp.Join, exp.With, bfs=False):
                    self.dag.add_edge(self._find_root_tables(select), child)

    def __repr__(self):
        return str({node_name: str(node) for node_name, node in self.dag.nodes.items()})

    def visualize(self, filename="dag", output_format="png"):
        dot = Digraph(graph_attr={"rankdir": "TB"})

        for node in self.dag.nodes.values():
            if node.name is None:
                continue
            dot.node(
                node.name, _attributes={"style": "filled", "color": "black", "fillcolor": "blue", "fontcolor": "white"}
            )
            for child in node.children:
                if child.name is None:
                    continue
                dot.edge(node.name, child.name)

        dot.render(filename, format=output_format, cleanup=True)
