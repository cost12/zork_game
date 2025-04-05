from pyvis.network import Network
from collections import deque
import math

from models.action          import Action
from models.actors          import Location
from models.state           import StateGroup, StateGraph, StateDisconnectedGraph
from factories.data_read_in import read_in_game
from factories.factories    import LocationFactory, ItemFactory

class NodeInfo:
    def __init__(self, *, room:Location=None, state_group:StateGroup=None):
        if room is not None:
            self.__room_init(room)
        elif state_group is not None:
            self.__state_group_init(state_group)
        else:
            raise RuntimeError()

    def __state_group_init(self, state_group:StateGroup):
        self.name = state_group.get_name().lower()
        self.title="Contains:\n\t"    +"\n\t".join([state.get_name() for state in state_group.get_states()])
        self.title+="\nAs actor:\n\t" +"\n\t".join([action.get_name() for action in state_group.get_actions_as_actor()])
        self.title+="\nAs tool:\n\t"  +"\n\t".join([action.get_name() for action in state_group.get_actions_as_tool()])
        self.title+="\nAs target:\n\t"+"\n\t".join([action.get_name() for action in state_group.get_actions_as_target()])
        self.x=None
        self.y=None
        self.edges=list[list[str,str,int]]()

    def __room_init(self, room:Location):
        self.name=room.get_name().lower()
        self.title="Contains:\n"+"\n".join([item.get_name() for item in room.contents])
        self.x=0
        self.y=0
        self.edges=list[list[str,str,int]]()

        for direction, path in room.paths.items():
            for room2 in path._list_ends():
                self.add_edge(direction.get_name(), room2.get_name())

    def open_direction(self) -> str:
        directions = ["north", "south", "east", "west", "southwest", "southeast", "southwest", "northwest", "northeast"]
        for used_direction,_,_ in self.edges:
            if used_direction in directions:
                directions.remove(used_direction)
        if len(directions) > 0:
            return directions[0]
        return None

    def add_edge(self, label:str, end:str) -> None:
        label = label.lower()
        end = end.lower()
        added = False
        for edge in self.edges:
            if edge[0] == label and edge[1] == end:
                edge[2] += 1
                added = True
                break
        if not added:
            self.edges.append([label, end, 1])
    
    def list_edges(self) -> list[list[str,str]]:
        out_list = []
        for edge in self.edges:
            out_list.append([edge[0] if edge[2] == 1 else f"{edge[0]} ({edge[2]})", edge[1]])
        final_list = []
        i = 0
        while i < len(out_list):
            label = f"{out_list[i][0]}"
            j = i + 1
            while j < len(out_list):
                if out_list[i][1] == out_list[j][1]:
                    label += f"/{out_list[j][0]}"
                    out_list.pop(j)
                j += 1
            final_list.append([label,out_list[i][1]])
            i += 1
        return final_list

def update_xy(update_info:NodeInfo, from_info:NodeInfo, direction:str, dist:int):
    match direction:
        case "north":
            update_info.x = from_info.x
            update_info.y = from_info.y - dist
        case "south":
            update_info.x = from_info.x
            update_info.y = from_info.y + dist
        case "east":
            update_info.x = from_info.x + dist
            update_info.y = from_info.y
        case "west":
            update_info.x = from_info.x - dist
            update_info.y = from_info.y
        case "northwest":
            update_info.x = from_info.x - math.sqrt(2)/2*dist
            update_info.y = from_info.y - math.sqrt(2)/2*dist
        case "southwest":
            update_info.x = from_info.x - math.sqrt(2)/2*dist
            update_info.y = from_info.y + math.sqrt(2)/2*dist
        case "southeast":
            update_info.x = from_info.x + math.sqrt(2)/2*dist
            update_info.y = from_info.y + math.sqrt(2)/2*dist
        case "northeast":
            update_info.x = from_info.x + math.sqrt(2)/2*dist
            update_info.y = from_info.y - math.sqrt(2)/2*dist
        case None:
            update_info.x = 500
            update_info.y = 500
        case _:
            return update_xy(update_info, from_info, from_info.open_direction(), dist)

