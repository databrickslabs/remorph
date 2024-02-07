import os
import sqlglot
from collections import defaultdict
import dsplot


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, node):
        self.children.append(node)


class Tree:
    def __init__(self, root):
        self.root = Node(root)

    def add_node(self, parent_name, node_name):
        parent_node = self.find_node(self.root, parent_name)
        if parent_node is not None:
            parent_node.add_child(Node(node_name))

    def find_node(self, node, name):
        if node.name == name:
            return node
        for child in node.children:
            found_node = self.find_node(child, name)
            if found_node is not None:
                return found_node
        return None


class RootTableIdentifier:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.root_tables = defaultdict(int)
        self.tree = None

    def identify_root_tables(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.sql'):
                with open(os.path.join(self.folder_path, filename), 'r') as file:
                    sql_content = file.read()
                    self._parse_sql_content(sql_content)

        root_tables = [table for table, count in self.root_tables.items() if count == 1]
        if root_tables:
            self.tree = Tree(root_tables[0])
            for table in root_tables[1:]:
                self.tree.add_node(root_tables[0], table)

    def _find_root_tables(self, expression):
        for token in expression.from_:
            if isinstance(token, sqlglot.expressions.Table):
                self.root_tables[token.args['this']] += 1

    def _parse_sql_content(self, sql_content):
        parsed_expression = sqlglot.parse_one(sql_content)
        for select in parsed_expression.find_all(sqlglot.expressions.Select, bfs=False):
            self._find_root_tables(select)

        for expression in parsed_expression:
            if isinstance(expression, sqlglot.expressions.Select):
                for token in expression.columns:
                    if isinstance(token, sqlglot.expressions.Identifier):
                        self.root_tables[token.args['this']] += 1

    def visualize(self):
        if self.tree is not None:
            self._dsplot_tree(self.tree.root)

    def _dsplot_tree(self, node, parent_name=None):
        if parent_name is not None:
            dsplot.arrow(parent_name, node.name)
        for child in node.children:
            self._dsplot_tree(child, node.name)
