import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

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

class IngredientSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Poções")
        self.geometry("800x500")
        
        # Inicializa as descrições dos ingredientes
        self.ingredient_descriptions = {
            'a': 'Água - Essencial para a vida.',
            'p': 'Pétalas - Usadas em poções de cura.',
            'o': 'Óleo - Incompatível com água, usado em poções de resistência.',
            # Adicione outras descrições conforme necessário
        }

        # Divisão em 2 colunas
        self.grid_columnconfigure(0, weight=1)  # Coluna esquerda
        self.grid_columnconfigure(1, weight=2)  # Coluna direita
        self.grid_rowconfigure(0, weight=1)

        # Terminal do Linux (lado esquerdo)
        self.terminal = tk.Text(self, bg="black", fg="white", font=("Courier", 12), width=40, height=20)
        self.terminal.grid(row=0, column=0, sticky="nsew")

        # Imagem do ingrediente (lado direito)
        self.ingredient_image_label = tk.Label(self, font=("Arial", 16))
        self.ingredient_image_label.grid(row=0, column=1, sticky="nsew")

        # Container para a imagem
        self.image_container = tk.Frame(self.ingredient_image_label)
        self.image_container.pack(expand=True)  # Expande para ocupar o espaço disponível

        # Campo de entrada para símbolo do ingrediente
        self.ingredient_entry = tk.Entry(self, font=("Arial", 14))
        self.ingredient_entry.grid(row=1, column=0, columnspan=2, pady=10)

        # Botão para adicionar ingrediente
        self.add_button = tk.Button(self, text="Adicionar Ingrediente", command=self.add_ingredient)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Botão para finalizar a poção
        self.finish_button = tk.Button(self, text="Finalizar Poção", command=self.finalize_potion)
        self.finish_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Botão para resetar a simulação
        self.reset_button = tk.Button(self, text="Resetar", command=self.reset_simulation)
        self.reset_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Carregar AFD
        self.afd = load_afd_from_file('afd_input.txt')
        self.ingredients_sequence = []  # Lista para armazenar a sequência de ingredientes

    def add_ingredient(self):
        ingredient_char = self.ingredient_entry.get().strip()  # Pega a entrada do usuário
        if not ingredient_char:
            messagebox.showerror("Erro", "Por favor, insira um símbolo de ingrediente.")
            return

        self.process_ingredient(ingredient_char)

    def show_ingredient(self, ingredient_char):
        # Limpa a imagem anterior
        for widget in self.image_container.winfo_children():
            widget.destroy()

        if not ingredient_char:
            # Se não houver ingrediente, exibe a imagem de fundo
            img_path = "ingredientes/fundo.png"
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((200, 200), Image.ANTIALIAS)
                img_tk = ImageTk.PhotoImage(img)

                img_label = tk.Label(self.image_container, image=img_tk)
                img_label.image = img_tk  # Referência para evitar que o garbage collector limpe a imagem
                img_label.pack(expand=True)  # Expande para centralizar a imagem
            return

        # Carrega e exibe a imagem do ingrediente correspondente ao símbolo
        img_path = f"ingredientes/{ingredient_char}.jpeg"  # Supondo que as imagens estão na pasta "ingredientes"
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((200, 200), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(img)

            img_label = tk.Label(self.image_container, image=img_tk, text=self.ingredient_descriptions.get(ingredient_char, ""), compound=tk.TOP, font=("Arial", 14))
            img_label.image = img_tk  # Referência para evitar que o garbage collector limpe a imagem
            img_label.pack(expand=True)  # Expande para centralizar a imagem
        else:
            messagebox.showerror("Erro", f"Imagem para o ingrediente '{ingredient_char}' não encontrada.")


    def process_ingredient(self, ingredient_char):
        self.afd.process_input(ingredient_char)
        self.show_ingredient(ingredient_char)  # Mostra a imagem do ingrediente

        self.ingredients_sequence.append(ingredient_char)  # Adiciona o ingrediente à sequência

        self.terminal.insert(tk.END, f"Ingrediente adicionado: {ingredient_char}\n")
        
        self.terminal.see(tk.END)
        self.ingredient_entry.delete(0, tk.END)  # Limpa a entrada após o processamento

    def finalize_potion(self):
        if self.afd.is_accepted():
            self.terminal.insert(tk.END, "Poção criada com sucesso!\n")
        else:
            self.terminal.insert(tk.END, "Erro na mistura! Poção não criada.\n")

        self.terminal.see(tk.END)
        self.afd.reset()  # Reseta o AFD após a finalização da poção
        self.ingredients_sequence.clear()  # Limpa a sequência de ingredientes

    def reset_simulation(self):
        self.afd.reset()  # Reseta o AFD
        self.ingredients_sequence.clear()  # Limpa a sequência de ingredientes
        self.terminal.delete(1.0, tk.END)  # Limpa o terminal
        self.show_ingredient("")  # Limpa a imagem do ingrediente
        self.ingredient_entry.delete(0, tk.END)  # Limpa a entrada de ingredientes

if __name__ == "__main__":
    app = IngredientSimulator()
    app.mainloop()