def get_room_nodes(room:Location, dist:int=150) -> list[NodeInfo]:
    out_edges = list[NodeInfo]()
    visited = set[Location]()
    to_visit = deque[Location]()
    node_info = dict[Location,NodeInfo]()
    to_visit.append(room)
    node_info[room] = NodeInfo(room=room)
    out_edges.append(node_info[room])
    while len(to_visit) > 0:
        n = to_visit.popleft()
        visited.add(n)
        for direction, path in n.paths.items():
            for n2 in path._list_ends():
                if n2 not in node_info:
                    info = NodeInfo(room=n2)
                    out_edges.append(info)
                    node_info[n2] = info
                if len(path._list_ends()) == 1:
                    update_xy(node_info[n2], node_info[n], direction.get_name(), dist)
                if n2 not in visited:
                    to_visit.append(n2)
    return out_edges

def get_time_nodes(graph:dict[StateGroup,tuple[int,StateGroup]]) -> list[NodeInfo]:
    nodes = dict[StateGroup,NodeInfo]()
    for sg1, edge in graph.items():
        weight, sg2 = edge
        if sg1 not in nodes:
            nodes[sg1] = NodeInfo(state_group=sg1)
        if sg2 not in nodes:
            nodes[sg2] = NodeInfo(state_group=sg2)
        nodes[sg1].add_edge(f"{weight} turns", nodes[sg2].name)
    return list(nodes.values())

def get_sg_nodes(graph:dict[StateGroup,dict[Action,StateGroup]]) -> list[NodeInfo]:
    nodes = dict[StateGroup,NodeInfo]()
    for sg1, edges in graph.items():
        if sg1 not in nodes:
            nodes[sg1] = NodeInfo(state_group=sg1)
        for edge, sg2 in edges.items():
            if sg2 not in nodes:
                nodes[sg2] = NodeInfo(state_group=sg2)
            edge_name = edge.get_name()
            nodes[sg1].add_edge(edge_name, nodes[sg2].name)
    return list(nodes.values())

def get_state_graph_nodes(state_graph:StateGraph) -> list[NodeInfo]:
    nodes = []
    nodes.extend(get_sg_nodes(state_graph.actor_graph))
    nodes.extend(get_sg_nodes(state_graph.target_graph))
    nodes.extend(get_sg_nodes(state_graph.tool_graph))
    nodes.extend(get_time_nodes(state_graph.time_graph))
    return nodes

def get_sdg_nodes(full_state:StateDisconnectedGraph) -> list[NodeInfo]:
    nodes = []
    for state_graph in full_state.state_graphs:
        nodes.extend(get_state_graph_nodes(state_graph))
    return nodes

def visualize_graph(nodes:list[NodeInfo], save_name:str) -> None:
    nt = Network(directed=True)
    for node in nodes:
        if node.x is None or node.y is None:
            nt.add_node(node.name, node.name, title=node.title)
        else:
            nt.add_node(node.name, node.name, x=node.x, y=node.y, title=node.title)
    for node in nodes:
        for label, end in node.list_edges():
            nt.add_edge(node.name, end, label=label)
    nt.toggle_physics(True)
    nt.show_buttons(filter_=True)
    nt.write_html(f'{save_name}.html', notebook=False)

def visualize_items(game:str, items:ItemFactory):
    for item in items.get_items():
        if item.states is None:
            print(item.get_name())
        nodes = get_sdg_nodes(item.states)
        visualize_graph(nodes, f'main/game_info/{game}/items/{item.get_name()}')

def visualize_rooms(game:str, rooms:LocationFactory):
    for room in rooms.get_locations():
        if room.is_start_location():
            nodes = get_room_nodes(room)
            break
    visualize_graph(nodes, f'main/game_info/{game}/rooms/rooms')

def visualize_game(game:str):
    rooms, characters, controls, items, actions, directions, _ = read_in_game(game)
    visualize_items(game, items)
    visualize_rooms(game, rooms)