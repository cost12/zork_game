import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from datetime import datetime
from collections import deque

from models.action          import Action
from models.actors          import Location
from models.state           import StateGroup, StateGraph
from factories.data_read_in import read_in_game, read_in_actions, read_in_states, read_in_state_graphs, read_in_state_disconnected_graphs
from factories.factories    import LocationFactory

def get_state_graph_edges(graph:dict[StateGroup,dict[Action,StateGroup]]) -> list[tuple[str,str,str]]:
    out_edges = list[tuple[str,str,str]]()
    for node1, edges in graph.items():
        node1_name = f"{node1.name}\n" + ",".join([state.get_name() for state in node1.states])
        for edge, node2 in edges.items():
            node2_name = f"{node2.name}\n" + ",".join([state.get_name() for state in node2.states])
            edge_name = edge.get_name()
            out_edges.append((node1_name,node2_name,edge_name))
    return out_edges

def get_time_graph_edges(graph:dict[StateGroup,tuple[int,StateGroup]]) -> list[tuple[str,str,str]]:
    out_edges = list[tuple[str,str,str]]()
    for node1, edge in graph.items():
        node1_name = f"{node1.name}\n" + ",".join([state.get_name() for state in node1.states])
        weight = str(edge[0])
        node2 = edge[1]
        node2_name = f"{node2.name}\n" + ",".join([state.get_name() for state in node2.states])
        out_edges.append((node1_name,node2_name,weight))
    return out_edges

def get_sdg_edges(state_graphs:list[StateGraph], graph_type:str) -> list[tuple[str,str,str]]:
    match graph_type.lower():
        case 'actor':
            graphs = [graph.actor_graph for graph in state_graphs]
        case 'target':
            graphs = [graph.target_graph for graph in state_graphs]
        case 'tool':
            graphs = [graph.tool_graph for graph in state_graphs]
        case 'time':
            graphs = [graph.time_graph for graph in state_graphs]
    groups = set[StateGroup]()
    for state_graph in graphs:
        for group in state_graph.keys():
            if group in groups:
                print("Warning: Graph will be inaccurate, same StateGroup in multiple StateGraphs")
            groups.add(group)
    combined = {
        state_group:dictionary for state_graph in graphs for state_group, dictionary in state_graph.items()
    }
    if graph_type.lower() == 'time':
        return get_time_graph_edges(combined)
    return get_state_graph_edges(combined)

def get_room_edges(room:Location) -> list[tuple[str,str,str]]:
    out_edges = list[tuple[str,str,str]]()
    visited = set[Location]()
    to_visit = deque[Location]()
    to_visit.append(room)
    while len(to_visit) >0:
        n = to_visit.popleft()
        visited.add(n)
        for direction, path in n.paths.items():
            n2 = path.end
            out_edges.append((n.get_name(), n2.get_name(), direction.get_name()))
            if n2 not in visited:
                to_visit.append(n2)
    return out_edges

def visualize_graph(edges:list[tuple[str,str,str]], ax, title, *, sf:float=1.1, node_font_size:int=5, label_font_size:int=3) -> None:
    G = nx.MultiDiGraph()
    connectionstyle = [f"arc3,rad={r}" for r in [0.15,0.30,0.45,0.60]]
    for u,v,label in edges:
        G.add_edge(u,v,label=label)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color="white", alpha=0)
    nx.draw_networkx_labels(G, pos, font_size=5, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color="grey", connectionstyle=connectionstyle, ax=ax)
    labels = {
        tuple(edge): f"{attrs["label"]}" for *edge, attrs in G.edges(keys=True, data=True)
    }
    nx.draw_networkx_edge_labels(
        G,
        pos,
        labels,
        connectionstyle=connectionstyle,
        label_pos=0.5,
        ax=ax,
        font_size=3
    )
    ax.set_title(title)
    ax.set_xlim([sf*x for x in ax.get_xlim()])
    ax.set_ylim([sf*y for y in ax.get_ylim()])

def visualize_state_graphs(game:str):
    actions = read_in_actions(game)
    states = read_in_states(game, actions)
    state_graphs = read_in_state_graphs(game, states, actions)
    for graph_group in state_graphs.get_state_graphs():
        fig, axes = plt.subplots(2, 2)
        fig.suptitle(f"{graph_group.get_name()} ({datetime.today().date()})")
        axes   = np.ravel(axes)
        graphs = [graph_group.actor_graph, graph_group.target_graph, graph_group.tool_graph, graph_group.time_graph]
        titles = ['Actor', 'Target', 'Tool', 'Time']
        for ax, graph, title in zip(axes, graphs, titles):
            edges = get_state_graph_edges(graph)
            visualize_graph(edges, ax, title)
        plt.savefig(f'main/game_info/{game}/state_graphs/{graph_group.get_name()}.png', dpi=300)

def visualize_sdgs(game:str):
    actions = read_in_actions(game)
    states = read_in_states(game, actions)
    state_graphs = read_in_state_graphs(game, states, actions)
    sdgs = read_in_state_disconnected_graphs(game, state_graphs)
    for graph in sdgs.get_state_disconnected_graphs():
        fig, axes = plt.subplots(2,2)
        fig.suptitle(f"{graph.get_name()} ({datetime.today().date()})")
        axes   = np.ravel(axes)
        titles = ['Actor', 'Target', 'Tool', 'Time']
        for ax, title in zip(axes, titles):
            edges = get_sdg_edges(graph.state_graphs, title)
            visualize_graph(edges, ax, title)
        plt.savefig(f'main/game_info/{game}/sdgs/{graph.get_name()}.png', dpi=300)


def visualize_rooms(game:str, rooms:LocationFactory):
    for room in rooms.get_locations():
        if room.is_start_location():
            edges = get_room_edges(room)
            break
    fig, axes = plt.subplots(1)
    fig.suptitle(f"Rooms ({datetime.today().date()})")
    axes = np.ravel(axes)
    ax = axes[0]
    sf = 1.1
    visualize_graph(edges, ax)
    ax.set_xlim([sf*x for x in ax.get_xlim()])
    ax.set_ylim([sf*y for y in ax.get_ylim()])
    plt.savefig(f'main/game_info/{game}/rooms/rooms.png', dpi=300)

def visualize_game(game:str):
    rooms, characters, controls, items, actions, directions, _ = read_in_game(game)
    #visualize_state_graphs(game)
    visualize_sdgs(game)
    #visualize_rooms(game, rooms)