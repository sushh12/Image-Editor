import customtkinter as ctk
from PIL import Image
class EditPanel(ctk.CTkFrame):
    def __init__(self, master, main_app):
        super().__init__(master)
        self.main_app = main_app

        self.debounce = None
        self.sliders = {}

        # List of edit features with their ranges and default values
        self.features = {
            "Brightness": (0.5, 1.5, 1.0),
            "Contrast": (0.5, 1.5, 1.0),
            "Exposure": (0.5, 1.5, 1.0),
            "Saturation": (0.0, 2.0, 1.0),
            "Highlights": (0.0, 1.0, 0.5),
            "Sharpness": (0.0, 2.0, 1.0),
        }

        for i, (feature, (min_val, max_val, default)) in enumerate(self.features.items()):
            label = ctk.CTkLabel(self, text=feature)
            label.grid(row=i*2, column=0, padx=10, pady=(5,0), sticky="w")

            slider = ctk.CTkSlider(self, from_=min_val, to=max_val, command=self.on_slider_change)
            slider.set(default)
            slider.grid(row=i*2+1, column=0, padx=10, pady=(0,5), sticky="ew")

            self.sliders[feature] = slider
        
        # Example loading icons
        crop_icon = ctk.CTkImage(Image.open("icons/crop.png"), size=(24,24))
        flip_icon = ctk.CTkImage(Image.open("icons/flip.png"), size=(24,24))
        rotateL_icon = ctk.CTkImage(Image.open("icons/rotate left.png"), size=(24,24))
        rotateR_icon = ctk.CTkImage(Image.open("icons/rotate right.png"), size=(24,24))
        
        #  Buttons for crop, flip, rotate
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=len(self.features)*2, column=0, padx=10, pady=10, sticky="ew")
        button_frame.columnconfigure((0,1,2), weight=1)

        crop_btn = ctk.CTkButton(button_frame, text="", image=crop_icon, width=5)
        crop_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        flip_btn = ctk.CTkButton(button_frame, text="", image=flip_icon, width=5, command=self.flip_image)
        flip_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        rotateL_btn = ctk.CTkButton(button_frame, text="", image=rotateL_icon, width=5, command=self.rotate_left)
        rotateL_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        rotateR_btn = ctk.CTkButton(button_frame, text="", image=rotateR_icon, width=5, command=self.rotate_right)
        rotateR_btn.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        

        # Filter section label
        filter_label = ctk.CTkLabel(self, text="Filters")
        filter_label.grid(row=20, column=0, padx=10, pady=(10,0), sticky="w")

        # Filter options list
        self.filter_options = ["None", "Grayscale", "Sepia", "Invert", "Blur", "Emboss", "Edge Enhance"]
        self.selected_filter = ctk.StringVar(value="None")

        # Filter dropdown (OptionMenu)
        self.filter_menu = ctk.CTkOptionMenu(self, values=self.filter_options, variable=self.selected_filter)
        self.filter_menu.grid(row=21, column=0, padx=10, pady=5, sticky="ew")

        # Apply Filter button
        apply_filter_btn = ctk.CTkButton(self, text="Apply Filter")
        apply_filter_btn.grid(row=22, column=0, padx=10, pady=5, sticky="ew")

        self.columnconfigure(0, weight=1)
    
    def crop_image(self):
        self.main_app.crop_image()

    def flip_image(self):
        self.main_app.flip_image()

    def rotate_left(self):
        self.main_app.rotate_image(90)

    def rotate_right(self):
        self.main_app.rotate_image(-90)
        
    def on_slider_change(self, values):
        if self.debounce:
            self.after_cancel(self.debounce)
        # Called when any slider moves, send all slider values to main app
        values = {feature: slider.get() for feature, slider in self.sliders.items()}
        self.main_app.apply_edits(values)
        
        # Wait 150 ms after slider stops moving to call apply_edits
        self.debounce_job = self.after(150, self.apply_edits_debounced)

    def apply_edits_debounced(self):
        values = {feature: slider.get() for feature, slider in self.sliders.items()}
        self.main_app.apply_edits(values)
        
    def reset_sliders(self):
    # """Reset all sliders to their default values."""
        for feature, slider in self.sliders.items():
            default = self.features[feature][2]  # get default value from features dict
            slider.set(default)