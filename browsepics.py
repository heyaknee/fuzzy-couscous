import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageBrowserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Browser")
        self.root.geometry("800x600")

        # Variable to hold the path of selected image
        self.current_image = None
        self.current_image_index = 0
        self.image_list = []
        self.copy_image_var = tk.BooleanVar()  # Variable for checkbox

        # Creating the UI
        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons and checkbox
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Button to select the folder
        self.select_folder_btn = tk.Button(top_frame, text="Select Folder", command=self.select_folder)
        self.select_folder_btn.pack(side=tk.LEFT, padx=5)

        # Button to go to the previous image
        self.prev_btn = tk.Button(top_frame, text="Previous", command=self.prev_image)
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        # Button to go to the next image
        self.next_btn = tk.Button(top_frame, text="Next", command=self.next_image)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        # Checkbox to copy the image
        self.copy_checkbox = tk.Checkbutton(top_frame, text="Copy Image", variable=self.copy_image_var)
        self.copy_checkbox.pack(side=tk.RIGHT, padx=5)

        # Label to show the selected image
        self.image_label = tk.Label(self.root)
        self.image_label.pack(padx=10, pady=10, expand=True)

        # Label to show the image name
        self.image_name_label = tk.Label(self.root, text="")
        self.image_name_label.pack()

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.image_list = [f for f in os.listdir(folder_selected) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            self.image_folder = folder_selected
            if self.image_list:
                self.current_image_index = 0
                self.load_image()

    def load_image(self):
        if self.image_list:
            image_path = os.path.join(self.image_folder, self.image_list[self.current_image_index])
            image = Image.open(image_path)
            image.thumbnail((600, 400))  # Resize image to fit the window
            self.current_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.current_image)
            self.image_name_label.config(text=self.image_list[self.current_image_index])

            # Automatically copy the image if checkbox is checked
            if self.copy_image_var.get():
                self.copy_image()

    def next_image(self):
        if self.image_list and self.current_image_index < len(self.image_list) - 1:
            self.current_image_index += 1
            self.load_image()

    def prev_image(self):
        if self.image_list and self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_image()

    def copy_image(self):
        dest_folder = filedialog.askdirectory(title="Select Destination Folder")
        if dest_folder:
            image_path = os.path.join(self.image_folder, self.image_list[self.current_image_index])
            try:
                shutil.copy(image_path, dest_folder)
                messagebox.showinfo("Success", f"Image copied to {dest_folder}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageBrowserApp(root)
    root.mainloop()
