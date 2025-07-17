import customtkinter as ctk
from PIL import Image

class EditPanel(ctk.CTkFrame):
    def __init__(self, master, main_app):
        super().__init__(master)
        self.main_app = main_app

        self.debounce_job = None
        self.sliders = {}
        self.disable_slider_callback = False

        self.features = {
            "Brightness": (0.5, 1.5, 1.0),
            "Contrast": (0.5, 1.5, 1.0),
            "Exposure": (0.5, 1.5, 1.0),
            "Saturation": (0.0, 2.0, 1.0),
            "Highlights": (0.0, 1.0, 0.5),
        }

        # Create sliders
        for i, (feature, (min_val, max_val, default)) in enumerate(self.features.items()):
            ctk.CTkLabel(self, text=feature).grid(row=i * 2, column=0, padx=10, pady=(5, 0), sticky="w")
            slider = ctk.CTkSlider(self, from_=min_val, to=max_val, command=self.on_slider_change)
            slider.set(default)
            slider.grid(row=i * 2 + 1, column=0, padx=10, pady=(0, 5), sticky="ew")
            self.sliders[feature] = slider

        # Load icons
        crop_icon = ctk.CTkImage(Image.open("icons/crop.png"), size=(24, 24))
        flip_icon = ctk.CTkImage(Image.open("icons/flip.png"), size=(24, 24))
        rotateL_icon = ctk.CTkImage(Image.open("icons/rotate left.png"), size=(24, 24))
        rotateR_icon = ctk.CTkImage(Image.open("icons/rotate right.png"), size=(24, 24))

        # Buttons for crop, flip, rotate
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=len(self.features) * 2, column=0, padx=10, pady=10, sticky="ew")
        button_frame.columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkButton(button_frame, text="", image=crop_icon, width=5, command=self.main_app.toggle_crop_mode).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="", image=flip_icon, width=5, command=self.main_app.flip_image).grid(row=0,column=1,padx=5,pady=5,sticky="ew")
        ctk.CTkButton(button_frame, text="", image=rotateL_icon, width=5, command=self.rotate_left).grid(row=0,column=2,padx=5, pady=5,sticky="ew")
        ctk.CTkButton(button_frame, text="", image=rotateR_icon, width=5, command=self.rotate_right).grid(row=0,column=3,padx=5,pady=5,sticky="ew")
        ctk.CTkButton(button_frame, text="Filters", width=10, command=self.main_app.toggle_filter_panel).grid(row=1, column=1, sticky="ew")

    def rotate_left(self):
        self.main_app.rotate_image(90)

    def rotate_right(self):
        self.main_app.rotate_image(-90)

    def on_slider_change(self, values):
        if self.disable_slider_callback:
            return
        if self.debounce_job:
            self.after_cancel(self.debounce_job)
        values = {feature: slider.get() for feature, slider in self.sliders.items()}
        self.main_app.apply_edits(values)
        self.debounce_job = self.after(150, self.apply_edits_debounced)

    def apply_edits_debounced(self):
        values = {feature: slider.get() for feature, slider in self.sliders.items()}
        self.main_app.apply_edits(values)

    def reset_sliders(self):
        for feature, slider in self.sliders.items():
            slider.set(self.features[feature][2])