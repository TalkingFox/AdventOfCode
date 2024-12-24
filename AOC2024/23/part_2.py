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

    def get_connection_count(self) -> int:
        return len(self.connections)


class Group(object):
    def __init__(self):
        self.members: Dict[str, Node] = {}

    def can_admit(node: Node) -> bool:
        return False

    def add_node(node: Node) -> None:
        pass


nodes: Dict[str, Node] = {}
input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, "r") as in_file:
    for line in in_file:
        if line == "\n" or not line:
            continue
        line = line.strip()
        connection = line.split("-")
        a_node_id = connection[0]
        if a_node_id not in nodes:
            node = Node(a_node_id)
            nodes[node.id] = node

        b_node_id = connection[1]
        if b_node_id not in nodes:
            node = Node(b_node_id)
            nodes[node.id] = node

        a_node = nodes[a_node_id]
        b_node = nodes[b_node_id]
        a_node.add_connection(b_node)
        b_node.add_connection(a_node)


def find_cliques(
    nodes_by_id: Dict[str, Node],
    current_clique: Set[str],
    prospective_nodes: Set[str],
    excluded_nodes: Set[str],
) -> List[Set[str]]:
    if not any(prospective_nodes) and not any(excluded_nodes):
        return [current_clique]

    total_cliques = []
    for node in list(prospective_nodes):
        connections = set(nodes_by_id[node].connections.keys())

        next_level_clique = current_clique.union([node])
        next_level_prospective_nodes = prospective_nodes.intersection(connections)
        next_level_exclusions = excluded_nodes.intersection(connections)

        total_cliques.extend(
            find_cliques(
                nodes_by_id,
                next_level_clique,
                next_level_prospective_nodes,
                next_level_exclusions,
            )
        )

        prospective_nodes.remove(node)
        excluded_nodes.add(node)

    return total_cliques


cliques = find_cliques(
    nodes,
    current_clique=set(),
    prospective_nodes=set(nodes.keys()),
    excluded_nodes=set(),
)

max_clique: Set[str] = set()
for clique in cliques:
    if len(clique) > len(max_clique):
        max_clique = clique

print(",".join(sorted(list(max_clique))))
