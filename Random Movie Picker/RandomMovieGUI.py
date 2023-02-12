import tk 
import random
import customtkinter as ctk
from movieScrapper import getMediaInfo

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class RandomMovieGUI(ctk.CTk):
    def __init__(self):
        self.app = ctk.CTk()
        self.media = getMediaInfo()
        self.create_base_widget()


    def create_base_widget(self):
        self.app.title("Random Movie Picker")
        self.app.geometry("500x500")
        self.app.resizable(True, True)

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app=RandomMovieGUI()
    app.run()
