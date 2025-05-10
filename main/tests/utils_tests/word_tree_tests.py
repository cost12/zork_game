import pytest

from utils.relator import WordTree

@pytest.fixture
def a():
    pass

def test_add():
    word_tree = WordTree[int]()
    word_tree.add(["hello"], 1)
    word_tree.add(["hello", 'world'], 2)
    word_tree.add(['a','b','c','d'], 3)
    word_tree.add(['hello', 'world'], 4)

    assert word_tree.get_exactly(["hello"])[0] == 1
    hello_world = word_tree.get_exactly(['hello','world'])
    hello_world.sort()
    assert hello_world == [2,4]
    assert word_tree.get_exactly(['a','b','c','d'])[0] == 3

def test_get_possible():
    word_tree = WordTree[int]()

    assert word_tree.get_possible(['a']) == []

    word_tree.add(['a','b','c','d'], 1)
    word_tree.add(['a','b','x','y'], 2)
    word_tree.add(['x','y','z'],     3)
    word_tree.add(['a','b'],         4)
    
    assert word_tree.get_possible(['a','b']) == [(4, ['a','b'], [])]
    assert word_tree.get_possible(['a','b','x','y','z']) == [(4, ['a','b'], ['x','y','z']), (2, ['a','b','x','y'], ['z'])]
    assert word_tree.get_possible(['a'])     == []