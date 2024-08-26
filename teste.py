import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class Automato:
    def __init__(self, config_file):
        self.states = {}
        self.transitions = {}
        self.initial_state = None
        self.final_state = None
        self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            lines = f.readlines()

        states_line = lines[0].strip().split(':')[1].strip()
        states = states_line.split()
        
        for state in states:
            self.states[state] = []

        self.initial_state = lines[1].strip().split(':')[1].strip()
        self.final_state = lines[2].strip().split(':')[1].strip()

        for line in lines[3:]:
            if line.strip() == '':
                continue
            if '->' in line:
                from_state, rest = line.split('->')
                from_state = from_state.strip()
                to_state, symbols = rest.split('|')
                to_state = to_state.strip()
                symbols = symbols.strip().split()
                self.transitions.setdefault(from_state, []).append((to_state, symbols))

    def process_input(self, inputs):
        current_state = self.initial_state
        output = []
        for symbol in inputs:
            if current_state in self.transitions:
                transition_found = False
                for to_state, symbols in self.transitions[current_state]:
                    if symbol in symbols:
                        output.append(f"Transição: {current_state} -> {to_state} com '{symbol}'")
                        current_state = to_state
                        transition_found = True
                        break
                if not transition_found:
                    output.append(f"Erro: Transição inválida a partir do estado {current_state} com '{symbol}'")
                    current_state = 'erro'
                    break
            else:
                output.append("Erro: Estado não possui transições.")
                current_state = 'erro'
                break

        if current_state == self.final_state:
            output.append(f"Poção criada com sucesso no estado: {current_state}.")
        elif current_state == 'erro':
            output.append("Erro na mistura da poção.")
        else:
            output.append(f"Ainda no estado: {current_state}. Mais ingredientes são necessários.")

        return output

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Poções")
        
        self.automato = None

        # Frame para simular o terminal
        self.terminal_frame = tk.Frame(root)
        self.terminal_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame para mostrar a imagem do ingrediente
        self.image_frame = tk.Frame(root)
        self.image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text_area = tk.Text(self.terminal_frame, height=20, width=50)
        self.text_area.pack(padx=10, pady=10)

        self.ingredient_image = tk.Label(self.image_frame)
        self.ingredient_image.pack(padx=10, pady=10)

        self.load_button = tk.Button(root, text="Carregar Automato", command=self.load_automato)
        self.load_button.pack(pady=10)

        self.input_entry = tk.Entry(root)
        self.input_entry.pack(pady=10)

        self.process_button = tk.Button(root, text="Adicionar Ingrediente", command=self.process_input)
        self.process_button.pack(pady=10)

    def load_automato(self):
        file_path = filedialog.askopenfilename(title="Selecione o arquivo de configuração", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.automato = Automato(file_path)
            messagebox.showinfo("Carregado", "Autômato carregado com sucesso!")

    def process_input(self):
        if self.automato is None:
            messagebox.showwarning("Aviso", "Por favor, carregue um autômato primeiro.")
            return

        input_data = self.input_entry.get().strip()
        if not input_data:
            messagebox.showwarning("Aviso", "Por favor, insira um ingrediente.")
            return

        inputs = input_data.split()
        results = self.automato.process_input(inputs)

        # Atualiza a área de texto do terminal
        self.text_area.delete(1.0, tk.END)
        for result in results:
            self.text_area.insert(tk.END, result + "\n")

        # Atualiza a imagem do ingrediente
        self.update_ingredient_image(input_data)

        self.input_entry.delete(0, tk.END)

    def update_ingredient_image(self, ingredient):
        ingredient_images = {
            'a': 'ingredientes/agua.png',
            'p': 'ingredientes/petalas.jpeg',
            'o': 'ingredientes/oleo.png',
            # Adicione aqui mais ingredientes se necessário
            'f': 'ingredientes/folha.png',
            't': 'ingredientes/terra.png',
            'b': 'ingredientes/broto.png',
            'c': 'ingredientes/charco.png',
        }

        if ingredient in ingredient_images:
            img_path = ingredient_images[ingredient]
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((100, 100), Image.ANTIALIAS)
                img_tk = ImageTk.PhotoImage(img)
                self.ingredient_image.config(image=img_tk)
                self.ingredient_image.image = img_tk
            else:
                self.ingredient_image.config(image="")
                messagebox.showerror("Erro", f"Imagem não encontrada para o ingrediente '{ingredient}'")
        else:
            self.ingredient_image.config(image="")
            messagebox.showerror("Erro", f"Ingrediente '{ingredient}' não reconhecido.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
