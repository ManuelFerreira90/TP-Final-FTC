import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def ler_afd_arquivo(filename):
    """
    Reads the AFD (Deterministic Finite Automaton) from a file and returns a directed graph (DiGraph).
    
    Parameters:
    - filename: str, the name of the file containing the AFD definition.
    
    Returns:
    - G: NetworkX DiGraph, the graph representation of the AFD.
    """
    G = nx.DiGraph()
    initial_state = None
    final_states = set()

    with open(filename, 'r') as file:
        lines = file.readlines()

    states_line = lines[0].strip()
    if not states_line.startswith('Q:'):
        raise ValueError("Primeira linha deve começar com 'Q:'")

    states = states_line.split()[1:]
    G.add_nodes_from(states)

    initial_state_line = lines[1].strip()
    if not initial_state_line.startswith('I:'):
        raise ValueError("Segunda linha deve começar com 'I:'")

    initial_state = initial_state_line.split()[1]

    # Process final states
    final_states_line = lines[2].strip()
    if not final_states_line.startswith('F:'):
        raise ValueError("Terceira linha deve começar com 'F:'")

    final_states = set(final_states_line.split()[1:])

    # Mark final states in the graph
    for final_state in final_states:
        if final_state in G:
            G.nodes[final_state]['final'] = True
        else:
            print(f"Warning: Estado final {final_state} não encontrado no grafo.")

    # Process transitions
    for line in lines[3:]:
        line = line.strip()
        if '->' in line:
            parts = line.split('->')
            if len(parts) != 2:
                continue

            state_transition, char = parts
            state_transition = state_transition.strip()
            if '|' in char:
                next_state, char = char.split('|')
                next_state = next_state.strip()
                char = char.strip()

                if state_transition and next_state:
                    G.add_edge(state_transition, next_state, label=char)

    return G

def desenhar_grafo_grid(G):
    """
    Draws the AFD graph in a grid layout.
    
    Parameters:
    - G: NetworkX DiGraph, the graph representation of the AFD.
    """
    nodes = list(G.nodes())
    grid_size = int(len(nodes) ** 0.5) + 1

    pos = {node: (i % grid_size, i // grid_size) for i, node in enumerate(nodes)}

    fig_width = max(10, grid_size * 2)  # Increased width
    fig_height = max(8, grid_size * 1.5)  # Increased height
    plt.figure(figsize=(fig_width, fig_height))

    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue',
            font_size=12, font_weight='bold', edge_color='gray', arrows=True, node_shape='o')

    labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=12)  # Increased font size

    final_states = [node for node, data in G.nodes(data=True) if data.get('final', False)]
    nx.draw_networkx_nodes(G, pos, nodelist=final_states, node_color='lightgreen', node_size=3000)
    plt.show()

def animate_with_button(G, transition_states):
    """
    Create an interactive plot of the AFD graph with a "Forward" button to transition states.
    
    Parameters:
    - G: NetworkX DiGraph, the graph representation of the AFD.
    - transition_states: List[str], the ordered states to highlight in red.
    """
    nodes = list(G.nodes())
    grid_size = int(len(nodes) ** 0.5) + 1  # Define the grid size based on the number of nodes

    # Assign positions to nodes in a grid pattern
    pos = {node: (i % grid_size, i // grid_size) for i, node in enumerate(nodes)}

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)  # Adjust layout to make room for the button

    state_index = [0]

    def draw_graph():
        """
        Function to draw the graph with the current highlighted state.
        """
        ax.clear()
        nx.draw(G, pos, ax=ax, with_labels=True, node_size=3000,
                node_color='lightblue', font_size=12, font_weight='bold',
                edge_color='gray', arrows=True, node_shape='o')

        current_state = transition_states[state_index[0] % len(transition_states)]
    

        labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=12, ax=ax)  # Increased font size

        final_states = [node for node, data in G.nodes(data=True) if data.get('final', False)]
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=final_states, node_color='lightgreen', node_size=3000)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[current_state],
                               node_color='red', node_size=3000)
    def forward(event):
        """
        Callback function to advance to the next state when the button is clicked.
        """
        state_index[0] += 1
        draw_graph()
        plt.draw()

    draw_graph()

    ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
    button = Button(ax_button, 'Forward')
    button.on_clicked(forward)

    plt.show()
