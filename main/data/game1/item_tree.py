import logging

from models.actors import ItemTree
from utils.relator import NameFinder

logger = logging.getLogger(__name__)

def get_item_tree(name_space:NameFinder):
    item_tree = ItemTree()

    items = [
        ('rack', 'locationdetail', 'armory', 'location'),
        ('spear', 'target', 'rack', 'locationdetail'),
        ('pitchfork', 'target', 'rack', 'locationdetail'),
        ('sword', 'target', 'rack', 'locationdetail'),
        ('table', 'locationdetail', 'attic', 'location'),
        ('leaflet', 'target', 'table', 'locationdetail'),
        ('hourglass', 'target', 'table', 'locationdetail'),
        ('yellow book', 'target', 'table', 'locationdetail'),
        ('lantern', 'target', 'table', 'locationdetail'),
        ('spear rack', 'locationdetail', 'barn', 'location'),
        ('pitchfork rack', 'locationdetail', 'barn', 'location'),
        ('rubber ducky', 'target', 'spear rack', 'locationdetail'),
        ('warm boots', 'target', 'pitchfork rack'),
        ('toilet', 'locationdetail', 'bathroom', 'location'),
        ('vermilion book', 'target', 'tiolet', 'locationdetail'),
        ('shower', 'target', 'bathroom', 'location'),
        ('sink', 'target', 'bathroom', 'location'),
        ('bear', 'actor', 'bears den', 'location'),
        ('bedside', 'locationdetail', 'bedroom', 'location'),
        ('mug', 'target', 'bedside', 'locationdetail'),
        ('brown book', 'target', 'bedside', 'locationdetail'),
        ('player1', 'actor', 'bedroom', 'location'),
        ('beehive', 'locationdetail', 'beehive room', 'location'),
        ('honey', 'target', 'beehive', 'locationdetail'),
        ('floor', 'locationdetail', 'candlelit room', 'location'),
        ('beeswax candle', 'target', 'floor', 'locationdetail'),
        ('small candle', 'target', 'floor', 'locationdetail'),
        ('square candle', 'target', 'floor', 'locationdetail'),
        ('squat candle', 'target', 'floor', 'locationdetail'),
        ('thin candle', 'target', 'floor', 'locationdetail'),
        ('trunk', 'target', 'cellar', 'location'),
        ('seated', 'locationdetail', 'coach car', 'location'),
        ('child', 'actor', 'seated', 'locationdetail'),
        ('trunk', 'target', 'cold room', 'location'),
        ('dashboard', 'locationdetail', "conductor's car", 'location'),
        ('burgundy book', 'target', 'dashboard', 'locationdetail'),
        ('couch', 'locationdetail', 'den', 'location'),
        ('red book', 'target', 'couch', 'locationdetail'),
        ('wool hat', 'target', 'couch', 'locationdetail'),
        ('counter', 'locationdetail', 'dining car', 'location'),
        ('gray book', 'target', 'counter', 'locationdetail'),
        ('table2', 'locationdetail', 'dining room', 'location'),
        ('plate', 'target', 'table2', 'locationdetail'),
        ('cushion', 'locationdetail', 'display room', 'location'),
        ('wallet', 'target', 'cushion', 'locationdetail'),
        ('mirror', 'locationdetail', "driver's seat", 'locaiton'),
        ('sunglasses', 'target', 'mirror', 'locationdetail'),
        ('ground', 'locationdetail', 'garden', 'location'),
        ('thick gloves', 'target', 'ground', 'locationdetail'),
        ('trowel', 'target', 'ground', 'locationdetail'),
        ('wall', 'locationdetail', 'greenhouse', 'location'),
        ('dried herbs', 'target', 'wall', 'locationdetail'),
        ('rack2', 'locationdetail', 'gym', 'location'),
        ('weights', 'target', 'rack2', 'locationdetail'),
        ('cabinet', 'target', 'kitchen', 'location'),
        ('stove', 'target', 'kitchen', 'location'),
        ('kitchen sink', 'target', 'kitchen', 'location'),
        ('shelf 3', 'locationdetail', 'library', 'location'),
        ('shelf 4', 'locationdetail', 'library', 'location'),
        ('shelf 5', 'locationdetail', 'library', 'location'),
        ('shelf 6', 'locationdetail', 'library', 'location'),
        ('shelf 7', 'locationdetail', 'library', 'location'),
        ('shelf 8', 'locationdetail', 'library', 'location'),
        ('shelf 9', 'locationdetail', 'library', 'location'),
        ('bully', 'actor', 'man cave', 'location'),
        ('museum wall', 'locationdetail', 'museum gallery', 'location'),
        ('hercules', 'target', 'museum wall', 'locationdetail'),
        ('desk', 'locationdetail', 'office', 'location'),
        ('emerald book', 'target', 'desk', 'locationdetail'),
        ('magnifying glass', 'target', 'desk', 'locationdetail'),
        ('orge', 'actor', 'orge lair', 'location'),
        ('in trunk', 'locationdetail', 'parking lot', 'location'),
        ('fuzzy jacket', 'target', 'in trunk', 'locationdetail'),
        ('puzzle room table', 'locationdetail', 'puzzle room', 'location'),
        ('puzzle', 'target', 'puzzle room table', 'locationdetail'),
        ('in seat', 'locationdetail', 'theatre seats', 'location'),
        ('keys', 'target', 'in seat', 'locationdetail'),
        ('stage', 'locationdetail', 'theatre stage', 'location'),
        ('lyre', 'target', 'stage', 'locationdetail'),
        ('triangle', 'target', 'stage', 'locationdetail'),
        ('slide whistle', 'target', 'stage', 'locationdetail'),
        ('bongo', 'target', 'stage', 'locationdetail'),
        ('violin', 'target', 'stage', 'locationdetail'),
        ('stand', 'locationdetail', 'theatre stage', 'location'),
        ('baton', 'target', 'stand', 'locationdetail'),
        ('note', 'target', 'stand', 'locationdetail'),
    ]

    for room in name_space.get_from_name(category='location'):
        item_tree.add_room(room)
    for path in name_space.get_from_name(category='path'):
        item_tree.add_path(path)

    for item in items:
        match item[1]:
            case 'locationdetail':
                item_tree.add_location_detail(name_space.get_from_id(item[0], item[1]), name_space.get_from_id(item[2], item[3]))
            case 'target':
                item_tree.add_item(name_space.get_from_id(item[0], item[1]), name_space.get_from_id(item[2], item[3]))
            case 'actor':
                item_tree.add_character(name_space.get_from_id(item[0], item[1]), name_space.get_from_id(item[2], item[3]))
            case _:
                logger.debug('Unknown item type %s in building ItemTree', item[1])

    return item_tree
