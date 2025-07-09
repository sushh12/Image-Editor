# gui.py
import customtkinter as ctk
from customtkinter import CTkImage
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

from editPanel import EditPanel

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Image Editing Application")
        self.root.geometry("800x600")
        
        self.original_img = None
        self.current_img = None
        self.zoom_scale = 1.0       
        
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
        self.image_frame = ctk.CTkFrame(self.root)
        self.image_frame.pack(side="left", fill="both", expand=True)
        
        self.image_label = ctk.CTkLabel(self.image_frame, text=" ")
        self.image_label.pack(expand=True)
        
        # Edit panel (initially hidden)
        self.edit_panel = EditPanel(self.root, self)
        self.edit_panel.pack(side='right', fill='y')
        self.edit_panel.pack_forget()  # hide initially

        
    # Open/import image
    def open_img(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            self.original_img = Image.open(file_path)
            self.original_img = ImageOps.exif_transpose(self.original_img)
            self.current_img = self.original_img.copy()
            
            # Reset sliders when new image is loaded
            self.edit_panel.reset_sliders()
            
            # Get image label size (or set default if not yet rendered)
            label_width = 500
            label_height = 500

            # Calculate aspect ratio to fit without cropping
            img_ratio = self.current_img.width / self.current_img.height
            label_ratio = label_width / label_height

            if img_ratio > label_ratio:
                new_width = label_width
                new_height = int(label_width / img_ratio)
            else:
                new_height = label_height
                new_width = int(label_height * img_ratio)

            resized_image = self.current_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.img_ctk = ctk.CTkImage (light_image=resized_image, size=(new_width, new_height))
            self.image_label.configure(image=self.img_ctk)
            self.image_label.image = self.img_ctk
            
    def apply_edits(self, values):
        if self.original_img:
            
            img = self.original_img.copy()
            
            # Brightness
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(values["Brightness"])
            
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(values["Contrast"])
            
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(values["Exposure"])
            
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(values["Saturation"])
            
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(values["Brightness"])

            if values["Highlights"] > 0:
                bright = img.point(lambda p: min(255, int(p * (1 + values["Highlights"]))))
                img = Image.blend(img, bright, alpha=0.5)
                
            # Update the current image and display it
            self.current_img = img
            # self.show_edited_img()
            display_img = self.current_img.copy()
            display_img.thumbnail((500, 500))
            self.tk_img = CTkImage(light_image=display_img, size=display_img.size)
            self.image_label.configure(image=self.tk_img)
            self.image_label.image = self.tk_img
        else:
            CTkMessagebox(title="Warning", message="Invalid operation")

    def flip_image(self):
        if self.current_img:
            self.current_img = self.current_img.transpose(Image.FLIP_LEFT_RIGHT)
            self.show_edited_img()

    def rotate_image(self, angle):
        if self.current_img:
            self.current_img = self.current_img.rotate(angle, expand=True)
            self.show_edited_img()
            
    def show_edited_img(self):
        if self.current_img:
            display_img = self.current_img.copy()
            display_img.thumbnail((500, 500))
            self.tk_img = ctk.CTkImage(light_image=display_img, size=display_img.size)
            self.image_label.configure(image=self.tk_img)
            self.image_label.image = self.tk_img

    def save_img(self):
        if self.current_img:
            file_path = filedialog.asksaveasfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
            if file_path:
                self.current_img.save(file_path)
        else:
            CTkMessagebox(title="Warning", message="image not found")
		
    def toggle_edit_panel(self):
        if self.edit_panel.winfo_ismapped():
            self.edit_panel.pack_forget()
        else:
            self.edit_panel.pack(side='right', fill='y')
        
    def save_img(self):
        if self.current_img:
            file_path = filedialog.asksaveasfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
            if file_path:
                self.current_img.save(file_path)
   
    def run(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    app = App()
    app.run()