import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from gerador_grafo import *
from AFD import *
from APD import *
from MT import * 
class IngredientSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", lambda event: self.attributes('-fullscreen', False))

        self.title("Simulador de Poções")
        self.geometry("800x500")
        self.afd = None
        self.mt = None
        self.apd = None
        self.ingredient_descriptions = self.load_ingredient_descriptions()
        self.ingredients_sequence = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.create_menu()
        self.create_widgets()
        self.doom_guy_situation = 0
        self.doom_guy_state = 1
        self.doom_guy_faces_swapped = 0
        self.load_doom_guy_image()
        self.animate_doom_guy()

    def create_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Carregar", menu=file_menu)
        file_menu.add_command(label="Carregar AFD", command=self.load_afd)
        file_menu.add_command(label="Carregar APD", command=self.load_apd)
        file_menu.add_command(label="Carregar MT", command=self.load_mt)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.quit)

    def create_widgets(self):
        self.terminal = tk.Text(self, bg="black", fg="white", font=("Courier", 12), width=40, height=20)
        self.terminal.grid(row=0, column=0, sticky="nsew")

        self.ingredient_image_label = tk.Label(self)
        self.ingredient_image_label.grid(row=0, column=1, sticky="nsew")

        self.description_text = tk.Text(self, wrap=tk.WORD, font=("Arial", 14), height=10, width=25, bg="lightyellow", state=tk.DISABLED)
        self.description_text.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.ingredient_entry = tk.Entry(self, font=("Arial", 14))
        self.ingredient_entry.grid(row=2, column=0, columnspan=2, pady=10)

        button_width = 20

        self.add_button = tk.Button(self, text="Adicionar Ingrediente", width=button_width, command=self.add_ingredient)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.finish_button = tk.Button(self, text="Finalizar Poção", width=button_width, command=self.finalize_potion)
        self.finish_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.see_graph = tk.Button(self, text="Visualizar Automato", width=button_width, command=self.show_graph)
        self.see_graph.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.reset_button = tk.Button(self, text="Resetar", width=button_width, command=self.reset_simulation)
        self.reset_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.update_buttons_state()

    def load_ingredient_descriptions(self, filename="ingredientes.txt"):
        descriptions = {}
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                key, description = line.strip().split(': ', 1)
                descriptions[key] = description
        return descriptions

    def load_ingredient_image(self, ingredient):
        image_path = f"imagens/ingredientes/{ingredient}.jpg"
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img.thumbnail((200, 200))  # Ajustar o tamanho da imagem, se necessário
            return ImageTk.PhotoImage(img)
        else:
            print(f"Imagem não encontrada para o ingrediente: {ingredient}")
            return None
        
    def change_situation(self,num):
         self.doom_guy_situation = num
         self.load_doom_guy_image()
    def load_doom_guy_image(self):
        if(self.doom_guy_situation == 0):
            doom_guy_path = "imagens/doom_guy/doom_guy_calm.png"
        elif(self.doom_guy_situation == 1):
             doom_guy_path = "imagens/doom_guy/doom_guy_surprised.png"
        elif(self.doom_guy_situation == 2):
              doom_guy_path = "imagens/doom_guy/doom_guy_happy.png"
        elif(self.doom_guy_situation == 3):
              doom_guy_path = "imagens/doom_guy/doom_guy_beaten.png"
        elif(self.doom_guy_situation == 4):
              doom_guy_path = "imagens/doom_guy/doom_guy_god.png"
             
        cover_path = "imagens/doom_guy/doom_guy_inventory_cover.png"

        if os.path.exists(doom_guy_path) and os.path.exists(cover_path):
            doom_guy_image = Image.open(doom_guy_path).convert("RGBA")
            cover_image = Image.open(cover_path).convert("RGBA")

            face_width = 120
            face_height = doom_guy_image.height

            cover_image = cover_image.crop((0, 0, face_width, face_height))
            background = Image.new('RGBA', (face_width, face_height), (0, 0, 0, 0))
            background.paste(cover_image, (0, 0), cover_image)
            if(self.doom_guy_situation != 1):
                self.doom_guy_faces = [
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((0, 0, face_width, face_height)))),
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((face_width, 0, 2 * face_width, face_height)))),
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((2 * face_width, 0, 3 * face_width, face_height))))
                ]

            if(self.doom_guy_situation == 1):
                  self.doom_guy_faces = [
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((0, 0, face_width, face_height)))),
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((0, 0, face_width, face_height)))),
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((0, 0, face_width, face_height))))


                ]
                  
            if(self.doom_guy_situation == 2):
                  self.doom_guy_faces = [
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((0, 0, face_width, face_height)))),
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((face_width, 0, 2 * face_width, face_height)))),
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((0, 0, face_width, face_height))))


                ]
                  
            if(self.doom_guy_situation == 3):
                  self.doom_guy_faces = [
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((0, 0, face_width, face_height)))),
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((0, 0, face_width, face_height)))),
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((face_width, 0, 2 * face_width, face_height)))),


                ]

            if(self.doom_guy_situation == 4):
                  self.doom_guy_faces = [
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((2 * face_width, 0, 3 * face_width, face_height)))),
                    #ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((face_width, 0, 2 * face_width, face_height))))
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((0, 0, face_width, face_height)))),
                    ImageTk.PhotoImage(Image.alpha_composite(background, doom_guy_image.crop((2 * face_width, 0, 3 * face_width, face_height)))),



                ]

                 
            # Inicializando o label do Doom Guy com a primeira face
             
            self.doom_guy_label = tk.Label(self, image=self.doom_guy_faces[self.doom_guy_state])
            self.doom_guy_label.place(relx=1.0, rely=1.0, anchor="se")
        else:
            print("Caminho para as imagens está incorreto ou imagens não encontradas.")

    def animate_doom_guy(self):
     
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
        self.after(700, self.animate_doom_guy)

    def load_afd(self):
        self.reset_simulation()

       


        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.afd = load_afd_from_file(file_path)
            self.update_buttons_state()
            self.Grafo = ler_afd_arquivo(file_path)
            messagebox.showinfo("Sucesso", "Automato carregado com sucesso.")

    def load_apd(self):
        self.reset_simulation()

       
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.apd = load_APD_from_file(file_path)
            self.update_buttons_state()
            self.Grafo = ler_apd_arquivo(file_path)
            messagebox.showinfo("Sucesso", "Automato carregado com sucesso.")

    def load_mt(self):
        self.mt = None
        self.afd = None

        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.mt = load_mt_from_file(file_path)
            self.update_buttons_state()
            self.Grafo = ler_mt_arquivo(file_path)
            messagebox.showinfo("Sucesso", "MT carregado com sucesso.")


    def update_buttons_state(self):
        state = tk.NORMAL if (self.afd or self.mt or self.apd) else tk.DISABLED
        self.add_button.config(state=state)
        self.finish_button.config(state=state)
        self.see_graph.config(state=state)
        self.reset_button.config(state=state)
    def check_ingredients_mt(self,ingredients):
        for ingredient in ingredients:
             if ingredient not in self.ingredient_descriptions:
                  return False
        return True
    def add_ingredient(self):
        if not self.afd and not self.mt and not self.apd:
            messagebox.showerror("Erro", "Automato não carregado.")
            return

        ingredient = self.ingredient_entry.get()
        if ((ingredient in self.ingredient_descriptions and self.afd) or (ingredient in self.ingredient_descriptions and self.apd) or (self.mt and self.check_ingredients_mt(ingredient))):
            self.ingredients_sequence.append(ingredient)
            self.ingredient_entry.delete(0, tk.END)

            self.terminal.insert(tk.END, f"Ingrediente Adicionado: {ingredient}\n")
            self.terminal.see(tk.END)
            if  self.afd:
                self.afd.process_input(ingredient)
            if  self.apd:
                self.apd.process_input(ingredient)
           
           
               
                 

            self.description_text.config(state=tk.NORMAL)
            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(tk.END, self.ingredient_descriptions[ingredient])
            self.description_text.config(state=tk.DISABLED)

            ingredient_image = self.load_ingredient_image(ingredient)
            if ingredient_image:
                    self.ingredient_image_label.config(image=ingredient_image)
                    self.ingredient_image_label.image = ingredient_image
            else:
                    self.ingredient_image_label.config(image='')
          
        else:
            self.terminal.insert(tk.END, f"Ingrediente Desconhecido: {ingredient}\n")
            self.terminal.see(tk.END)

    def finalize_potion(self):
        if(self.afd):
            if(self.afd.is_accepted()):
                ingredientes_total = ""
                for ingredient in self.ingredients_sequence:
                    ingredientes_total += f" - {ingredient}\n"
                self.change_situation(2)
                messagebox.showinfo("Sucesso", f"Poção Finalizada com Ingredientes:\n{ingredientes_total}")
                self.terminal.insert(tk.END, f"Estado Final atingido! \n")
                self.terminal.see(tk.END)
                self.ingredients_sequence.clear()
                self.ingredient_entry.delete(0, tk.END)
                
            elif(self.afd.is_rejected()):
                    self.change_situation(1)
                    messagebox.showerror("Erro", f"O conjunto de ingredientes resultou em um estado de erro!")
                    self.terminal.insert(tk.END, f"Estado de Erro atingido! \n")

            if(self.afd.is_accepted() or self.afd.is_rejected()):
                opcao = messagebox.askyesno("Percorrimento do AFD", ". Gostaria de visualizar o percorrimento do AFD?")
                if(opcao):
                    animate_with_button_afd(self.Grafo, self.afd.states_passed)
                self.reset_simulation()
            else:
                    messagebox.showinfo("Não finalizado", f"O conjunto de ingredientes não resultado em um estado final ou um estado de erro!")
        
        if(self.apd):
            if(self.apd.is_accepted()):
                ingredientes_total = ""
                for ingredient in self.ingredients_sequence:
                    ingredientes_total += f" - {ingredient}\n"
                self.change_situation(2)
                messagebox.showinfo("Sucesso", f"Poção Finalizada com Ingredientes:\n{ingredientes_total}")
                self.terminal.insert(tk.END, f"Estado Final atingido! \n")
                self.terminal.see(tk.END)
                self.ingredients_sequence.clear()
                self.ingredient_entry.delete(0, tk.END)
                
            elif(self.apd.is_rejected()):
                    self.change_situation(1)
                    messagebox.showerror("Erro", f"O conjunto de ingredientes resultou em um estado de erro!")
                    self.terminal.insert(tk.END, f"Estado de Erro atingido! \n")

            if(self.apd.is_accepted() or self.apd.is_rejected()):
              
                opcao = messagebox.askyesno("Percorrimento do APD", ". Gostaria de visualizar o percorrimento do APD?")
                if(opcao):  
                    animate_with_button_apd(self.Grafo, self.apd.states_passed,self.apd.pilha_states)
                self.reset_simulation()
            else:
                    messagebox.showinfo("Não finalizado", f"O conjunto de ingredientes não resultado em um estado final ou um estado de erro!")
        
        
        
        
        if(self.mt):
            self.mt.initialize_tape(self.ingredients_sequence)
            self.mt.process_input()
            if(self.mt.is_accepted()):
                ingredientes_total = ""
                for ingredient in self.ingredients_sequence:
                    ingredientes_total += f" - {ingredient}\n"
                self.change_situation(4)
                messagebox.showinfo("Sucesso", f"Poção Finalizada com Ingredientes:\n{ingredientes_total}")
                self.terminal.insert(tk.END, f"Estado Final atingido! \n")
                self.terminal.see(tk.END)
                self.ingredients_sequence.clear()
                self.ingredient_entry.delete(0, tk.END)
                
            elif(self.mt.is_rejected()):
                    self.change_situation(3)
                    messagebox.showerror("Erro", f"O conjunto de ingredientes resultou em um estado de erro!")
                    self.terminal.insert(tk.END, f"Estado de Erro atingido! \n")

            if(self.mt.is_accepted() or self.mt.is_rejected):
                opcao = messagebox.askyesno("Percorrimento da MT", ". Gostaria de visualizar o percorrimento da MT?")
                if(opcao):
                    animated_button_mt(self.Grafo, self.mt.states_passed,self.mt.tape_states)
                self.reset_simulation()
            else:
                    messagebox.showinfo("Não finalizado", f"O conjunto de ingredientes não resultado em um estado final ou um estado de erro!")

             



            

        

    def reset_simulation(self):
        self.terminal.delete(1.0, tk.END)
        self.ingredient_entry.delete(0, tk.END)
        self.description_text.config(state=tk.NORMAL)
        self.description_text.delete(1.0, tk.END)
        self.description_text.config(state=tk.DISABLED)
        self.ingredients_sequence.clear()
        if(self.afd):
            self.afd.reset()
        if(self.mt):
             self.mt.reset()
        if(self.apd):
             self.apd.reset()
        self.change_situation(0)
        self.ingredient_image_label.config(image='')

        
        self.afd = None
        self.mt = None
        self.apd = None

    def show_graph(self):
        if self.Grafo:
            if self.afd:
                desenhar_grafo_grid_afd(self.Grafo)
            if self.mt:
                 desenhar_grafo_grid_mt(self.Grafo)

            if self.apd:
                 desenhar_grafo_grid_apd(self.Grafo)
                 


