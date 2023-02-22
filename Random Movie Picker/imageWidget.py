import customtkinter
from PIL import Image
import requests
import webbrowser

class ButtonImageWidget(customtkinter.CTkFrame):
    def __init__(self, master ,command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.media_dict = {}
        self.image_list = []
        self.url_list = []
        self.button_list = []
        self.command = command
        self.dict_length = 0
        self.configure(fg_color="#000000")

    def add_images(self, media_dict):
        self.media_dict = media_dict
        self.dict_length = len(self.media_dict)
        for key in self.media_dict:
            img = Image.open(requests.get(media_dict[key][3], stream=True).raw)
            self.image_list.append(customtkinter.CTkImage(img))
            self.url_list.append(media_dict[key][1])
        self.add_buttons()
    
    def add_buttons(self):
        for i in range(self.dict_length):
            button = customtkinter.CTkButton(self, image=self.image_list[i], command=lambda i=i: webbrowser.open(self.url_list[i]))
            if i < 2:
                button.grid(row=i, column=0, pady=(0, 10))
            else:
                button.grid(row=i-2, column=1, pady=(0, 10))
            self.button_list.append(button)
        print(self.button_list)