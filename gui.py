# gui.py
import customtkinter as ctk
from customtkinter import CTkImage
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageTk

from editPanel import EditPanel

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Image Editing Application")
        self.root.geometry("800x600")
        
        self.original_img = None
        self.current_img = None      
        
        # Configure grid layout
        self.root.grid_rowconfigure(1, weight=1)  # Row 1 will expand
        self.root.grid_columnconfigure(0, weight=1)  # Image column expands
        self.root.grid_columnconfigure(1, weight=0)  # Panel column static
        
        # btn_frame Frame
        self.btn_frame = ctk.CTkFrame(self.root)
        self.btn_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Configure column weights for buttons to adjust spacing as needed
        self.btn_frame.columnconfigure((0,1,2), weight=0)
        
        # Open Button
        ctk.CTkButton(self.btn_frame, text="Open", width=10, command=self.open_img).grid(row=0, column=0)
        # edit Button
        ctk.CTkButton(self.btn_frame, text="Edit", width=10, command=self.toggle_edit_panel).grid(row=0, column=1)
        # Save Button
        ctk.CTkButton(self.btn_frame, text="Save", width=10, command=self.save_img).grid(row=0, column=2)
        
        # Image Display Frame
        self.image_frame = ctk.CTkFrame(self.root)
        self.image_frame.grid(row=1, column=0, sticky="nsew")
        
        # image display canvas
        self.image_canvas = ctk.CTkCanvas(self.image_frame,width=500, height=500, bg="#272727",borderwidth=0, highlightthickness=0)
        self.image_canvas.place(relx=0.5, rely=0.5, anchor="center")
        
        # Initialize image_id for canvas image
        self.image_id = None
        
        # Bind mouse events for dragging
        self.image_canvas.bind("ButtonPress-1", self.start_drag)
        self.image_canvas.bind("B1-Motion", self.do_drag)
        
        # Drag variables
        self.drag_data = {"x":0, "y":0}
        
        # Edit panel (initially hidden)
        self.edit_panel = EditPanel(self.root, self)
        self.edit_panel.grid(row=1, column=1, sticky="ns")
        self.edit_panel.grid_remove()  # hide initially

        
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
            self.display_img(self.current_img)
 
    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def do_drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]

        # Move image
        if self.image_id:
            self.image_canvas.move(self.image_id, dx, dy)

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
            
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
                
            self.display_img(img)
        else:
            CTkMessagebox(title="Warning", message="Invalid operation")

    def flip_image(self):
        if self.current_img:
            flipped = self.current_img.transpose(Image.FLIP_LEFT_RIGHT)
            self.display_img(flipped)

    def rotate_image(self, angle):
        if self.current_img:
            rotated = self.current_img.rotate(angle, expand=True)
            self.display_img(rotated)

    def display_img(self, current_img):
        if current_img is None:
            return
        
         # Canvas size
        canvas_width = int(self.image_canvas.winfo_width()) 
        canvas_height = int(self.image_canvas.winfo_height()) 

        # Calculate aspect ratio to fit without cropping
        img_ratio = self.current_img.width / self.current_img.height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / img_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * img_ratio)

        resized_image = current_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(resized_image)
            
        # Delete previous image if any
        if self.image_id:
            self.image_canvas.delete(self.image_id)
        
        # Display image created
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        self.image_id = self.image_canvas.create_image(center_x, center_y, anchor="center", image=self.tk_img)
        
        # Update current_img
        self.current_img = current_img

    def save_img(self):
        if self.current_img:
            file_path = filedialog.asksaveasfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
            if file_path:
                self.current_img.save(file_path)
        else:
            CTkMessagebox(title="Warning", message="image not found")
		
    def toggle_edit_panel(self):
        if self.edit_panel.winfo_ismapped():
            self.edit_panel.grid_remove()
        else:
            self.edit_panel.grid(row=1, column=1, sticky="ns")
   
    def run(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    app = App()
    app.run()