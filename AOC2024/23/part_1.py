import os
from typing import Dict, List, Set


class Node(object):
    def __init__(self, id: str):
        self.id = id
        self.connections: Dict[str, Node] = {}

    def add_connection(self, node):
        self.connections[node.id] = node

    def is_connected_to(self, node_id: str) -> bool:
        return node_id in self.connections

    def get_groups(self) -> List[List[str]]:
        groups: List[List[str]] = []
        connections = list(self.connections.values())
        for i in range(len(connections)):
            i_node = connections[i]
            for j in range(i + 1, len(connections)):
                j_node = connections[j]
                if i_node.is_connected_to(j_node.id):
                    groups.append(sorted([self.id, i_node.id, j_node.id]))

        return groups


nodes: Dict[str, Node] = {}
t_nodes: List[Node] = []
input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, "r") as in_file:
    for line in in_file:
        line = line.strip()
        connection = line.split("-")
        a_node_id = connection[0]
        if a_node_id not in nodes:
            node = Node(a_node_id)
            nodes[node.id] = node
            if node.id.startswith("t"):
                t_nodes.append(node)

        b_node_id = connection[1]
        if b_node_id not in nodes:
            node = Node(b_node_id)
            nodes[node.id] = node
            if node.id.startswith("t"):
                t_nodes.append(node)

        a_node = nodes[a_node_id]
        b_node = nodes[b_node_id]
        a_node.add_connection(b_node)
        b_node.add_connection(a_node)

unique_sets: Set[str] = set()
for node in t_nodes:
    groups = node.get_groups()
    for group in groups:
        unique_sets.add(str(group))

print(f"Found {len(unique_sets)} mutual groups of three.")
