class APD:
    def __init__(self, states, transitions, initial_state, final_state, error_state):
        self.states = states
        self.transitions = transitions
        self.current_state = initial_state
        self.final_state = final_state
        self.initial_state = initial_state
        self.error_state = error_state
        self.states_passed = [initial_state]
        self.pilha = ['&']
        self.topoDaPilha = 0

    def process_input(self, input_char):
        if self.current_state in self.transitions:
            for (next_state, char, desempilha, empilha) in self.transitions[self.current_state]:
                if char == input_char:
                    if desempilha == self.pilha[self.topoDaPilha] or desempilha == '&':
                        print(self.current_state)
                        self.current_state = next_state
                        self.states_passed.append(self.current_state)

                        if desempilha == self.pilha[self.topoDaPilha] and desempilha != '&':
                            self.pilha.remove(desempilha)
                            self.topoDaPilha -= 1

                        if(empilha != '&'):
                            self.pilha.append(empilha)
                            self.topoDaPilha += 1

                    else:
                        break

                    return
        
        self.current_state = self.error_state
        self.states_passed.append(self.current_state)


    def is_accepted(self):
        return self.current_state == self.final_state

    def is_rejected(self):
        return self.current_state == self.error_state
    


    def reset(self):
        self.states_passed = []
        self.current_state = self.initial_state
        self.pilha = []
        self.topoDaPilha = 0

def load_APD_from_file(filename):
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
        state_transition, char, desempilha, empilha = parts[0].split(' -> '), parts[1].strip(), parts[2].strip(), parts[3].strip()
        current_state, next_state = state_transition[0], state_transition[1]
        if current_state not in transitions:
            transitions[current_state] = []
        transitions[current_state].append((next_state, char, desempilha, empilha))

    error_state = [state for state in states_line if 'erro' in state][0]
    return APD(states_line, transitions,initial_state, final_state, error_state)

# Carregar o AFD a partir do arquivo
apd = load_APD_from_file('apd_imput.txt')

# Interação com o usuário
while True:
    ingrediente = input("Insira o símbolo do ingrediente: ")
    apd.process_input(ingrediente)
    if apd.current_state == apd.error_state:
        break
    continuar = input("Deseja inserir mais um ingrediente (s/n)? ")
    if continuar.lower() != 's':
        break

if apd.is_accepted():
    print("Poção criada com sucesso!")
else:
    print("Erro na mistura")
