# gui.py
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from PIL import Image

from editPanel import EditPanel

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Image Editing Application")
        self.root.geometry("800x600")
        
        # self.editor = Editor()
        self.current_img = None
        
        # btn_frame Frame
        self.btn_frame = ctk.CTkFrame(self.root)
        self.btn_frame.pack(side="top", fill="x")
        
        # Open Button
        self.open_btn = ctk.CTkButton(self.btn_frame, text="Open", width=10, command=self.open_img).grid(row=0, column=0)
        # edit Button
        self.edit_btn = ctk.CTkButton(self.btn_frame, text="Edit", width=10, command=self.toggle_edit_panel).grid(row=0, column=1)
        # Save Button
        self.save_btn = ctk.CTkButton(self.btn_frame, text="Save", width=10, command=self.save_img).grid(row=0, column=2)
        
        
        # Image Display Frame
        self.image_frame = ctk.CTkFrame(self.root, fg_color="white")
        self.image_frame.pack(side="left", fill="both", expand=True)
        
        self.image_label = ctk.CTkLabel(self.image_frame, text=" ")
        self.image_label.pack(expand=True)
        
        # Edit panel (initially hidden)
        self.edit_panel = EditPanel(self.root, self)
        self.edit_panel.pack(side='right', fill='y')
        self.edit_panel.pack_forget()  # hide initially

        
     # Open/import image
    # def open_img(self):
    #     file_path = filedialog.askopenfilename(
    #         title="Select an image",
    #         filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
    #     )
    #     if file_path:
    #         self.original_img = Image.open(file_path)
    #         self.current_img = self.original_img.copy()
    #         self.current_img = self.current_img.resize((400, 400))
    #         self.img_ctk = ctk.CTkImage(light_image=self.current_img, size=(400, 400))
    #         self.image_label.configure(image=self.img_ctk)
    #         self.image_label.image = self.img_ctk

    # def save_img(self):
    #     if self.current_img:
    #         file_path = filedialog.asksaveasfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
    #         if file_path:
    #             self.current_img.save(file_path)
    #     else:
    #         CTkMessagebox(title="Warning", message="image not found")
		
    # def toggle_edit_panel(self):
    #     if self.edit_panel.winfo_ismapped():
    #         self.edit_panel.pack_forget()
    #     else:
    #         self.edit_panel.pack(side='right', fill='y')
            
    def run(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    app = App()
    app.run()

