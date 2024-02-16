import tkinter as tk
from tkinter import PhotoImage
import random
import pygame

class LacBauCuaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lac Bau Cua")
        self.root.iconbitmap('Asset/drapeauVN.ico')
        self.nombre_de_jetons = 0
        self.paris = {"biche": 0, "gourde": 0, "coq": 0, "poisson": 0, "crabe": 0, "crevette": 0}
        self.init_pygame()
        self.load_images()
        self.create_widgets()
        self.create_game_board()
        self.add_launch_dice_button()

    def init_pygame(self):
        pygame.mixer.init()

    def load_images(self):
            self.images = {
                "biche": PhotoImage(file="Asset/nai.png"),
                "gourde": PhotoImage(file="Asset/bau.png"),
                "coq": PhotoImage(file="Asset/ga.png"),
                "poisson": PhotoImage(file="Asset/ca.png"),
                "crabe": PhotoImage(file="Asset/cua.png"),
                "crevette": PhotoImage(file="Asset/tom.png"),
            }
            self.image_jeton = PhotoImage(file="Asset/Jeton.png")

    def create_widgets(self):
        self.configure_grid()

        # Frame pour les labels
        labels_frame = tk.Frame(self.root)
        labels_frame.grid(row=0, column=0, sticky="nw")

        # Frame pour les boutons
        buttons_frame = tk.Frame(self.root)
        buttons_frame.grid(row=0, column=1, sticky="ne")

        # Labels dans le labels_frame
        self.label_jetons = tk.Label(labels_frame, text="Jetons: 0")
        self.label_jetons.pack(anchor="w")

        self.label_gain = tk.Label(labels_frame, text="Gains: 0")
        self.label_gain.pack(anchor="w")

        self.label_resultats = tk.Label(labels_frame, text="Résultats des dés: ")
        self.label_resultats.pack(anchor="w")

        # Boutons dans le buttons_frame
        self.bouton_musique = tk.Button(buttons_frame, text="Jouer/arrêter la musique", command=self.toggle_music)
        self.bouton_musique.pack()

        self.bouton_ajouter_jetons = tk.Button(buttons_frame, text="Ajouter 10 jetons", command=self.ajouter_jetons)
        self.bouton_ajouter_jetons.pack()

        self.bouton_reinitialiser = tk.Button(buttons_frame, text="Réinitialiser les paris", command=self.reinitialiser_paris)
        self.bouton_reinitialiser.pack()

    def create_game_board(self):
        self.plateau = tk.Frame(self.root)
        # Assurez-vous que le plateau se trouve dans la bonne rangée et qu'il s'étend correctement
        self.plateau.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

        self.canvas_elements = {}
        for i, element in enumerate(["biche", "gourde", "coq", "poisson", "crabe", "crevette"]):
            canvas = tk.Canvas(self.plateau, width=128, height=128)
            # Ajustez le placement des canvas si nécessaire
            canvas.grid(row=i // 3, column=i % 3, sticky="nw")
            canvas.create_image(0, 0, anchor="nw", image=self.images[element])
            self.canvas_elements[element] = canvas
            canvas.bind("<Button-1>", lambda event, e=element: self.on_canvas_click(event, e))

    def add_launch_dice_button(self):
        self.bouton_lancer = tk.Button(self.root, text="Lancer les Dés", command=self.lancer_des)
        # Assurez-vous que le bouton s'étend sur toute la largeur de la fenêtre
        self.bouton_lancer.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

    def configure_grid(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)

    def ajouter_jetons(self):
        self.nombre_de_jetons += 10
        self.update_jetons_label()

    def update_jetons_label(self):
        self.label_jetons.config(text=f"Jetons: {self.nombre_de_jetons}")

    def on_canvas_click(self, event, element):
        self.parier(element)

    def parier(self, element):
        if self.nombre_de_jetons > 0:
            self.paris[element] += 1
            self.nombre_de_jetons -= 1
            self.update_jetons_label()
            self.update_jetons_on_canvas(element)

    def update_jetons_on_canvas(self, element):
        x_offset = 10 + 20 * (self.paris[element] - 1)
        y_offset = 10
        self.canvas_elements[element].create_image(x_offset, y_offset, anchor="nw", image=self.image_jeton, tags=f"jeton_{element}")

    def reinitialiser_paris(self):
        total_paris = sum(self.paris.values())
        self.nombre_de_jetons += total_paris
        for key in self.paris.keys():
            self.paris[key] = 0
            self.canvas_elements[key].delete(f"jeton_{key}")
        self.update_jetons_label()

    def lancer_des(self):
        resultats_des = [random.choice(list(self.paris.keys())) for _ in range(3)]
        gains = 0
        for element, mise in self.paris.items():
            count = resultats_des.count(element)
            if count > 0:
                gains += mise + (mise * count)
        self.nombre_de_jetons += gains
        for key in self.paris.keys():
            self.paris[key] = 0
            self.canvas_elements[key].delete(f"jeton_{key}")
        self.update_jetons_label()
        self.label_resultats.config(text="Résultats des dés: " + ", ".join(resultats_des))
        self.label_gain.config(text=f"Gains: {gains}")

    def toggle_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.load("Asset/musicVN.mp3")
            pygame.mixer.music.play(-1)

def main():
    root = tk.Tk()
    app = LacBauCuaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()