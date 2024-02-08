import os
from collections import defaultdict

from sqlglot import exp, parse
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, node):
        self.children.append(node)


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


class RootTableIdentifier:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.root_tables = defaultdict(int)
        self.dag = DAG()

    def generate_lineage(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".sql"):
                with open(os.path.join(self.folder_path, filename)) as file:
                    sql_content = file.read()
                    self._parse_sql_content(sql_content, filename)

    def identify_root_tables(self):
        self.generate_lineage()
        #[TODO] implement the logic to identify the root tables at each level

    @staticmethod
    def _find_root_tables(expression) -> str:
        for table in expression.find_all(exp.Table, bfs=False):
            return table.name

    def _parse_sql_content(self, sql_content, file_name):
        parsed_expression = parse(sql_content)
        for expr in parsed_expression:
            child = file_name
            for create in expr.find_all(exp.Create, exp.Insert, bfs=False):
                child = self._find_root_tables(create)
                self.dag.add_node(child)

            for select in expr.find_all(exp.Select, exp.Join, exp.With, bfs=False):
                self.dag.add_edge(self._find_root_tables(select), child)

    def visualize(self):
        G = nx.DiGraph()  # noqa N806

        for node in self.dag.nodes.values():
            G.add_node(node.name)
            for c in node.children:
                G.add_edge(node.name, c.name)

        nx.draw(G, with_labels=True)
        plt.show()

