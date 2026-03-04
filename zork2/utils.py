import logging
from abc import ABC, abstractmethod
import random
import dataclasses

from frozendict import frozendict

import networkx as nx

logger = logging.getLogger(__name__)

class Named(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def get_aliases(self) -> list[str]:
        pass

@dataclasses.dataclass(frozen=True)
class ItemLimit:
    size_limit   : float|None = None
    weight_limit : float|None = None
    value_limit  : float|None = None

    def get_size_limit(self) -> float|None:
        return self.size_limit

    def get_weight_limit(self) -> float|None:
        return self.weight_limit

    def get_value_limit(self) -> float|None:
        return self.value_limit

class HasLocation(Named):
    @abstractmethod
    def get_weight(self) -> float:
        pass

    @abstractmethod
    def get_size(self) -> float:
        pass

    @abstractmethod
    def get_value(self) -> float:
        pass

class Container(Named):
    @abstractmethod
    def get_limit(self) -> ItemLimit:
        pass

class Carrier(HasLocation):
    @abstractmethod
    def get_children(self, names: 'NameFinder') -> list[HasLocation]:
        pass

class HasInventory(Carrier):
    @abstractmethod
    def get_inventory(self, names: 'NameFinder') -> Container:
        pass

class HasWearing(Carrier):
    @abstractmethod
    def get_wearing(self, names: 'NameFinder') -> Container:
        pass

class Path(Container):
    @abstractmethod
    def list_starts(self, names: 'NameFinder') -> list[tuple[Container, Named]]:
        pass

    @abstractmethod
    def list_possible_ends(self, names: 'NameFinder', start: Container) -> list[Container]:
        pass

def _category(named: Named) -> str:
    cat = str(type(named)).lower().rsplit(".", maxsplit=1)[-1][:-2]
    if 'action' in cat:
        return 'action'
    return cat

class ItemTree:
    def __init__(self, *, graph:nx.DiGraph=None):
        self.__graph = graph if graph else nx.DiGraph()

    def __repr__(self) -> str:
        return str(self.__graph.edges)

    # initialization

    def add_node(self, node: HasLocation|Container, category: str|None = None) -> 'ItemTree':
        if category is None:
            category = _category(node)
        new_graph = self.__graph.copy()
        new_graph.add_node(node.get_id(), category=category)
        return ItemTree(graph=new_graph)

    def __add_edge(self, graph: nx.DiGraph, child: HasLocation, parent: Container):
        graph.add_edge(parent.get_id(), child.get_id(), relationship="child")

    def __add_child(self, graph: nx.DiGraph, child: HasLocation, parent: Container, category: str):
        graph.add_node(child.get_id(), category=category)
        self.__add_edge(graph, child, parent)

    def add_child(self, child: HasLocation, parent: Container, category: str|None = None) -> 'ItemTree':
        if category is None:
            category = _category(child)
        new_graph = self.__graph.copy()
        self.__add_child(new_graph, child, parent, category)
        return ItemTree(graph=new_graph)

    def add_carrier(self, names: 'NameFinder', carrier: Carrier, parent: Container, category: str|None = None, child_category: str|None = None) -> 'ItemTree':
        if category is None:
            category = _category(carrier)
        new_graph = self.__graph.copy()
        new_graph.add_node(carrier.get_id(), category=category)
        self.__add_edge(new_graph, carrier, parent)
        for child in carrier.get_children(names):
            if child_category is None:
                child_category = _category(child)
            self.__add_child(new_graph, child, carrier, child_category)
        return ItemTree(graph=new_graph)

    # mutators

    def move(self, child: HasLocation, new_parent: Container) -> 'ItemTree':
        new_graph = self.__graph.copy()
        old_parent = self.get_parent(child)
        if old_parent is None:
            raise RuntimeError("Wrong number of parents for item to be moved.")
        new_graph.remove_edge(old_parent, child.get_id())
        new_graph.add_edge(new_parent.get_id(), child.get_id(), relationship="child")
        return ItemTree(graph=new_graph)

    # utils

    def contains(self, node: HasLocation|Container) -> bool:
        return node.get_id() in self.__graph

    def get_inventory_contents(self, names: 'NameFinder', node: HasInventory) -> list[str]:
        inventory = node.get_inventory(names)
        contents  = self.get_children(inventory)
        return contents

    def is_wearing(self, names: 'NameFinder', node: HasWearing, item: Named) -> bool:
        return item.get_id() in self.get_children(node.get_wearing(names))

    def is_holding(self, names: 'NameFinder', node: HasInventory, item: Named) -> bool:
        return item.get_id() in self.get_children(node.get_inventory(names))

    def get_local_tree(self, node: HasLocation|Container) -> 'ItemTree':
        ancestors   : set[str] = nx.ancestors(self.__graph, node.get_id())
        descendants : set[str] = nx.descendants(self.__graph, node.get_id())
        nodes                  = ancestors | {node.get_id()} | descendants
        subgraph               = self.__graph.subgraph(nodes).copy()
        return ItemTree(graph=subgraph)

    def get_subtree(self, node: HasLocation|Container) -> 'ItemTree':
        descendants : set[str] = nx.descendants(self.__graph, node.get_id())
        nodes                  = {node.get_id()} | descendants
        subgraph               = self.__graph.subgraph(nodes).copy()
        return ItemTree(graph=subgraph)

    def get_parent(self, node: HasLocation|Container) -> str|None:
        parents = list(self.__graph.predecessors(node.get_id()))
        if len(parents) > 0:
            return parents[0]
        return None

    def get_children(self, node: HasLocation|Container) -> list[str]:
        return [self.__graph.nodes[c] for c in self.__graph.successors(node.get_id())]

    def get_top_parent(self, node: HasLocation|Container) -> str:
        top = node
        parents = list(self.__graph.predecessors(node.get_id()))
        while parents:
            top = parents[0]
            parents = list(self.__graph.predecessors(parents[0]))
        return top

class WorldMap:
    def __init__(self, *, init_map: frozendict[str,frozendict[str,str]]|None=None):
        self.__world_map : frozendict[str,frozendict[str,str]] = init_map if init_map is not None else frozendict()

    def get_rep(self, names: 'NameFinder') -> str:
        edges = []
        for room, directions in self.__world_map.items():
            for direction, path_id in directions.items():
                path : Path = names.get_from_id(path_id)
                for possible_end in path.list_possible_ends(names, names.get_from_id(room)):
                    edges.append((room, direction, possible_end.get_id()))
        return str(edges)

    # initialization

    def add_path(self, names: 'NameFinder', path: Path) -> 'WorldMap':
        new_map = {key:dict(val) for key, val in self.__world_map.items()}
        for start, direction in path.list_starts(names):
            if not start in new_map:
                new_map[start.get_id()] = {}
            new_map[start.get_id()][direction.get_id()] = path.get_id()
        return WorldMap(init_map=frozendict({key:frozendict(val) for key, val in new_map.items()}))

    # utils

    def are_adjacent(self, node: Container, path: Path) -> bool:
        return path.get_id() in self.__world_map[node.get_id()].values()

    def get_paths(self, node: Container) -> list[str]:
        return list(self.__world_map[node.get_id()].values())

    def get_path(self, node: Container, direction: Named) -> str|None:
        if direction.get_name() == "random":
            return random.choice(list(self.__world_map[node.get_id()].values()))
        return self.__world_map[node.get_id()].get(direction.get_id())

class WordTreeNode:
    def __init__(self, value: frozenset[str]|None = None, branches: frozendict[str, 'WordTreeNode']|None = None):
        self.__value : frozenset[str] = value if value is not None else frozenset()
        self.__children : frozendict[str, 'WordTreeNode'] = branches if branches is not None else frozendict()

    def get_rep(self, previous: str) -> str:
        rep = f"{previous}: {set(self.__value)}"
        for word, child in self.__children.items():
            rep += f"\n{child.get_rep(previous + " " + word)}"
        return rep

    def add(self, words: list[str], value: Named) -> 'WordTreeNode':
        if len(words) == 0:
            return WordTreeNode(self.__value.union([value.get_id()]), self.__children)
        if words[0] in self.__children:
            updated_child = self.__children[words[0]].add(words[1:], value)
            return WordTreeNode(self.__value, self.__children | {words[0]: updated_child})
        return WordTreeNode(self.__value, self.__children | {words[0]: WordTreeNode().add(words[1:], value)})

    def get_exactly(self, words: list[str]) -> list[str]:
        if len(words) == 0:
            return list(self.__value)
        return self.__children[words[0]].get_exactly(words[1:])

    def get_possible(self, words: list[str], used_words: list[str] = None) -> list[tuple[str, list[str], list[str]]]:
        if used_words is None:
            used_words : list[str] = []
        if len(words) == 0:
            return [(value, used_words, []) for value in self.__value]
        current = [(value, used_words, words) for value in self.__value]
        if words[0] in self.__children:
            current.extend(self.__children[words[0]].get_possible(words[1:], used_words+[words[0]]))
        return current

    def all(self) -> list[str]:
        result = list(self.__value)
        for child in self.__children.values():
            result.extend(child.all())
        return result

class NameFinder:
    def __init__(self, by_name: frozendict[str, WordTreeNode]|None = None, by_id: frozendict[str, Named]|None = None):
        self.__by_name : frozendict[str, WordTreeNode] = by_name if by_name is not None else frozendict()
        self.__by_id : frozendict[str, Named] = by_id if by_id is not None else frozendict()

    def __repr__(self) -> str:
        rep = ""
        for category, tree in self.__by_name.items():
            rep += f"\n{category}:\n{tree.get_rep("\t")}"
        return rep

    def add(self, named: Named, *, category: str|None = None) -> tuple[bool, 'NameFinder']:
        if named.get_id() in self.__by_id:
            logger.debug('%s %s already exists', _category(named), named.get_id())
            return False, self
        new_id = self.__by_id | {named.get_id(): named}
        if not category:
            category = _category(named)
        logger.debug('%s %s', category, named.get_id())
        category_tree = self.__by_name.get(category, WordTreeNode())
        for name in named.get_aliases():
            name = name.lower().split(" ")
            category_tree = category_tree.add(name, named)
        return True, NameFinder(self.__by_name | {category: category_tree}, new_id)

    def add_many(self, to_add: list[Named], *, category:str|None=None) -> tuple[list[bool], 'NameFinder']:
        new_finder = self
        added : list[bool] = []
        for named in to_add:
            success, new_finder = new_finder.add(named, category=category)
            added.append(success)
        return added, new_finder

    def get_from_name(self, name: str = None, category: str|list[str] = None, items: ItemTree = None) -> list[Named]:
        matches : set[str] = set()
        if isinstance(category, str):
            category = category.lower()
            if category in self.__by_name:
                if name is None:
                    matches.update(set(self.__by_name[category].all()))
                else:
                    name = name.lower().split(" ")
                    matches.update(set(self.__by_name[category].get_exactly(name)))
        elif isinstance(category, list):
            for cat in category:
                cat = cat.lower()
                if cat in self.__by_name:
                    if name is None:
                        matches.update(set(self.__by_name[cat].all()))
                    else:
                        name = name.lower().split(" ")
                        matches.update(set(self.__by_name[cat].get_exactly(name)))
        else: # category is None
            for cat, cat_vals in self.__by_name.items():
                if name is None:
                    matches.update(set(cat_vals.all()))
                else:
                    name = name.lower().split(" ")
                    matches.update(set(cat_vals.get_exactly(name)))
        match_list : list[Named] = [self.__by_id[match] for match in matches]
        if items is not None:
            match_list = [match for match in match_list if isinstance(match, (HasLocation, Container)) and items.contains(match)]
        return match_list

    def get_from_id(self, name_id: str, category: str|list[str] = None) -> Named:
        name_id = name_id.lower()
        if name_id in self.__by_id:
            if category is None or \
            (isinstance(category, str)  and _category(self.__by_id[name_id]) == category.lower()) or \
            (isinstance(category, list) and _category(self.__by_id[name_id]) in [cat.lower() for cat in category]):
                return self.__by_id[name_id]
        raise ValueError(f"\"{name_id}\" not found in category {category}")

    def contains(self, named: Named) -> bool:
        return named.get_id() in self.__by_id

    def get_from_input(self, inputs: list[str], category: str|list[str]=None, items: list[ItemTree]|None=None) -> list[tuple[Named,list[str],list[str]]]:
        matches : list[tuple[str,list[str],list[str]]] = []
        inputs = [input.lower() for input in inputs]
        if category is None:
            for cat, cat_vals in self.__by_name.items():
                matches.extend(cat_vals.get_possible(inputs))
        elif isinstance(category, str):
            category = category.lower()
            if category in self.__by_name:
                matches.extend(self.__by_name[category].get_possible(inputs))
        elif isinstance(category, list):
            for cat in category:
                cat = cat.lower()
                matches.extend(self.__by_name[cat].get_possible(inputs))
        else:
            raise RuntimeError()
        match_list  = [(self.__by_id[match], used, leftover) for match, used, leftover in matches]
        if items is not None:
            new_order = []
            for tree in items:
                new_found = [
                    (match,used,leftover) for match,used,leftover in match_list if isinstance(match, (HasLocation,Container)) and tree.contains(match)
                ]
                new_order.extend(new_found)
                for found in new_found:
                    match_list.remove(found)
            new_order.extend(match_list)
            match_list = new_order
        return match_list

    def update(self, named: Named) -> bool:
        return NameFinder(self.__by_name, self.__by_id | {named.get_id(): named})

    def update_many(self, names: list[Named]) -> bool:
        return NameFinder(self.__by_name, self.__by_id | {named.get_id(): named for named in names})
