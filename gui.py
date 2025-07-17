import customtkinter as ctk
import tkinter as tk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from PIL import Image, ImageOps, ImageEnhance, ImageTk

from editPanel import EditPanel
from filterPanel import FilterPanel

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Image Editing Application")
        self.root.geometry("800x600")

        # Initialization
        self.original_img = None
        self.current_img = None
        self.crop_mode = False
        self.undo_stack = []

        # Configure grid layout
        self.root.grid_rowconfigure(1, weight=1)  # Row 1 will expand
        self.root.grid_columnconfigure(0, weight=1)  # Image column expands
        self.root.grid_columnconfigure(1, weight=0)  # Panel column static

        # Top buttons Frame
        self.btn_frame = ctk.CTkFrame(self.root)
        self.btn_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Configure column weights for buttons to adjust spacing as needed
        self.btn_frame.columnconfigure((0, 1, 2), weight=0)

        # Open Button
        ctk.CTkButton(self.btn_frame, text="Open", width=10, command=self.open_img).grid(row=0, column=0)
        # edit Button
        ctk.CTkButton(self.btn_frame, text="Edit", width=10, command=self.toggle_edit_panel).grid(row=0, column=1)
        # Save Button
        ctk.CTkButton(self.btn_frame, text="Save", width=10, command=self.save_img).grid(row=0, column=2)
        # Undo Button
        ctk.CTkButton(self.btn_frame, text="Undo", width=10, command=self.undo).grid(row=0, column=3)

        # Image Display Frame
        self.image_frame = ctk.CTkFrame(self.root)
        self.image_frame.grid(row=1, column=0, sticky="nsew")

        # Image display canvas
        self.image_canvas = tk.Canvas(self.image_frame, width=600, height=600, bg="#272727", borderwidth=0, highlightthickness=0)
        self.image_canvas.place(relx=0.5, rely=0.5, anchor="center")

        # Initialize image_id for canvas image
        self.image_id = None

        # Edit panel (initially hidden)
        self.edit_panel = EditPanel(self.root, self)
        self.edit_panel.grid(row=1, column=1, sticky="ns")
        self.edit_panel.grid_remove()  # hide initially

        # Filter panel (right side)
        self.filter_panel = FilterPanel(self.root, self)
        self.filter_panel.grid(row=0, column=2, sticky="ns")
        self.filter_panel.grid_remove()  # hide initially

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

    def apply_edits(self, values):
        if self.current_img:
            img = self.original_img.copy()
            img = ImageEnhance.Brightness(img).enhance(values["Brightness"])
            img = ImageEnhance.Contrast(img).enhance(values["Contrast"])
            img = ImageEnhance.Brightness(img).enhance(values["Exposure"])
            img = ImageEnhance.Color(img).enhance(values["Saturation"])
            if values["Highlights"] > 0:
                bright = img.point(lambda p: min(255, int(p * (1 + values["Highlights"]))))
                img = Image.blend(img, bright, alpha=0.5)
            self.push_undo()
            self.display_img(img)
        else:
            CTkMessagebox(title="Warning", message="Invalid operation")

    def toggle_crop_mode(self):
        if not self.current_img:
            CTkMessagebox(title="Warning", message="No image loaded")
            return
        if self.crop_mode:
            # Exit crop mode: remove rectangle, scalers, button
            if hasattr(self, 'crop_rect'):
                self.image_canvas.delete(self.crop_rect)
            if hasattr(self, 'scalers'):
                for scaler in self.scalers:
                    self.image_canvas.delete(scaler)
            if hasattr(self, 'confirm_crop_btn'):
                self.confirm_crop_btn.destroy()
            self.crop_mode = False
        else:
            # Enter crop mode
            self.crop_mode = True
            # Initialize crop rectangle covering full canvas
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()
            x1, y1 = 0, 0
            x2, y2 = canvas_width, canvas_height
            self.crop_box = [x1, y1, x2, y2]

            # Draw crop rectangle
            self.crop_rect = self.image_canvas.create_rectangle(*self.crop_box, outline="red", width=2)

            # Draw scalers/handles at corners
            self.scalers = []
            for x, y in self.get_scaler_positions():
                handle = self.image_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue", tags="scaler")
                self.scalers.append(handle)

            # Bind events to scalers
            self.image_canvas.tag_bind("scaler", "<ButtonPress-1>", self.on_scaler_press)
            self.image_canvas.tag_bind("scaler", "<B1-Motion>", self.on_scaler_drag)

            # Add confirm crop button below image
            self.confirm_crop_btn = ctk.CTkButton(self.image_frame, text="Confirm Crop", command=self.confirm_crop)
            self.confirm_crop_btn.place(relx=0.5, rely=0.95, anchor="s")

    def get_scaler_positions(self):
        x1, y1, x2, y2 = self.crop_box
        return [
            (x1, y1), (x2, y1),
            (x2, y2), (x1, y2)
        ]

    def on_scaler_press(self, event):
        self.dragged_scaler = self.image_canvas.find_withtag("current")[0]

    def on_scaler_drag(self, event):
        index = self.scalers.index(self.dragged_scaler)
        # Update crop_box based on dragged scaler
        if index == 0:
            self.crop_box[0], self.crop_box[1] = event.x, event.y
        elif index == 1:
            self.crop_box[2], self.crop_box[1] = event.x, event.y
        elif index == 2:
            self.crop_box[2], self.crop_box[3] = event.x, event.y
        elif index == 3:
            self.crop_box[0], self.crop_box[3] = event.x, event.y

        # Update rectangle and scalers
        self.image_canvas.coords(self.crop_rect, *self.crop_box)
        for i, (x, y) in enumerate(self.get_scaler_positions()):
            self.image_canvas.coords(self.scalers[i], x - 5, y - 5, x + 5, y + 5)

    def confirm_crop(self):
        if not self.crop_box:
            return

        x1, y1, x2, y2 = self.crop_box

        # Calculate displayed image dimensions
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        img_width, img_height = self.current_img.size

        img_ratio = img_width / img_height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            displayed_width = canvas_width
            displayed_height = int(canvas_width / img_ratio)
        else:
            displayed_height = canvas_height
            displayed_width = int(canvas_height * img_ratio)

        # Calculate top-left of displayed image on canvas
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        img_x1 = center_x - displayed_width // 2
        img_y1 = center_y - displayed_height // 2

        # Adjust crop box relative to displayed image
        rel_x1 = min(max(x1 - img_x1, 0), displayed_width)
        rel_y1 = min(max(y1 - img_y1, 0), displayed_height)
        rel_x2 = min(max(x2 - img_x1, 0), displayed_width)
        rel_y2 = min(max(y2 - img_y1, 0), displayed_height)

        # Map to original image coordinates
        scale_x = img_width / displayed_width
        scale_y = img_height / displayed_height

        crop_coords = (
            int(rel_x1 * scale_x),
            int(rel_y1 * scale_y),
            int(rel_x2 * scale_x),
            int(rel_y2 * scale_y)
        )

        # Ensure coordinates are within original image bounds
        crop_coords = (
            max(0, min(img_width, crop_coords[0])),
            max(0, min(img_height, crop_coords[1])),
            max(0, min(img_width, crop_coords[2])),
            max(0, min(img_height, crop_coords[3]))
        )

        self.push_undo()
        # Crop and display image filling canvas
        cropped_img = self.current_img.crop(crop_coords)
        self.display_img(cropped_img)

        self.original_img = cropped_img.copy()
        self.current_img = cropped_img.copy()

        # Cleanup: remove crop UI elements
        self.image_canvas.delete(self.crop_rect)
        for scaler in self.scalers:
            self.image_canvas.delete(scaler)
        self.confirm_crop_btn.destroy()

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
        # Update current_img
        self.current_img = current_img
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

    def push_undo(self):
        if self.current_img:
            slider_values = {feature: slider.get() for feature, slider in self.edit_panel.sliders.items()}
            self.undo_stack.append((
                self.original_img.copy(),
                self.current_img.copy(),
                slider_values))

    def undo(self):
        if self.undo_stack:
            last_original, last_current, last_sliders = self.undo_stack.pop()
            self.original_img = last_original
            self.display_img(last_current)

            # Temporarily disable slider callbacks
            self.edit_panel.disable_slider_callback = True
            for feature, value in last_sliders.items():
                self.edit_panel.sliders[feature].set(value)
            self.edit_panel.disable_slider_callback = False
        else:
            CTkMessagebox(title="Info", message="Nothing to undo")

    def save_img(self):
        if self.current_img:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg"), ("BMP files", "*.bmp")])
            if file_path:
                try:
                    # Get extension from file_path
                    ext = file_path.split('.')[-1].lower()
                    if ext not in ["png", "jpg", "jpeg", "bmp"]:
                        file_path += ".png"  # default to png if no valid extension

                    self.current_img.save(file_path)
                except Exception as e:
                    CTkMessagebox(title="Error", message=f"Failed to save image:\n{e}")
        else:
            CTkMessagebox(title="Warning", message="image not found")

    def toggle_edit_panel(self):
        if self.edit_panel.winfo_ismapped():
            self.edit_panel.grid_remove()
        else:
            self.edit_panel.grid(row=1, column=1, sticky="ns")

    def toggle_filter_panel(self):
        if self.filter_panel.winfo_ismapped():
            self.filter_panel.grid_remove()
            self.edit_panel.grid()
        else:
            if self.current_img:
                self.filter_panel.generate_thumbnails(self.current_img)
            self.filter_panel.grid(row=1, column=2, sticky="ns")
            self.edit_panel.grid_remove()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
