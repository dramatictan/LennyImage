# Run this to start

import customtkinter as ctk
from tools.sidebar import side_bar_nav
from user_interface_imagebot import ImageGenPage # ImageGenPage
from user_interface_chatbot import ChatGenPage # ChatGenPage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("LennyImage Multi-Tool")

        # main container to hold the current page
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)
        self.frames = {}

        # Initialize pages
        # Just add the Class Name in the array to store new page
        for F in [ImageGenPage, ChatGenPage]:
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Link the sidebar
        side_bar_nav(self, self.handle_sidebar_click)

        # Start page with image generator first
        self.show_page("ImageGenPage")

    def show_page(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise() # bring frame to front

    # remember update if got new page
    def handle_sidebar_click(self, selection):
        if selection == "image":
            self.show_page("ImageGenPage")
        elif selection == "chat":
            self.show_page("ChatGenPage")


if __name__ == "__main__":
    app = App()
    app.mainloop()