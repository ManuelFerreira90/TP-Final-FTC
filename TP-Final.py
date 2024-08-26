class AFD:
    def __init__(self, states, transitions, initial_state, final_state, error_state):
        self.states = states
        self.transitions = transitions
        self.current_state = initial_state
        self.final_state = final_state
        self.error_state = error_state

    def process_input(self, input_char):
        if self.current_state in self.transitions:
            for (next_state, char) in self.transitions[self.current_state]:
                if char == input_char:
                    self.current_state = next_state
                    return
        self.current_state = self.error_state

    def is_accepted(self):
        return self.current_state == self.final_state

    def reset(self):
        self.current_state = "I"

def load_afd_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    states_line = lines[0].strip().split(': ')[1].split()
    initial_state = lines[1].strip().split(': ')[1]
    final_state = lines[2].strip().split(': ')[1]

    transitions = {}
    for line in lines[3:]:
        if not line.strip():
            continue
        parts = line.strip().split(' | ')
        state_transition, char = parts[0].split(' -> '), parts[1].strip()
        current_state, next_state = state_transition[0], state_transition[1]

        if current_state not in transitions:
            transitions[current_state] = []
        transitions[current_state].append((next_state, char))

    error_state = [state for state in states_line if 'erro' in state][0]
    return AFD(states_line, transitions, initial_state, final_state, error_state)

# Carregar o AFD a partir do arquivo
afd = load_afd_from_file('afd_input.txt')

# Interação com o usuário
while True:
    ingrediente = input("Insira o símbolo do ingrediente: ")
    afd.process_input(ingrediente)
    if afd.current_state == afd.error_state:
        break
    continuar = input("Deseja inserir mais um ingrediente (s/n)? ")
    if continuar.lower() != 's':
        break

if afd.is_accepted():
    print("Poção criada com sucesso!")
else:
    print("Erro na mistura")
