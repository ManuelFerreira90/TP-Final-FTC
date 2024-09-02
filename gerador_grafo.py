import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
##Responsável pela geração de grafos

##Lê o arquivo AFD e retorna o grafo
def ler_afd_arquivo(filename):
  
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

    final_states_line = lines[2].strip()
    if not final_states_line.startswith('F:'):
        raise ValueError("Terceira linha deve começar com 'F:'")

    final_states = set(final_states_line.split()[1:])

    for final_state in final_states:
        if final_state in G:
            G.nodes[final_state]['final'] = True
        else:
            print(f"Warning: Estado final {final_state} não encontrado no grafo.")

    for line in lines[3:]:
        line = line.strip()
        if  line == "---":
            break
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

##Lê o arquivo APD e retorna o grafo

def ler_apd_arquivo(filename):
    G = nx.DiGraph()
    initial_state = None
    final_state = None
    error_state = None

    with open(filename, 'r') as file:
        lines = file.readlines()

    states_line = lines[0].strip().split(': ')[1].split()
    G.add_nodes_from(states_line)

    initial_state = lines[1].strip().split(': ')[1]

    final_state = lines[2].strip().split(': ')[1]

    transitions = {}
    for line in lines[3:]:
        if not line.strip():
            continue
        if  line.strip() == "---":
            break
        parts = line.strip().split(' | ')#tira os espacos e colica cada parte separada por "|" em uma posicao do vetor "parts"
        
        current_state, next_state = (parts[0].split()[0],parts[0].split()[2])
        char, desempilha, empilha = parts[1].split()

        label = f"{char}; {desempilha}, {empilha}"
        G.add_edge(current_state, next_state, label=label)

    error_state = [state for state in states_line if 'erro' in state][0]

    G.nodes[final_state]['final'] = True

    return G

##Lê o arquivo MT e retorna o grafo

def ler_mt_arquivo(filename):
    G = nx.DiGraph()
    initial_state = None
    final_states = set()
    blank_symbol = None

    with open(filename, 'r') as file:
        lines = file.readlines()

    states_line = lines[0].strip()
    if not states_line.startswith('Q:'):
        raise ValueError("Primeira linha deve começar com 'Q:'")
    states = states_line.split(': ')[1].split()
    G.add_nodes_from(states)

    initial_state_line = lines[1].strip()
    if not initial_state_line.startswith('I:'):
        raise ValueError("Segunda linha deve começar com 'I:'")
    initial_state = initial_state_line.split(': ')[1]
    
    final_states_line = lines[2].strip()
    if not final_states_line.startswith('F:'):
        raise ValueError("Terceira linha deve começar com 'F:'")
    final_states = set(final_states_line.split(': ')[1].split())

    blank_symbol_line = lines[3].strip()
    if not blank_symbol_line.startswith('B:'):
        raise ValueError("Quarta linha deve começar com 'B:'")
    blank_symbol = blank_symbol_line.split(': ')[1]

    for final_state in final_states:
        if final_state in G:
            G.nodes[final_state]['final'] = True
      #  else:
          #  print(f"Warning: Estado final {final_state} não encontrado no grafo.")

    for line in lines[4:]:
        line = line.strip()
        if  line == "---":
            break
        if '->' in line:
            parts = line.split('->')
            if len(parts) == 2:
                state_transition = parts[0].strip()
                action_details = parts[1].strip()

                if '|' in action_details:
                    next_state_action = action_details.split('|')
                    if len(next_state_action) == 2:
                        next_state = next_state_action[0].strip()
                        action_parts = next_state_action[1].strip().split()

                        if len(action_parts) == 2:
                            write_symbol, move_direction = action_parts
                            label = f"{write_symbol};{move_direction}"
                            
                            if state_transition and next_state:
                                G.add_edge(state_transition, next_state, label=label)
        elif '|' in line:
            parts = line.split('|')
            if len(parts) == 2:
                state_transition = parts[0].strip()
                action_details = parts[1].strip()
                

                
                if action_details:
                    action_parts = action_details.split()
                    
                    next_state,write_symbol, move_direction = action_parts
                    init_state, symbol = state_transition.split()
                    label = f"{symbol};{write_symbol},{move_direction}"
                        
                    if state_transition:
                        G.add_edge(init_state, next_state, label=label)

    return G


##Lê o arquivo Moore e retorna o grafo

