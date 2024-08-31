class MT:
    def __init__(self, states, transitions, initial_state, final_states, blank_symbol, error_state):
        self.states = states
        self.transitions = transitions
        self.initial_state = initial_state
        self.current_state = self.initial_state
        self.final_states = final_states
        self.blank_symbol = blank_symbol
        self.error_state = error_state
        self.tape = []
        self.tape_states = []
        self.head_position = 0
        self.states_passed = []

    def initialize_tape(self, input_string):
        self.tape = list(input_string) + [self.blank_symbol]
        self.tape_states.append(self.tape.copy())
        self.head_position = 0
        self.states_passed = [self.current_state]
        

    def process_input(self):
        while self.current_state not in self.final_states and self.current_state != self.error_state:
            current_symbol = self.tape[self.head_position]
           
            
            # Verifica as transições com base no estado e símbolo atuais
            for (state_symbol, input_symbol), (next_state, write_symbol, move_direction) in self.transitions.items():
                state, symbol = state_symbol.split()  # Divide 'state symbol' em 'state' e 'symbol'
                if state == self.current_state and symbol == current_symbol:
                    # Encontrou a transição
                    self.tape[self.head_position] = write_symbol
                    self.current_state = next_state
                    self.states_passed.append(self.current_state)
                    
                   

                    
                    # Atualiza a posição da cabeça
                    self.head_position += 1 if move_direction == 'R' else -1

                    # Ajusta a fita caso necessário
                    if self.head_position < 0:
                        self.tape.insert(0, self.blank_symbol)
                        self.head_position = 0
                    elif self.head_position >= len(self.tape):
                        self.tape.append(self.blank_symbol)
                    self.tape_states.append(self.tape.copy())
                    print("aaaaa",self.tape_states)
                    break
                    
                
            else:
                # Se nenhuma transição foi encontrada, define o estado de erro
                self.current_state = self.error_state
                self.states_passed.append(self.current_state)
            
    def is_accepted(self):  
        return self.current_state in self.final_states

    def is_rejected(self):
        return self.current_state == self.error_state

    def reset(self):
        self.current_state = self.initial_state
        self.head_position = 0
        self.states_passed = []
        self.tape = []
        self.tape_states = []

def load_mt_from_file(filename):
    states = set()
    transitions = {}
    initial_state = None
    final_states = set()
    blank_symbol = None
    error_state = None

    with open(filename, 'r') as file:
        lines = file.readlines()

    # Processar os estados
    states_line = lines[0].strip()
    if not states_line.startswith('Q:'):
        raise ValueError("Primeira linha deve começar com 'Q:'")
    states = set(states_line.split(': ')[1].split())

    # Processar o estado inicial
    initial_state_line = lines[1].strip()
    if not initial_state_line.startswith('I:'):
        raise ValueError("Segunda linha deve começar com 'I:'")
    initial_state = initial_state_line.split(': ')[1]

    # Processar estados finais
    final_states_line = lines[2].strip()
    if not final_states_line.startswith('F:'):
        raise ValueError("Terceira linha deve começar com 'F:'")
    final_states = set(final_states_line.split(': ')[1].split())

    # Processar o símbolo branco
    blank_symbol_line = lines[3].strip()
    if not blank_symbol_line.startswith('B:'):
        raise ValueError("Quarta linha deve começar com 'B:'")
    blank_symbol = blank_symbol_line.split(': ')[1]

    # Identificar o estado de erro
    error_states_line = lines[4].strip()
    if not error_states_line.startswith('E:'):
        raise ValueError("Quinta linha deve começar com 'E:'")
    error_states = set(error_states_line.split(': ')[1].split())
    if error_states:
        error_state = next(iter(error_states))

    # Processar transições
    for line in lines[5:]:
        line = line.strip()
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
                            # Corrigir o processamento para adicionar corretamente ao dicionário de transições
                            transitions[(state_transition, parts[0].split()[1])] = (next_state, write_symbol, move_direction)
        elif '|' in line:
            parts = line.split('|')
            if len(parts) == 2:
                state_transition = parts[0].strip()
                action_details = parts[1].strip()
                if action_details:
                    action_parts = action_details.split()
                    next_state, write_symbol, move_direction = action_parts
                    init_state, symbol = state_transition.split()
                    transitions[(init_state + " " + symbol, symbol)] = (next_state, write_symbol, move_direction)

    if not error_state:
        raise ValueError("Estado de erro não encontrado")

    return MT(states, transitions, initial_state, final_states, blank_symbol, error_state)