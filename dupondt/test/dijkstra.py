import unittest

from dupondt.find_path.dijkstra import dijkstra


class Node:
    def __init__(self, id: int):
        self.id = id
        self.children: list[Node] = []
        self.d = 0

    def add_children(self, node, distance: int):
        self.children.append(node)
        self.d = distance


test_nodes = {k: Node(k) for k in range(1, 8)}
test_nodes[1].add_children(test_nodes[2], 1)
test_nodes[1].add_children(test_nodes[3], 2)

test_nodes[2].add_children(test_nodes[1], 1)
test_nodes[2].add_children(test_nodes[6], 3)
test_nodes[2].add_children(test_nodes[4], 2)

test_nodes[3].add_children(test_nodes[1], 2)
test_nodes[3].add_children(test_nodes[4], 3)
test_nodes[3].add_children(test_nodes[5], 4)

test_nodes[4].add_children(test_nodes[2], 2)
test_nodes[4].add_children(test_nodes[3], 3)
test_nodes[4].add_children(test_nodes[5], 2)
test_nodes[4].add_children(test_nodes[6], 3)
test_nodes[4].add_children(test_nodes[7], 3)

test_nodes[5].add_children(test_nodes[3], 4)
test_nodes[5].add_children(test_nodes[4], 2)
test_nodes[5].add_children(test_nodes[7], 5)

test_nodes[6].add_children(test_nodes[2], 3)
test_nodes[6].add_children(test_nodes[4], 3)
test_nodes[6].add_children(test_nodes[7], 4)

test_nodes[7].add_children(test_nodes[4], 3)
test_nodes[7].add_children(test_nodes[5], 5)
test_nodes[7].add_children(test_nodes[6], 4)


def get_distance(node1, node2):
    for child in node1.children:
        if child.id == node2.id:
            return getattr(child, 'd')


class TestDijkstraAlgorithm(unittest.TestCase):
    def test_shortest_path(self):
        self.assertEqual(
            list(map(
                lambda v: v.id,
                dijkstra(test_nodes[1], test_nodes[7], lambda node_id: test_nodes[node_id].children, get_distance)
            )),
            [1, 2, 4, 7]
        )


if __name__ == '__main__':
    unittest.main()
