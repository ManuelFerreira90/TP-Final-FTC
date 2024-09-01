class MooreMachine:
    def __init__(self, states, transitions, initial_state, final_state, outputs):
        self.states = states
        self.transitions = transitions
        self.current_state = initial_state
        self.final_state = final_state
        self.initial_state = initial_state
        self.outputs = outputs
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
                    return output
        
        # Se nenhuma transição válida foi encontrada, permanece no estado atual
        print(f"Erro: Transição inválida ou estado não encontrado para a entrada '{input_char}'.")
        return None

    def is_accepted(self):
        """
        Verifica se o estado atual é o estado final.
        """
        return self.current_state == self.final_state

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

    # Primeira linha define os estados da máquina
    states_line = lines[0].strip().split(': ')[1].split()
    initial_state = lines[1].strip().split(': ')[1]
    final_state = lines[2].strip().split(': ')[1]

    transitions = {}
    outputs = {}

    for line in lines[3:]:
        if not line.strip() or line.strip() == "---":
            continue
        
        # Processa a linha de transição
        parts = line.strip().split(' | ')
        state_transition = parts[0].split(' -> ')
        char = parts[1].strip()
        output = parts[2].strip()

        current_state, next_state = state_transition[0], state_transition[1]
        
        if current_state not in transitions:
            transitions[current_state] = []
        transitions[current_state].append((next_state, char, output))

        # Define a saída associada ao estado de destino
        outputs[next_state] = output

    return MooreMachine(states_line, transitions, initial_state, final_state, outputs)

# Exemplo de uso
file_path = './moore_input.txt'  # Nome do arquivo de configuração

# Carrega a máquina de Moore a partir do arquivo
moore_machine = load_moore_machine_from_file(file_path)

# Sequência de entrada de exemplo
input_sequence = ['s', 'a']

# Processa a sequência de entrada
for input_char in input_sequence:
    moore_machine.process_input(input_char)

# Verifica se o estado final foi atingido
if moore_machine.is_accepted():
    print("Receita traduzida com sucesso!")
else:
    print("Falha na tradução da receita.")


"""
DICIONARIO:
w => a: Água - Essencial para a vida.
t => p: Pétalas - Usadas em poções de cura.
i => o: Óleo - Incompatível com água, usado em poções de resistência.
b => b: Sangue de Basilisco - Letal se unido em cinzas de Fênix (c). Fora isso fortalece o efeito das poções.
a => c: Cinzas de Fênix - Revitalização e renascimento. Dá à poção propriedades de cura extrema. Só pode ser combinada com ingredientes neutros como água (a); misturar com escama de dragão (d) cancela seus efeitos.
r => m: Raiz de Mandrágora - Essencial em poções de cura, revitalizando quem a consome. Deve ser combinada com pétalas (p) ou água (a) para funcionar corretamente; misturar com óleo (o) causa um efeito tóxico.
s => v: Vapor de Vulcão - Aumenta a temperatura da poção, intensificando seus efeitos. Restrições Não pode ser misturado com água (a), se não...KABOOM.
c => d: Escama de Dragão - Dá à poção um efeito protetor, tornando-a útil em poções de defesa. Não pode ser misturada com ingredientes frágeis como pétalas (p), a delicadeza as suaviza e as deixa inúteis.
d => e: Poeira de Estrela - Sabe seu desejo que nunca se realizou? A sua estrela cadente foi refinada em poeira, tornando as poções mais potentes com sua mágica. Deve ser o último ingrediente adicionado; caso contrário, a poção falha, resultando em um estado de erro (e uma supernova).
"""