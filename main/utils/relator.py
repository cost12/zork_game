from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.actors import HasLocation
    from models.named  import Named

class WordTree[T]:

    def __init__(self):
        self.tree = dict[str,WordTree]()
        self.value = set[T]()

    def add(self, words:list[str], value:T) -> None:
        if len(words) == 0:
            self.value.add(value)
        else:
            first, rest = words[0], words[1:]
            if first not in self.tree:
                self.tree[first] = WordTree()
            self.tree[first].add(rest, value)

    def remove(self, words:list[str]=None, value:T=None) -> None:
        if words is None:
            if value is None: return
            for sub_tree in self.tree.values():
                sub_tree.remove(value=value)
            self.value.remove(value)
        elif value is None:
            if len(words) == 0:
                self.value.clear()
            elif len(words) == 1:
                del self.tree[words[0]]
            else:
                first, rest = words[0], words[1:]
                self.tree[first].remove(rest)
        else:
            if len(words) == 0:
                self.value.remove(value)
            elif len(words) == 1:
                self.tree[words[0]].remove([], value)
                if len(self.tree[words[0]].value) == 0:
                    del self.tree[words[0]]
            else:
                first, rest = words[0], words[1:]
                self.tree[first].remove(rest, value)

    def get_exactly(self, words:list[str]) -> list[T]:
        if len(words) == 0:
            return list(self.value)
        return self.tree[words[0]].get_exactly(words[1:])

    def get_possible(self, words:list[str], used_words:list[str]=None) -> list[tuple[T,list[str],list[str]]]:
        if used_words is None:
            used_words = list[str]()
        if len(words) == 0:
            return [(value, used_words, []) for value in self.value]
        current = [(value, used_words, words) for value in self.value]
        if words[0] in self.tree:
            current.extend(self.tree[words[0]].get_possible(words[1:], used_words+[words[0]]))
        return current
        
    def all(self) -> list[T]:
        result = list(self.value)
        for word, child in self.tree.items():
            result.extend(child.all())
        return result

class NameFinder:
    """Stores Items/Objects/Characters/Actions/ anything in the game namespace for quick access.
    Types of access:
        id - Each object has a unique id
        name/alias - Each object can have multiple names/aliases. These are not unique and may be shared by multiple objects.
        category/location limit - Each object has a category (Item/Character/Action/Room/...) and may have a location (HasLocation). By limiting the scope, fewer items can be returned from the first two types of access.
    """
    def __init__(self):
        self.by_name = dict[str,WordTree['Named']]()
        self.by_id   = dict[str,'Named']()

    def _category(self, named:'Named') -> str:
        return str(type(named)).lower().split(".")[-1][:-2]

    def add(self, named:'Named') -> bool:
        if named.get_id() in self.by_id:
            return False
        self.by_id[named.get_id()] = named
        category = self._category(named)
        if category not in self.by_name:
            self.by_name[category] = WordTree['Named']()
        for name in named.get_aliases():
            name = name.lower().split(" ")
            self.by_name[category].add(name, named)
        return True
    
    def add_many(self, to_add:list['Named']) -> list[bool]:
        return [self.add(named) for named in to_add]
    
    def remove(self, named:'Named') -> bool:
        category = self._category(named)
        if category in self.by_name:
            for name in named.get_aliases():
                name = name.lower().split(" ")
                self.by_name[category].remove(name, named)
        if named.get_id() in self.by_id:
            del self.by_id[named.get_id()]
            return True
        return False

    def get_from_name(self, name:str=None, category:str|list[str]=None, location:'HasLocation'=None) -> list['Named']:
        matches = set['Named']()
        if isinstance(category, str):
            category = category.lower()
            if category in self.by_name:
                if name is None:
                    matches.update(set(self.by_name[category].all()))
                else:
                    name = name.lower().split(" ")
                    matches.update(set(self.by_name[category].get_exactly(name)))
        elif isinstance(category, list):
            for cat in category:
                cat = cat.lower()
                if cat in self.by_name:
                    if name is None:
                        matches.update(set(self.by_name[cat].all()))
                    else:
                        name = name.lower().split(" ")
                        matches.update(set(self.by_name[cat].get_exactly(name)))
        else: # category is None
            for cat in self.by_name.keys():
                if name is None:
                    matches.update(set(self.by_name[cat].all()))
                else:
                    name = name.lower().split(" ")
                    matches.update(set(self.by_name[cat].get_exactly(name)))
        matches = list['Named'](matches)
        if location is not None:
            matches = [match for match in matches if isinstance(match, HasLocation) and match.is_in(location)]
        return matches
    
    def get_from_id(self, id:str, category:str|list[str]=None) -> 'Named':
        id = id.lower()
        if id in self.by_id:
            if category is None or \
            (isinstance(category, str)  and self._category(self.by_id[id]) == category.lower()) or \
            (isinstance(category, list) and self._category(self.by_id[id]) in [cat.lower() for cat in category]):
                return self.by_id[id]
        raise ValueError(f"\"{id}\" not found in category {category}")
    
    def get_from_input(self, inputs:list[str], category:str|list[str]=None, location:'HasLocation'=None) -> list[tuple['Named',list[str],list[str]]]:
        matches = list[tuple['Named',list[str],list[str]]]()
        inputs = [input.lower() for input in inputs]
        if category is None:
            for cat in self.by_name.keys():
                matches.extend(self.by_name[cat].get_possible(inputs))
        elif isinstance(category, str):
            category = category.lower()
            if category in self.by_name:
                matches.extend(self.by_name[category].get_possible(inputs))
        elif isinstance(category, list):
            for cat in category:
                cat = cat.lower()
                matches.extend(self.by_name[cat].get_possible(inputs))
        else:
            raise RuntimeError()
        if location is not None:
            matches = [(match,used,leftover) for match,used,leftover in matches if isinstance(match, HasLocation) and match.is_in(location)]
        return matches