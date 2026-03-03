import logging
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from models.actors import NamedContainer
    from models.named  import Named

logger = logging.getLogger(__name__)

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
            if value is None:
                return
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
                if first in self.tree:
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
        for child in self.tree.values():
            result.extend(child.all())
        return result

T = TypeVar("T", bound="Named")
class NameFinder[T]:
    """Stores Items/Objects/Characters/Actions/ anything in the game namespace for quick access.
    Types of access:
        id - Each object has a unique id
        name/alias - Each object can have multiple names/aliases. These are not unique and may be shared by multiple objects.
        category/location limit - Each object has a category (Item/Character/Action/Room/...) and may have a location (HasLocation). By limiting the scope, fewer items can be returned from the first two types of access.
    """
    def __init__(self):
        self.by_name = dict[str,WordTree[T]]()
        self.by_id   = dict[str,T]()

    def _category(self, named:T) -> str:
        cat = str(type(named)).lower().rsplit(".", maxsplit=1)[-1][:-2]
        if 'action' in cat:
            return 'action'
        return cat

    def add(self, named:'T|Named', *, category:str|None=None) -> bool:
        if named.get_id() in self.by_id:
            logger.debug('%s %s already exists', self._category(named), named.get_id())
            return False
        self.by_id[named.get_id()] = named
        if not category:
            category = self._category(named)
        logger.debug('%s %s', category, named.get_id())
        if category not in self.by_name:
            logger.debug('New category: %s', category)
            self.by_name[category] = WordTree[T]()
        for name in named.get_aliases():
            name = name.lower().split(" ")
            self.by_name[category].add(name, named)
        return True

    def add_many(self, to_add:list[T], *, category:str|None=None) -> list[bool]:
        return [self.add(named, category=category) for named in to_add]

    def remove(self, named:'T|Named') -> bool:
        if named.get_id() in self.by_id:
            del self.by_id[named.get_id()]
        else:
            return False
        category = self._category(named)
        if category in self.by_name:
            for name in named.get_aliases():
                name = name.lower().split(" ")
                self.by_name[category].remove(name, named)
        return True

    def get_from_name(self, name:str=None, category:str|list[str]=None, location:'NamedContainer'=None) -> list[T]:
        matches = set[T]()
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
            for cat, cat_vals in self.by_name.items():
                if name is None:
                    matches.update(set(cat_vals.all()))
                else:
                    name = name.lower().split(" ")
                    matches.update(set(cat_vals.get_exactly(name)))
        matches = list[T](matches)
        if location is not None:
            matches = [match for match in matches if isinstance(match, NamedContainer) and match.is_in(location)]
        return matches

    def get_from_id(self, name_id:str, category:str|list[str]=None) -> T:
        name_id = name_id.lower()
        if name_id in self.by_id:
            if category is None or \
            (isinstance(category, str)  and self._category(self.by_id[name_id]) == category.lower()) or \
            (isinstance(category, list) and self._category(self.by_id[name_id]) in [cat.lower() for cat in category]):
                return self.by_id[name_id]
        raise ValueError(f"\"{name_id}\" not found in category {category}")

    def contains(self, named:'T|Named') -> bool:
        return named.get_id() in self.by_id

    def get_from_input(self, inputs:list[str], category:str|list[str]=None, location:'NamedContainer'=None) -> list[tuple[T,list[str],list[str]]]:
        matches = list[tuple[T,list[str],list[str]]]()
        inputs = [input.lower() for input in inputs]
        if category is None:
            for cat, cat_vals in self.by_name.items():
                matches.extend(cat_vals.get_possible(inputs))
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
            matches = [(match,used,leftover) for match,used,leftover in matches if isinstance(match, NamedContainer) and match.is_in(location)]
        return matches
