import math
from typing import TypeVar, Iterable, Callable

T = TypeVar('T')


def dijkstra(source_node: T, target_node: T,
             find_children_nodes: Callable[[int], Iterable[T]], get_distance: Callable[[T, T], int],
             limit: int = math.inf) -> list[T]:
    """
    Find the shortest path from a node to all other nodes in a graph.

    Args:
        source_node: The node to start the search from.
        target_node: The node to end the search at.
        find_children_nodes: A function that returns the edges of the graph.
        get_distance: A function that returns the distance between two node.
        limit: The maximum distance to search.

    Returns:
        A list of nodes in the shortest path from the start node to all other nodes.
    """
    if not (hasattr(source_node, 'id') and hasattr(target_node, 'id')):
        raise TypeError('node must have an id attribute')

    if not callable(find_children_nodes) or not callable(get_distance):
        raise TypeError('find_children_nodes and get_distance must be callable')

    setattr(source_node, 'from', None)
    setattr(source_node, 'distance', 0)

    if source_node == target_node:
        return [source_node]

    selected_nodes: list[T] = [source_node]
    nodes: list[T] = []
    visited_nodes: set[T] = set(selected_nodes)

    current_node = selected_nodes[0]
    i = 0

    while i < limit:
        children_nodes = find_children_nodes(current_node.id)

        if any(children_node.id == target_node.id for children_node in children_nodes):
            return selected_nodes + [target_node]

        visited_nodes_id = list(map(lambda visited_node: visited_node.id, visited_nodes))

        children_nodes = filter(lambda node: node.id not in visited_nodes_id, children_nodes)
        nodes = list(filter(lambda node: node.id not in visited_nodes_id, nodes))

        if len(nodes) == 0:
            nearest_node = None
            nearest_distance = math.inf
        else:
            nearest_node = min(nodes, key=lambda node: getattr(node, 'distance'))
            nearest_distance = getattr(nearest_node, 'distance')

        for children_node in children_nodes:
            children_node_distance = get_distance(current_node, children_node)

            setattr(children_node, 'from', current_node)
            setattr(children_node, 'distance', children_node_distance + getattr(current_node, 'distance'))

            nodes.append(children_node)

            if nearest_node is None or nearest_distance > children_node_distance:
                nearest_node = children_node
                nearest_distance = children_node_distance

        selected_nodes.append(nearest_node)
        visited_nodes.add(nearest_node)
        current_node = nearest_node

        i += 1

    return []
