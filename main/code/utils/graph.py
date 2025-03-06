from typing import Optional

class Node[E]:
    def get_child(self, edge:E) -> Optional['Node']:
        pass

    def get_edges(self) -> list[E]:
        pass

    """
    def add_visitor(self, visitor:'GraphWalker'[E]) -> None:
        pass

    def get_visitiors(self) -> list['GraphWalker'[E]]:
        pass

    def remove_visitor(self, visitor:'GraphWalker'[E]) -> bool:
        pass
    """

class NodeGraph[E]:
    def __init__(self, head:Node[E]):
        self.head = head

    def get_child(self, node:Node[E], edge:E) -> Optional['Node']:
        return node.get_child(edge)

    def get_edges(self, node:Node[E]) -> list[E]:
        return node.get_edges()

"""
class GraphWalker[E]:

    def __init__(self, node:Node[E]):
        self.node = node

    def get_node(self) -> Node[E]:
        return self.node

    def set_node(self, node:Node[E]) -> None:
        pass

    def remove_from_graph(self) -> None:
        pass

    def walk(self, edge:E) -> Node|None:
        end_node = self.node.get_child(edge)
        if end_node is not None:
            self.node = end_node
        return end_node
    
    def get_available_edges(self) -> list[E]:
        return self.node.get_edges()
"""