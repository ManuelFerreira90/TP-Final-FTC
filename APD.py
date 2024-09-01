class APD:
    def __init__(self, states, transitions, initial_state, final_state, error_state):
        self.states = states
        self.transitions = transitions
        self.current_state = initial_state
        self.final_state = final_state
        self.initial_state = initial_state
        self.error_state = error_state
        self.states_passed = [initial_state]
        self.pilha = []
        self.pilha_states = []
        self.pilha_states.append(self.pilha.copy())
        #self.topoDaPilha = 0

    def process_input(self, input_char):
        if self.current_state in self.transitions:
            for (next_state, char, desempilha, empilha) in self.transitions[self.current_state]:
                if char == input_char:
                    print(empilha)
                    if desempilha ==self.topo() or desempilha == '&':
            
                        self.current_state = next_state
                        self.states_passed.append(self.current_state)

                            #self.pilha.remove(desempilha)
                        if desempilha == self.topo() or desempilha != '&':
                            self.desempilhar()
                            
                            #self.topoDaPilha -= 1

                        if(empilha != '&'):
                            #self.pilha.append(empilha)
                            self.empilhar(empilha)
                            print(self.pilha)
                            #self.pilha_states.append(self.pilha.copy())
                            #self.topoDaPilha += 1
                        
                    else:
                        break

                    return
        
        self.current_state = self.error_state
        self.states_passed.append(self.current_state)

    def empilhar(self, item):
        self.pilha.append(item)
        self.pilha_states.append(self.pilha.copy())


    def desempilhar(self):
        if not self.esta_vazia():
            self.pilha_states.append(self.pilha.copy())
            return self.pilha.pop()
           

    def topo(self):
        if not self.esta_vazia():
            return self.pilha[-1]
        return None

    def esta_vazia(self):
        return len(self.pilha) == 0

    def tamanho(self):
        return len(self.pilha)

    def is_accepted(self):
        return ((self.current_state == self.final_state) and  self.esta_vazia() )

    def is_rejected(self):
        return self.current_state == self.error_state
    


    def reset(self):
        self.states_passed = []
        self.current_state = self.initial_state
        self.pilha = []

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
