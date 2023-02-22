import tkinter as tk
import random
import customtkinter as ctk
from movieScrapper import getMediaInfo
from ScrollableCheckBoxFrame import ScrollableCheckBoxFrame
from imageWidget import ButtonImageWidget

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class RandomMovieGUI(ctk.CTk):
    def getMedia(self, numPages):
        self.media_dict = getMediaInfo(numPages)
        #get all the genres from the media_dict using a set
        self.new_genre_list = []
        for key in self.media_dict:
            for genre in self.media_dict[key][5]:
                if genre not in self.all_genre_list:
                    self.new_genre_list.append(genre)
        self.new_genre_list = list(set(self.new_genre_list))
        self.all_genre_list = self.all_genre_list + self.new_genre_list



    def __init__(self):
        super().__init__()
        self.media_dict = {}
        self.filtered_media = {}
        self.IMDB_score = 0
        self.new_genre_list = []
        self.all_genre_list = []
        self.year_max = 1900
        self.genre_list_selected = []
        self.movies_selected = False
        self.series_selected = False
        self.number_of_pages = 1
        # configure window
        self.title("Movie Picker")
        self.geometry(f"{1320}x{696}")
        self.resizable(False, False)

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0,sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=0)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Movie Picker", font=ctk.CTkFont(size=26, weight="bold"))
        self.logo_label.grid(row=0, column=0,padx=20, pady=(50, 40))
        
        self.page_selector = ctk.CTkButton(self.sidebar_frame, command=self.select_number_of_pages, text="Select number of pages to scan")
        self.page_selector.grid(row=1, column=0, padx=20, pady=10)
        
        self.IMDB_slider_label = ctk.CTkLabel(self.sidebar_frame, text="Select minimum IMDB score", anchor="w")
        self.IMDB_slider_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.IMDB_slider = ctk.CTkSlider(self.sidebar_frame, from_=0, to=10, number_of_steps=100,command=self.change_IMDB_slider_event)
        self.IMDB_slider.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        
    
        self.type_of_media_label = ctk.CTkLabel(self.sidebar_frame, text="Select type of media", anchor="w")
        self.type_of_media_label.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.movie_checkbox = ctk.CTkCheckBox(self.sidebar_frame, text="Movies", command=self.movie_checkbox_event)
        self.movie_checkbox.grid(row=5, column=0, padx=15, pady=5)
        self.tv_checkbox = ctk.CTkCheckBox(self.sidebar_frame, text="TV Shows", command=self.tv_checkbox_event)
        self.tv_checkbox.grid(row=6, column=0, padx=15, pady=5)
        
        self.media_genres_label = ctk.CTkLabel(self.sidebar_frame, text="Select genres", anchor="w")
        self.media_genres_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.media_genres_checkbox = ScrollableCheckBoxFrame(master=self.sidebar_frame, width=200, command=self.genre_checkbox_event,
                                                                 item_list=self.new_genre_list)
        self.media_genres_checkbox.grid(row=8, column=0, padx=15, pady=15, sticky="ns")

        self.search_button = ctk.CTkButton(self.sidebar_frame, command=self.search_button_event, text="Search")
        self.search_button.grid(row=9, column=0, padx=20, pady=10)

        self.image_frame = ctk.CTkFrame(self, corner_radius=0)
        self.image_frame.grid(row=0, column=1, rowspan=4,sticky="nsew")
        self.selectable_images = ButtonImageWidget(self.image_frame, width=100, height=100)


    def search_button_event(self):
        try:
            self.getMedia(numPages=self.number_of_pages)
            for genre in self.new_genre_list:
                    self.media_genres_checkbox.add_item(item=genre)
            filtered_media=self.filterAllMedia()
            self.selectable_images.add_images(filtered_media)
        except ValueError or TypeError:
            pass

    def select_number_of_pages(self):
        dialog = ctk.CTkInputDialog(text="Type in a number:", title="Select number of pages")
        try:
            self.number_of_pages =int(dialog.get_input())
            self.page_selector.configure(text=f"Number of pages: {self.number_of_pages}")
        except ValueError or TypeError:
            pass

    def filterAllMedia(self):
        #filter the media dict by the selected filters (genres, IMDB score, year and media type)
        filtered_media = self.filterByType(self.media_dict)
        filtered_media = self.filterByGenre(filtered_media)
        filtered_media = self.filterByIMDB(filtered_media)
        return filtered_media

    def filterByIMDB(self, media_dic):
        #filter the media dict by the selected IMDB score
        filtered_media = {}
        for key, value in media_dic.items():
            if value[2] >= self.IMDB_score:
                filtered_media[key] = value
        return filtered_media
    
    def filterByGenre(self, media_dic):
        #filter the media dict by the selected genres
        filtered_media = {}
        selected_genres = self.genre_list_selected
        for key, value in media_dic.items():
            for genre in value[5]:
                if genre in selected_genres:
                    filtered_media[key] = value
                    break
        return filtered_media

    def filterByType(self, media_dic):
        #filter the media dict by the selected media type
        filtered_media = {}
        print(self.movies_selected, self.series_selected)
        if self.movies_selected:
            for key, value in media_dic.items():
                if value[0] == "Filme":
                    filtered_media[key] = value
        if self.series_selected:
            for key, value in media_dic.items():
                if value[0] == "Série":
                    filtered_media[key] = value
        return filtered_media

    
    def change_IMDB_slider_event(self, new_value):
        #format the value to 1 decimal place
        new_value = round(new_value, 1)
        self.IMDB_slider_label.configure(text=f"Min IMDB: {new_value}")
        self.IMDB_score = new_value
    
    def change_year_slider_event(self, new_value):
        new_value = int(new_value)
        self.ReleaseYear_slider_label.configure(text=f"Max release Year: {new_value}")
        self.year_max = new_value


    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def movie_checkbox_event(self):
        self.movies_selected = self.movie_checkbox.get()

    def tv_checkbox_event(self):
        self.series_selected = self.tv_checkbox.get()
        
    def genre_checkbox_event(self):
        self.genre_list_selected = self.media_genres_checkbox.get_checked_items()

if __name__ == "__main__":
    app=RandomMovieGUI()
    app.mainloop()
