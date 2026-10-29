from tkinter import *
from PIL import Image, ImageTk
import customtkinter as ctk

# ----------- NEW -------------- #
def side_bar_nav(window, callback):

    min_w = 0      # hidden state
    max_w = 200
    cur_width = min_w
    target_width = min_w
    speed = 12

    # ---------------- SIDEBAR FRAME (HIDDEN INITIALLY) ----------------
    frame = ctk.CTkFrame(window, fg_color="#222222", width=min_w, corner_radius=0)
    frame.place(x=0, y=0, relheight=1)
    frame.lift()
    frame.pack_propagate(False)

    frame.grid_columnconfigure(0, weight = 0)
    frame.grid_columnconfigure(1, weight = 1)
    frame.grid_columnconfigure(2, weight = 1)
    frame.grid_columnconfigure(3, weight = 1)
    frame.grid_columnconfigure(4, weight = 1)

    button_frame = ctk.CTkFrame(master = frame)
    button_frame.pack(fill = "both", expand = True, pady = (70, 0))
    image_btn = ctk.CTkButton(button_frame, text="", fg_color="transparent", anchor="w")
    chat_btn = ctk.CTkButton(button_frame, text="", fg_color="transparent", anchor="w")

    image_btn.grid(row = 1, column = 0, sticky = "w", pady = 10, padx = 5)
    chat_btn.grid(row = 3, column = 0, sticky = "w", pady = 10, padx = 5)

    # Toggle Button
    toggle_btn = ctk.CTkButton(
        window,
        text="☰",
        width=50,
        height = 50,
        fg_color = "#222222",
        hover_color = "#7A7A7A",
        command=lambda: toggle()
    )
    toggle_btn.place(x=10, y=10)
    toggle_btn.lift()

    # state
    expanded_ui = False

    def update_ui():
        nonlocal expanded_ui

        if cur_width > 120 and not expanded_ui:
            image_btn.configure(text=' Image Generation V1', image=None, command = lambda: callback("image"))
            chat_btn.configure(text=' Chatbot', image=None, command = lambda: callback("chat"))
            expanded_ui = True

        elif cur_width <= 120 and expanded_ui:
            image_btn.configure(text='')
            chat_btn.configure(text='')
            expanded_ui = False

    def animate():
        nonlocal cur_width

        if cur_width != target_width:

            if cur_width < target_width:
                cur_width = min(cur_width + speed, target_width)
            else:
                cur_width = max(cur_width - speed, target_width)

            frame.configure(width=cur_width)
            update_ui()

        window.after(15, animate)

    def toggle():
        nonlocal target_width

        if target_width == min_w:
            target_width = max_w
        else:
            target_width = min_w

    # keep sidebar at the top
    def keep_top():
        frame.lift()
        toggle_btn.lift()
        window.after(50, keep_top)

    keep_top()
    animate()
    return toggle