def ler_moore_arquivo(filename):

    G = nx.DiGraph()
    initial_state = None
    outputs = {}

    with open(filename, 'r') as file:
        lines = file.readlines()

    states_line = lines[0].strip().split(': ')[1].split()
    G.add_nodes_from(states_line)

    initial_state = lines[1].strip().split(': ')[1]

    transitions = {}
    for line in lines[3:]:
        if not line.strip():
            continue
        if  line.strip() == "---":
            break
        
        parts = line.strip().split(' | ')
        state_transition = parts[0].split(' -> ')
        char, output= parts[1].strip().split()
       

        current_state, next_state = state_transition[0], state_transition[1]
        
        if current_state not in transitions:
            transitions[current_state] = []
        transitions[current_state].append((next_state, char, output))

        label = f"{char}/{output}"
        G.add_edge(current_state, next_state, label=label)

    if initial_state in G:
        G.nodes[initial_state]['initial'] = True

    return G

##Desenha grafo da AFD

def desenhar_grafo_grid_afd(G):

    nodes = list(G.nodes())
    grid_size = int(len(nodes) ** 0.5) + 1

    pos = {node: (i % grid_size, i // grid_size) for i, node in enumerate(nodes)}

    fig_width = max(10, grid_size * 2)  
    fig_height = max(8, grid_size * 1.5)  
    plt.figure(figsize=(fig_width, fig_height))

    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue',
            font_size=12, font_weight='bold', edge_color='gray', arrows=True, node_shape='o')

    labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=12)  

    final_states = [node for node, data in G.nodes(data=True) if data.get('final', False)]
    nx.draw_networkx_nodes(G, pos, nodelist=final_states, node_color='lightgreen', node_size=3000)
    plt.show()

    
##Animação transição AFD

def animate_with_button_afd(G, transition_states):
    nodes = list(G.nodes())
    grid_size = int(len(nodes) ** 0.5) + 1
    pos = {node: (i % grid_size, i // grid_size) for i, node in enumerate(nodes)}

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)
    state_index = [0]

    def draw_graph():
        ax.clear()
        nx.draw(G, pos, ax=ax, with_labels=True, node_size=3000,
                node_color='lightblue', font_size=12, font_weight='bold',
                edge_color='gray', arrows=True, node_shape='o')

        current_state = transition_states[state_index[0] % len(transition_states)]
    
        labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=12, ax=ax)  

        final_states = [node for node, data in G.nodes(data=True) if data.get('final', False)]
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=final_states, node_color='lightgreen', node_size=3000)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[current_state],
                               node_color='red', node_size=3000)

    def forward(event=None):
        state_index[0] += 1
        draw_graph()
        plt.draw()

    def backward(event=None):
        state_index[0] -= 1
        draw_graph()
        plt.draw()

    def on_key(event):
        if event.key == 'right' or event.key == 'enter':
            forward()
        elif event.key == 'left':
            backward()

    draw_graph()

    ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
    button = Button(ax_button, 'Próximo')
    button.on_clicked(forward)

    fig.canvas.mpl_connect('key_press_event', on_key)

    plt.show()


##Desenha grafo da MT

def desenhar_grafo_grid_mt(G):
   # for edge in G.edges():
       # print(edge)
  
    nodes = list(G.nodes())
    grid_size = int(len(nodes) ** 0.5) + 1

    pos = {node: (i % grid_size, i // grid_size) for i, node in enumerate(nodes)}

    fig_width = max(10, grid_size * 2)
    fig_height = max(8, grid_size * 1.5)
    plt.figure(figsize=(fig_width, fig_height))

    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue',
            font_size=12, font_weight='bold', edge_color='gray', arrows=True, node_shape='o')

    labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=12)

    final_states = [node for node, data in G.nodes(data=True) if data.get('final', False)]
    nx.draw_networkx_nodes(G, pos, nodelist=final_states, node_color='lightgreen', node_size=3000)
    #plt.().window.state('zoomed')

    plt.show()

##Desenha grafo da APD


def desenhar_grafo_grid_apd(G):
 
    nodes = list(G.nodes())
    grid_size = int(len(nodes) ** 0.5) + 1

    pos = {node: (i % grid_size, i // grid_size) for i, node in enumerate(nodes)}

    fig_width = max(10, grid_size * 2)
    fig_height = max(8, grid_size * 1.5)
    plt.figure(figsize=(fig_width, fig_height))

    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue',
            font_size=12, font_weight='bold', edge_color='gray', arrows=True, node_shape='o')

    labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=12)

    final_states = [node for node, data in G.nodes(data=True) if data.get('final', False)]
    nx.draw_networkx_nodes(G, pos, nodelist=final_states, node_color='lightgreen', node_size=3000)

    plt.show()

##Animação transição da MT

