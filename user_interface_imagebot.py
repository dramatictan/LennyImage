import tkinter as tk

from PIL import Image, ImageTk
from pathlib import Path
import customtkinter as ctk
import threading
import os
from tkinter import messagebox

from imagebot import generate_image

# ------------------------- Page 1 ------------------------------- #
class ImageGenPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.WIDTH = 768
        self.HEIGHT = 768
        self.STEPS = 50

        # Function callback to generate image
        def generate_image_callback(event=None):
            user_prompt = entryInput.get() # Retrieve user input from entryInput
            image_name_prompt = imageNameInput.get()

            if not image_name_prompt:
                image_name_prompt = user_prompt

            # parse integer inputs
            try:
                w = int(widthInput.get())
                h = int(heightInput.get())
            except ValueError:
                w, h = 768, 768

            # if inference step is invalid, default to 50
            try:
                s = int(stepInput.get())
            except ValueError:
                s = 50

            # Disable button when generating
            button.configure(state="disable", text="Generating...")

            # Remove previous image and add progress bar back
            inputLabel.pack_forget()
            progress.pack(expand=True, pady=250)
            progress.set(0)
            progress.start()

            def worker():
                file_path = generate_image(user_prompt, image_name_prompt, width=w, height=h, steps=s)
                self.after(0, lambda: finish_generation(file_path))

            threading.Thread(target=worker, daemon=True).start()

        # Call imagebot.py
        def run_generation(prompt, name, width=None, height=None, steps=None):
            width = width or self.WIDTH
            height = height or self.HEIGHT
            steps = steps or self.STEPS

            file_path = generate_image_callback(prompt, name, width=self.WIDTH, height=self.HEIGHT, steps=self.STEPS)
            update_image_preview(file_path)
            button.configure(state="normal", text="Generate")

        # Display image from folder
        def update_image_preview(file_path):
            if not os.path.exists(file_path):
                messagebox.showerror("Error", "File not found.")
                return

            self.update()
            img = Image.open(file_path)

            # Get current frame size
            frame_width = frame.winfo_width()
            frame_height = frame.winfo_height()
            if frame_width <= 10 or frame_height <= 10:
                frame_width, frame_height = 800, 800

            img.thumbnail((frame_width, frame_height)) # Generated image size
            tk_img = ImageTk.PhotoImage(img) # Final Image product

            # Replace placeholder label with the output image
            inputLabel.configure(image=tk_img, text="")
            inputLabel.image = tk_img
            progress.pack_forget() # remove progress bar when image is done
            inputLabel.pack(expand=True)

        # Dimension Edit
        def defaultDimension(event=None):
            widthInput.delete(0, tk.END)
            widthInput.insert(0, self.WIDTH)
            heightInput.delete(0, tk.END)
            heightInput.insert(0, self.HEIGHT)

        def portraitDimension():
            widthInput.delete(0, tk.END)
            widthInput.insert(0, "768")
            heightInput.delete(0, tk.END)
            heightInput.insert(0, "1024")

        def landscapeDimension():
            widthInput.delete(0, tk.END)
            widthInput.insert(0, "1024")
            heightInput.delete(0, tk.END)
            heightInput.insert(0, "768")

        def testDefaultDimension():
            widthInput.delete(0, tk.END)
            widthInput.insert(0, "512")
            heightInput.delete(0, tk.END)
            heightInput.insert(0, "512")

        def finish_generation(file_path):
            update_image_preview(file_path)
            get_image_paths("generated_images") # Call function again to update the stored images
            delete_image("generated_images") # Delete the earliest image available

            # Progress Bar
            progress.stop()
            progress.set(1)

            button.configure(state="normal", text="Generate")

        # Steps Edit
        def defaultSteps(event=None):
            stepInput.delete(0, tk.END)
            stepInput.insert(0, self.STEPS)

        # ---------------------------------------------------------
        # Saved Images Array
        def get_image_paths(folder_path):
            folder = Path(folder_path)
            col_counter = 0

            try:
                if not folder.exists():
                    raise FileNotFoundError(f"Folder not found: {folder}")
                if not folder.is_dir():
                    raise NotADirectoryError(f"Not a directory: {folder}")

                for widget in rightFrame.winfo_children():
                    if isinstance(widget, ctk.CTkLabel) and widget != savedImagesLabel:
                        widget.destroy()

                # Sort png images by last modified time (show newest first)
                stored_images = sorted(Path(folder).glob('*.png'), key=lambda x: x.stat().st_mtime, reverse=True)

                for stored_image in stored_images:
                    print(stored_image)

                    img = Image.open(stored_image)
                    img.thumbnail((200, 200))
                    tk_img = ImageTk.PhotoImage(img)

                    lbl = ctk.CTkLabel(imagesFrame, image=tk_img, text="")
                    lbl.image = tk_img
                    lbl.grid(row=1, column=col_counter, sticky="w", padx=20, pady=5)
                    col_counter += 1 # increment col for image to be stacked horizontally

            finally:
                print("Images found.")

        def delete_image(folder_path):
            max_stored_image = 11
            folder = Path(folder_path)

            # Stored images in temp array
            stored_images = sorted(Path(folder).glob("*.png"), key=lambda x: x.stat().st_mtime) # sort to oldest image first
            if len(stored_images) > max_stored_image:
                oldest_image = stored_images[0]
                try:
                    os.remove(oldest_image)
                    print(f"Image deleted successful after limit reached.")
                except Exception as e:
                    print(f"Failed to delete image: {e}")


        # ----------------------------------------------------------------
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self.grid_rowconfigure(0, weight=0) # title stays top
        self.grid_rowconfigure(1, weight=1) # image frame expand to fill space
        self.grid_rowconfigure(2, weight=0) # input stays bottom
        self.grid_rowconfigure(3, weight=0)

        # Pin text to top-left corner
        label = ctk.CTkLabel(self, text="LennyImage", font=("Roboto", 24, "bold"))
        label.grid(row=0, column=0, sticky="nw", padx=80, pady=20, columnspan=2)

        # ------------------------- Main (Row 1) -------------------------
        # Image Generated Output Section
        frame = ctk.CTkFrame(master=self)
        frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew", columnspan=2) # nsew means stretch to fill the entire row 1 which around the middle section
        frame.grid_propagate(True)

        # Progress Bar
        progress = ctk.CTkProgressBar(frame, orientation='horizontal', width=600)

        # label inside the frame through master = frame
        inputLabel = ctk.CTkLabel(master=frame, text="", font=("Roboto", 24))
        inputLabel.pack(expand=True)

        # ------------------------- Window -------------------------
        # input entry
        entryInput = ctk.CTkEntry(self, width=600, height=40, placeholder_text="Generate a rainbow")
        entryInput.grid(row=2, column=0, pady=(10, 5), padx=20, sticky="sew")

        # file name input entry
        imageNameInput = ctk.CTkEntry(self, width=600, height=40, placeholder_text="Name of the image file (optional)")
        imageNameInput.grid(row=3, column=0, pady=(5, 20), padx=20, sticky="sew")

        # Command will be generateImage for the function
        button = ctk.CTkButton(
            master = self,
            text = "Generate",
            width = 150,
            height = 60,
            corner_radius = 10,
            fg_color = "#6A5ACD",
            hover_color = "#836FFF",
            border_color = "#483D8B",
            border_width = 1,
            font = ("Roboto", 18, "bold"),
            command = generate_image_callback # generate image
        )
        button.grid(row=3, column=1, pady=(5, 30), padx=30, sticky="sw")
        entryInput.bind("<Return>", lambda e: generate_image_callback())
        imageNameInput.bind("<Return>", lambda e: generate_image_callback())

        # ------------------------- Right Side Bar -------------------------
        rightFrame = ctk.CTkFrame(master=self)
        rightFrame.grid(row=1, column=2, padx=20, pady=20, sticky="nsew", rowspan=3) # nsew means stretch to fill the entire row 1 which around the middle section

        # Content inside the sidebar
        savedImagesLabel = ctk.CTkLabel(master=rightFrame, text="Saved Images", font=("Roboto", 15, "bold"))
        savedImagesLabel.grid(row=0, column=0, sticky="w", padx=20, pady=40)

        rightFrame.grid_columnconfigure(0, weight=0)
        rightFrame.grid_rowconfigure(0, weight=0) # label only
        rightFrame.grid_rowconfigure(1, weight=1) # Saved Image
        rightFrame.grid_rowconfigure(2, weight=0) # Image Dimensions
        rightFrame.grid_rowconfigure(3, weight=1) # Num Inference Step
        rightFrame.grid_rowconfigure(4, weight = 1)

        savedSectionLabel = ctk.CTkLabel(rightFrame, text="No image saved yet", font=("Roboto", 12)) # Placeholder for stored images
        savedSectionLabel.grid(row=1, column=0, sticky="w", padx=20)

        # Scrollbar
        # (imageFrame -> rightFrame -> lbl)
        imagesFrame = ctk.CTkScrollableFrame(rightFrame, orientation="horizontal", width=480, height=190)
        imagesFrame.grid(row=1, column=0, padx=20, sticky="nsew")

        # Image Dimensions
        dimensionFrame = ctk.CTkFrame(master=rightFrame, fg_color="transparent")
        dimensionFrame.grid(row=2, column=0, sticky="w")

        dimensionLabel = ctk.CTkLabel(dimensionFrame, text="Dimensions", font=("Roboto", 15, "bold"))
        dimensionLabel.grid(row=0, column=0, sticky="w", padx=20, pady=10)

        heightInput = ctk.CTkEntry(dimensionFrame, width=230, height=40, placeholder_text="Height (px)")
        heightInput.grid(row=1, column=0, pady=(10, 0), padx=(20, 10), sticky="ew")

        widthInput = ctk.CTkEntry(dimensionFrame, width=230, height=40, placeholder_text="Width (px)")
        widthInput.grid(row=1, column=1, pady=(10, 0), padx=(10, 20), sticky="ew")

        # Button Dimensions Preset
        buttonGroupFrame = ctk.CTkFrame(master=dimensionFrame, fg_color="transparent")
        buttonGroupFrame.grid(row=2, column=0, columnspan=2, pady=20, sticky="ew")
        buttonGroupFrame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        defaultButton = ctk.CTkButton(buttonGroupFrame, text="Default", font=("Roboto", 15), width=150, command=defaultDimension)
        portraitButton = ctk.CTkButton(buttonGroupFrame, text="Portrait", font=("Roboto", 15), width=150, command=portraitDimension)
        landscapeButton = ctk.CTkButton(buttonGroupFrame, text="Landscape", font=("Roboto", 15), width=150, command=landscapeDimension)
        testDefaultButton = ctk.CTkButton(buttonGroupFrame, text="Test-Default", font=("Roboto", 15), width=150, command=testDefaultDimension)

        defaultButton.grid(row=0, column=0, padx=(5, 0))
        portraitButton.grid(row=0, column=1, padx=5)
        landscapeButton.grid(row=0, column=2, padx=5)
        testDefaultButton.grid(row=0, column=3, padx=5)

        # Num Inference Steps
        stepFrame = ctk.CTkFrame(master=rightFrame, fg_color="transparent")
        stepFrame.grid(row=3, column=0, sticky="w")

        stepLabel = ctk.CTkLabel(stepFrame, text="Steps", font=("Roboto", 15, "bold"))
        stepLabel.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        stepInput = ctk.CTkEntry(stepFrame, width=230, height=40, placeholder_text="Steps Required (min: 10, max: 50)")
        stepInput.grid(row=1, column=0, pady=(10, 0), padx=(20, 10), sticky="ew")

        get_image_paths("generated_images")

