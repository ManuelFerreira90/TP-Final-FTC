class MooreMachine:
    def __init__(self, states, transitions, initial_state, outputs):
        self.states = states
        self.transitions = transitions
        self.current_state = initial_state
        self.initial_state = initial_state
        self.outputs = outputs
        self.output_log = [" "]
        self.states_passed = [initial_state]

    def process_input(self, input_char):
        """
        Processa um único símbolo de entrada e realiza a transição de estado correspondente.
        """
        if self.current_state in self.transitions:
            for (next_state, char, output) in self.transitions[self.current_state]:
                if char == input_char:
                    # Transição para o próximo estado
                    self.current_state = next_state
                    self.states_passed.append(self.current_state)
                    print(f"Entrada: {input_char}, Saída: {output}")
                    self.output_log.append(output)
                    return output
        
        print(f"Erro: Transição inválida ou estado não encontrado para a entrada '{input_char}'.")
        return None

    def reset(self):
        """
        Reseta a máquina ao estado inicial.
        """
        self.states_passed = [self.initial_state]
        self.current_state = self.initial_state

def load_moore_machine_from_file(filename):
    """
    Carrega a configuração da máquina de Moore a partir de um arquivo.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

    states_line = lines[0].strip().split(': ')[1].split()
    initial_state = lines[1].strip().split(': ')[1]

    transitions = {}
    outputs = {}

    for line in lines[2:]:
        if not line.strip() or line.strip() == "---":
            continue
        
        parts = line.strip().split(' | ')
        state_transition = parts[0].split(' -> ')
        char = parts[1].strip()
        output = parts[2].strip()

        current_state, next_state = state_transition[0], state_transition[1]
        
        if current_state not in transitions:
            transitions[current_state] = []
        transitions[current_state].append((next_state, char, output))

        outputs[next_state] = output

    return MooreMachine(states_line, transitions, initial_state, outputs)
