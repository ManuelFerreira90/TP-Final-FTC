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

    def process_input(self, input_char):
        if self.current_state in self.transitions:
            for (next_state, char, desempilha, empilha) in self.transitions[self.current_state]:#obtem as transicoes possiveis a partir do estado atual 
                if char == input_char:
                    if desempilha ==self.topo() or desempilha == '&':#verifica se a transicao e valida
                        self.current_state = next_state
                        self.states_passed.append(self.current_state)

                        if desempilha == self.topo() or desempilha != '&':
                            self.desempilhar()

                        if(empilha != '&'):
                            self.empilhar(empilha)
                        else:
                            self.pilha_states.append(self.pilha.copy())
                    else:#se a transicao nao for valida vai para o estado de erro
                        break

                    return
        
        self.current_state = self.error_state
        self.states_passed.append(self.current_state)

    def empilhar(self, item):
        self.pilha.append(item)
        self.pilha_states.append(self.pilha.copy())


    def desempilhar(self):
        if not self.esta_vazia():
            self.pilha.pop()   
            self.pilha_states.append(self.pilha.copy())
            return      

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
        self.states_passed = [self.initial_state]
        self.pilha = []

def load_APD_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    #as 3 primeiras linhas do arquivo sao estados,estado inicial e estados finais respectivamente
    states_line = lines[0].strip().split(': ')[1].split()
    initial_state = lines[1].strip().split(': ')[1]
    final_state = lines[2].strip().split(': ')[1]

    transitions = {}
    for line in lines[3:]:#obtem as linha a partir da linha 4 do arquivo
        if not line.strip():
            continue
        if  line.strip() == "---":
            break

        parts = line.strip().split(' | ')#tira os espacos e colica cada parte separada por "|" em uma posicao do vetor "parts"
        
        current_state, next_state = (parts[0].split()[0],parts[0].split()[2])
        char, desempilha, empilha = parts[1].split()
    

        if current_state not in transitions:
            transitions[current_state] = []
        transitions[current_state].append((next_state, char, desempilha, empilha))#monta o vetor de trasocao

    error_state = [state for state in states_line if 'erro' in state][0]
    return APD(states_line, transitions,initial_state, final_state, error_state)#cria o APD
