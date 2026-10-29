import tkinter as tk

from PIL import Image, ImageTk
from pathlib import Path
import customtkinter as ctk
import threading
import os
from tkinter import messagebox, PhotoImage

from huggingface_hub.utils import send_telemetry

from chatbot import generate_output

# Ideas:
# Add avatar 3D
# Add framing of the avatar 

# ------------------------- Page 3 ------------------------------- #
class ChatGenPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Store input and output temporary
        self.stored_user_input = []
        self.stored_chatbot_output = []

        # Send input to chatbot
        def send_input():

            if send_btn.cget("state") == "disable":
                return

            # Retrieve text from input entry and remove whitespaces
            contents = human_input.get()
            if not contents.strip():
                return

            # Append user input to create a history convo track
            self.stored_user_input.append(contents) # Add to convo track array

            update_ui("You", contents) # send to convo frame

            send_btn.configure(state = "disable", text = "Sending...")
            human_input.delete(0, tk.END)

            # AI generate response output
            def worker():
                response = generate_output(contents)
                print(f"AI received: {contents}")
                # print(f"AI responded: {response}") CONFIRM UI CAN RETRIEVE OUTPUT

                self.after(0, lambda: retrieve_output(response))

            threading.Thread(target = worker, daemon = True).start()

        # Retrieve output
        def retrieve_output(output):
            self.update()

            # TEST: Ask the UI to put the output on the main screen
            print(f"Output response from Gemini in UI: {output}")

            self.stored_chatbot_output.append(output) # stored to output track array
            update_ui("Chatbot", output) # send to convo frame

            # Revert button to normal state to type new message
            send_btn.configure(state = "normal", text = "Send")
            return output

        # Update UI to show input and response at the output frame
        # sender can be AI ot you
        # text can be either message sent by both side
        def update_ui(sender, text):
            if sender == "Chatbot":
                font_type = "Google Sans Mono"
                align = "w"
                bubble_color = "#1E90FF"
            else:
                font_type = "Google Sans Mono"
                align = "e"
                bubble_color = "#FF7F50"

            # Bubble frame
            bubble_frame = ctk.CTkFrame(
                master=output_frame,
                fg_color=bubble_color,
                corner_radius=16  # Rounded corners for the bubble
            )
            bubble_frame.pack(pady=6, padx=10, anchor=align)

            # Create the text label inside the bubble frame
            convo_label = ctk.CTkLabel(
                master=bubble_frame,
                text=text,
                wraplength=800,
                font=(font_type, 15, "bold"),
                justify="left"
            )
            convo_label.pack(padx=14, pady=10)

            self.update_idletasks()
            output_frame._parent_canvas.yview_moveto(1.0) # auto scroll to bottom after new message

        # -------------------------------------------------------------------------------------------------
        # Main Body
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 4) # Chat body
        self.grid_columnconfigure(3, weight = 4) # Chat Body

        self.grid_rowconfigure(0, weight = 0) # title stays top
        self.grid_rowconfigure(1, weight = 1) # Chat body
        self.grid_rowconfigure(2, weight = 0) # Input

        label = ctk.CTkLabel(self, text="LennyImage", font=("Roboto", 24, "bold"))
        label.grid(row=0, column=0, sticky="nw", padx=80, pady=20, columnspan=4)

        # ------------------------- Main (Row 1) -------------------------
        # Output Text Section
        output_frame = ctk.CTkScrollableFrame(master = self, height = 600)
        output_frame.grid(row = 1, column = 2, padx = 40, pady = 20, columnspan = 2, sticky = "nsew")

        # Input Text Section
        input_frame = ctk.CTkFrame(master = self, fg_color = "transparent")
        input_frame.grid(row = 2, column = 2, padx = 40, pady = (5, 40), columnspan = 2, sticky = "nsew")
        input_frame.grid_columnconfigure(0, weight = 1)
        input_frame.grid_columnconfigure(1, weight = 0)

        human_input = ctk.CTkEntry(master = input_frame, width = 1000, height = 60, placeholder_text = "How do I learn Python?")
        human_input.grid(row = 0, column = 0, pady = (5, 50), sticky = "ew")
        send_btn = ctk.CTkButton(
            master = input_frame,
            text = "Send",
            width = 150,
            height = 60,
            corner_radius = 10,
            fg_color = "#6A5ACD",
            hover_color = "#836FFF",
            border_color = "#483D8B",
            border_width = 1,
            font = ("Roboto", 18, "bold"),
            command = send_input
        )
        send_btn.grid(row = 0, column = 1, pady = (5, 30), padx = 30, sticky = "nw")
        human_input.bind("<Return>", lambda e: send_input())
        # -------------------------------------------------------------------------------------------------