def animate_with_button_mt(G, transition_states, stack):
    nodes = list(G.nodes())
    grid_size = int(len(nodes) ** 0.5) + 1
    pos = {node: (i % grid_size, i // grid_size) for i, node in enumerate(nodes)}

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)  
    state_index = [0]

    def draw_graph():
        ax.clear()
        nx.draw(G, pos, ax=ax, with_labels=True, node_size=3000,
                node_color='lightblue', font_size=12, font_weight='bold',
                edge_color='gray', arrows=True, node_shape='o')

        current_state = transition_states[state_index[0] % len(transition_states)]
        labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=12, ax=ax)

        final_states = [node for node, data in G.nodes(data=True) if data.get('final', False)]
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=final_states, node_color='lightgreen', node_size=3000)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[current_state], node_color='red', node_size=3000)

        ax.text(0.05, 0.02, f"Pilha: {stack[state_index[0] % len(stack)]}", transform=fig.transFigure,
                fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

    def forward(event=None):
        state_index[0] += 1
        draw_graph()
        plt.draw()

    def backward(event=None):
        state_index[0] -= 1
        draw_graph()
        plt.draw()

    def on_key(event):
        if event.key == 'right' or event.key == 'enter':
            forward()
        elif event.key == 'left':
            backward()

    draw_graph()

    ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
    button = Button(ax_button, 'Próximo')
    button.on_clicked(forward)

    fig.canvas.mpl_connect('key_press_event', on_key)

    plt.show()
    
##Animação transição da APD

def animate_with_button_apd(G, transition_states, stack):
    nodes = list(G.nodes())
    grid_size = int(len(nodes) ** 0.5) + 1
    pos = {node: (i % grid_size, i // grid_size) for i, node in enumerate(nodes)}

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)  
    state_index = [0]

    def draw_graph():
        ax.clear()
        nx.draw(G, pos, ax=ax, with_labels=True, node_size=3000,
                node_color='lightblue', font_size=12, font_weight='bold',
                edge_color='gray', arrows=True, node_shape='o')

        current_state = transition_states[state_index[0] % len(transition_states)]
        labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=12, ax=ax)

        final_states = [node for node, data in G.nodes(data=True) if data.get('final', False)]
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=final_states, node_color='lightgreen', node_size=3000)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[current_state], node_color='red', node_size=3000)

        ax.text(0.05, 0.02, f"Pilha: {stack[state_index[0] % len(stack)]}", transform=fig.transFigure,
                fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

    def forward(event=None):
        state_index[0] += 1
        draw_graph()
        plt.draw()

    def backward(event=None):
        state_index[0] -= 1
        draw_graph()
        plt.draw()

    def on_key(event):
        if event.key == 'right' or event.key == 'enter':
            forward()
        elif event.key == 'left':
            backward()

    draw_graph()

    ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
    button = Button(ax_button, 'Próximo')
    button.on_clicked(forward)

    fig.canvas.mpl_connect('key_press_event', on_key)

    plt.show()

##Desenhar grafo da Moore

def desenhar_grafo_moore(G):
 
    pos = nx.spring_layout(G)
    
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue',
            font_size=12, font_weight='bold', edge_color='gray', arrows=True)

    labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)
    
    initial_states = [node for node, data in G.nodes(data=True) if data.get('initial', False)]
    final_states = [node for node, data in G.nodes(data=True) if data.get('final', False)]
    
    nx.draw_networkx_nodes(G, pos, nodelist=initial_states, node_color='lightgreen', node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=final_states, node_color='red', node_size=3000)

    plt.show()


##Animação transição da Moore
def animate_with_button_moore(G, transition_states, output_symbols):
    nodes = list(G.nodes())
    grid_size = int(len(nodes) ** 0.5) + 1
    pos = {node: (i % grid_size, i // grid_size) for i, node in enumerate(nodes)}

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)  
    state_index = [0]

    def draw_graph():
        ax.clear()
        nx.draw(G, pos, ax=ax, with_labels=True, node_size=3000,
                node_color='lightblue', font_size=12, font_weight='bold',
                edge_color='gray', arrows=True, node_shape='o')

        current_state = transition_states[state_index[0] % len(transition_states)]
        labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=12, ax=ax)

        final_states = [node for node, data in G.nodes(data=True) if data.get('final', False)]
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=final_states, node_color='lightgreen', node_size=3000)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[current_state], node_color='red', node_size=3000)

        ax.text(0.05, 0.02, f"Símbolo de Saída: {output_symbols[state_index[0] % len(output_symbols)]}", 
                transform=fig.transFigure, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

    def forward(event=None):
        state_index[0] += 1
        draw_graph()
        plt.draw()

    def backward(event=None):
        state_index[0] -= 1
        draw_graph()
        plt.draw()

    def on_key(event):
        if event.key == 'right' or event.key == 'enter':
            forward()
        elif event.key == 'left':
            backward()

    draw_graph()

    ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
    button = Button(ax_button, 'Próximo')
    button.on_clicked(forward)

    fig.canvas.mpl_connect('key_press_event', on_key)

    plt.show()