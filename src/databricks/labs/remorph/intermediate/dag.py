import logging

logger = logging.getLogger(__name__)


class Node:
    def __init__(self, name: str):
        self.name = name
        self.children = []
        self.parents = []

    def add_child(self, node: str):
        self.children.append(node)
        node.parents.append(self)

    def get_degree(self):
        return len(self.parents)

    def __repr__(self):
        return f"Node({self.name}, {self.children})"


class DAG:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_name: str):
        if node_name not in self.nodes and node_name is not None:
            self.nodes[node_name] = Node(node_name.lower())

    def add_edge(self, parent_name: str, child_name: str):
        parent_name = parent_name.lower() if parent_name is not None else None
        child_name = child_name.lower() if child_name is not None else None
        logger.debug(f"Adding edge: {parent_name} -> {child_name}")
        if parent_name not in self.nodes and parent_name != "none":
            self.add_node(parent_name)
        if child_name not in self.nodes and child_name != "none":
            self.add_node(child_name)

        if child_name is not None:
            self.nodes[parent_name].add_child(self.nodes[child_name])

    def identify_immediate_parents(self, table_name: str):
        table_name = table_name.lower()  # convert to lower() case
        if table_name in self.nodes:
            return [parent.name for parent in self.nodes[table_name].parents]

    def identify_immediate_children(self, table_name: str):
        table_name = table_name.lower()  # convert to lower() case
        if table_name in self.nodes:
            return [child.name for child in self.nodes[table_name].children]

    def identify_root_tables(self, level: int):
        all_nodes = set(self.nodes.values())
        root_tables_at_level = set()

        for node in all_nodes:
            if len(self.identify_immediate_parents(node.name)) == 0:  # This is a root node
                queue = [(node, 0)]  # The queue for the BFS. Each element is a tuple (node, level).
                while queue:
                    current_node, node_level = queue.pop(0)

                    if node_level == level:
                        root_tables_at_level.add(current_node.name)
                    elif node_level < level:
                        for child_name in self.identify_immediate_children(current_node.name):
                            queue.append((self.nodes[child_name], node_level + 1))

        return root_tables_at_level

    def __repr__(self):
        return str({node_name: str(node) for node_name, node in self.nodes.items()})
