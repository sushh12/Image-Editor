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
            label.grid(row=i*2, column=0, padx=10, pady=(10,0), sticky="w")

            slider = ctk.CTkSlider(self, from_=min_val, to=max_val, command=self.on_slider_change)
            slider.set(default)
            slider.grid(row=i*2+1, column=0, padx=10, pady=(0,10), sticky="ew")

            self.sliders[feature] = slider

        self.columnconfigure(0, weight=1)

    def on_slider_change(self, edits):
        # Called when any slider moves, send all slider values to main app
        values = {feature: slider.get() for feature, slider in self.sliders.items()}
        self.main_app.apply_edits(values)
        
