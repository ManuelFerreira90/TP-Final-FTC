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
            'b': 'Sangue de Basilisco - Letal se unido em cinzas de Fênix (c). Fora isso fortalece o efeito das poções',
            'c': 'Cinzas de Fênix - Revitalização e renascimento. Dá à poção propriedades de cura extrema.Só pode ser combinada com ingredientes neutros como água (a); misturar com escama de dragão (d) cancela seus efeitos. ',
            'm': 'Raiz de Mandrágora - Essencial em poções de cura, revitalizando quem a consome. Deve ser combinada com pétalas (p) ou água (a) para funcionar corretamente; misturar com óleo (o) causa um efeito tóxico.',
            'v': 'Vapor de Vulcão - Aumenta a temperatura da poção, intensificando seus efeitos. Restrições: Não pode ser misturado com água (a), se não...KABOOM.',
            'd': 'Escama de Dragão - Dá à poção um efeito protetor, tornando-a útil em poções de defesa. Não pode ser misturada com ingredientes frágeis como pétalas (p), a delicadeza as suaviza e as deixa inúteis.',
            'e': 'Poeira de Estrela - Sabe seu desejo que nunca se realizou? A sua estrela cadente foi refinada em poeira, tornando as poções mais potentes com sua mágica. Deve ser o último ingrediente adicionado; caso contrário, a poção falha, resultando em um estado de erro (e uma supernova).'
        }

        # Divisão em 2 colunas
        self.grid_columnconfigure(0, weight=1)  # Coluna esquerda
        self.grid_columnconfigure(1, weight=2)  # Coluna direita
        self.grid_rowconfigure(0, weight=1)

        # Terminal do Linux (lado esquerdo)
        self.terminal = tk.Text(self, bg="black", fg="white", font=("Courier", 12), width=40, height=20)
        self.terminal.grid(row=0, column=0, sticky="nsew")

        # Imagem do ingrediente (lado direito)
        self.ingredient_image_label = tk.Label(self)
        self.ingredient_image_label.grid(row=0, column=1, sticky="nsew")

        # Widget para descrição do ingrediente
        self.description_text = tk.Text(self, wrap=tk.WORD, font=("Arial", 14), height=10, width=25, bg="lightyellow", state=tk.DISABLED)
        self.description_text.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Campo de entrada para símbolo do ingrediente
        self.ingredient_entry = tk.Entry(self, font=("Arial", 14))
        self.ingredient_entry.grid(row=2, column=0, columnspan=2, pady=10)

        # Botão para adicionar ingrediente
        self.add_button = tk.Button(self, text="Adicionar Ingrediente", command=self.add_ingredient)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Botão para finalizar a poção
        self.finish_button = tk.Button(self, text="Finalizar Poção", command=self.finalize_potion)
        self.finish_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Botão para resetar a simulação
        self.reset_button = tk.Button(self, text="Resetar", command=self.reset_simulation)
        self.reset_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Carregar AFD
        self.afd = load_afd_from_file('afd_inpunt1.txt')
        self.ingredients_sequence = []  # Lista para armazenar a sequência de ingredientes

        # Adiciona a animação do Doom Guy
        self.doom_guy_situation = 0  # Começa com o Doom Guy em um estado normal
        self.doom_guy_state = 1  # Começa na face do meio
        self.doom_guy_faces_swapped = 0
        self.load_doom_guy_image()
        self.animate_doom_guy()

    def load_doom_guy_image(self):
        # Paths for the images
        doom_guy_path = "imagens/doom_guy/doom_guy_calm.png"
        cover_path = "imagens/doom_guy/doom_guy_inventory_cover.png"

        if os.path.exists(doom_guy_path) and os.path.exists(cover_path):
            # Load Doom Guy image and convert to RGBA for transparency support
            doom_guy_image = Image.open(doom_guy_path).convert("RGBA")

            # Load the cover image
            cover_image = Image.open(cover_path).convert("RGBA")

            # Get dimensions of the Doom Guy image (assumes all faces have the same size)
            face_width = 60
            face_height = doom_guy_image.height

            # Ensure cover image is in the same dimensions
            cover_image = cover_image.crop((0, 0, face_width, face_height))

            # Create a transparent background with the same size as the Doom Guy face
            background = Image.new('RGBA', (face_width, face_height), (0, 0, 0, 0))

            # Composite the cover image onto the background
            background.paste(cover_image, (0, 0), cover_image)

            # Create Doom Guy face images by compositing the animated faces on top of the background
            self.doom_guy_faces = [
                ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((0, 0, face_width, face_height)))),
                ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((face_width, 0, 2 * face_width, face_height)))),
                ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((2 * face_width, 0, 3 * face_width, face_height))))
            ]

            # Create a label for the Doom Guy face and place it in the bottom right corner
            self.doom_guy_label = tk.Label(self, image=self.doom_guy_faces[self.doom_guy_state])
            self.doom_guy_label.place(relx=1.0, rely=1.0, anchor="se")  # Place in the bottom right corner

    def animate_doom_guy(self):
        if self.doom_guy_situation == 0:
            # Alterna entre os estados
            self.doom_guy_faces_swapped += 1
            if self.doom_guy_faces_swapped > 10:
                self.doom_guy_state = 1
                self.doom_guy_faces_swapped = 0
            else:
                if self.doom_guy_state == 0:
                    self.doom_guy_state = 2
                else:
                    self.doom_guy_state = 0
        self.doom_guy_label.config(image=self.doom_guy_faces[self.doom_guy_state])
        self.after(500, self.animate_doom_guy)

    def add_ingredient(self):
        ingredient = self.ingredient_entry.get().strip().lower()

        if ingredient in self.ingredient_descriptions:
            self.ingredients_sequence.append(ingredient)
            self.terminal.insert(tk.END, f"Iniciando a poção com o ingrediente: {ingredient}\n")

            # Atualizar imagem e descrição do ingrediente
            self.update_ingredient_image_and_description(ingredient)

            self.afd.reset()
            self.afd.process_input(ingredient)

            ##if self.afd.is_accepted():
              ##  self.terminal.insert(tk.END, f"Ingrediente {ingredient} aceito na sequência.\n")
            ##else:
              ##  self.terminal.insert(tk.END, f"Ingrediente {ingredient} não aceito na sequência.\n")
        else:
            messagebox.showerror("Erro", "Ingrediente inválido. Por favor, insira um ingrediente válido.")
        self.ingredient_entry.delete(0, tk.END)

    def update_ingredient_image_and_description(self, ingredient):
        # Atualizar a imagem do ingrediente
        image_path = f"imagens/ingredientes/{ingredient}.jpg"
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((200, 200))  # Ajusta o tamanho da imagem
            self.ingredient_image_label.image = ImageTk.PhotoImage(image)
            self.ingredient_image_label.config(image=self.ingredient_image_label.image)
        else:
            self.ingredient_image_label.config(image='')  # Limpa a imagem se não encontrada

        # Atualizar a descrição do ingrediente
        description = self.ingredient_descriptions.get(ingredient, "")
        self.description_text.config(state=tk.NORMAL)
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(tk.END, description)
        self.description_text.config(state=tk.DISABLED)

    def finalize_potion(self):
        # Simula o processo de finalização da poção
        self.terminal.insert(tk.END, "Finalizando a poção...\n")
        self.terminal.insert(tk.END, f"Sequência final dos ingredientes: {''.join(self.ingredients_sequence)}\n")
        self.terminal.insert(tk.END, "Poção finalizada com sucesso!\n")

        # Atualizar a animação do Doom Guy
        self.doom_guy_situation = 1

    def reset_simulation(self):
        # Reseta a simulação
        self.terminal.delete(1.0, tk.END)
        self.ingredients_sequence = []
        self.afd.reset()
        self.update_ingredient_image_and_description('')
        self.doom_guy_situation = 0  # Reseta o estado da animação

if __name__ == "__main__":
    app = IngredientSimulator()
    app.mainloop()
