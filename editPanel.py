import customtkinter as ctk

class EditPanel(ctk.CTkFrame):
    def __init__(self, master, main_app):
        super().__init__(master)
        self.main_app = main_app

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
        
        #  Buttons for crop, flip, rotate
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=len(self.features)*2, column=0, padx=10, pady=10, sticky="ew")
        button_frame.columnconfigure((0,1,2), weight=1)

        crop_btn = ctk.CTkButton(button_frame, text="Crop", width = 5)
        crop_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        flip_btn = ctk.CTkButton(button_frame, text="Flip", width = 5)
        flip_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        rotate_btn = ctk.CTkButton(button_frame, text="R", width = 5)
        rotate_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        rotate_btn = ctk.CTkButton(button_frame, text="R", width = 5)
        rotate_btn.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

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
        
    def apply_selected_filter(self):
        """Get selected filter from dropdown and call main app function."""
        filter_name = self.selected_filter.get().lower()  # convert to lowercase for backend function consistency
        self.main_app.apply_filter(filter_name)

    def on_slider_change(self, edits):
        # Called when any slider moves, send all slider values to main app
        values = {feature: slider.get() for feature, slider in self.sliders.items()}
        self.main_app.apply_edits(values)