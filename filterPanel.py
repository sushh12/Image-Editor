import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageEnhance

class FilterPanel(ctk.CTkFrame):
    def __init__(self, master, app, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = app
        self.filters = ["Original", "Punch", "Golden", "Cool Light", "B&W", "B&W High Contrast"]
        self.previews = {}
        self.tk_img = {}

        self.build_ui()
        self.generate_thumbnails()  # Generate placeholder thumbnails initially

    def build_ui(self):
        back_icon = ctk.CTkImage(Image.open("icons/back.png"), size=(24, 24))
        # Place back button once, outside loop
        self.back_btn = ctk.CTkButton(self, text="", image=back_icon, width=5, fg_color='transparent', hover_color="gray",
                      command=self.app.toggle_filter_panel).grid(row=0, column=0, columnspan=2, pady=5, sticky="nw")

        for i, filter_name in enumerate(self.filters):
            # filter label with preview
            lbl = ctk.CTkLabel(self, text=filter_name, compound="top")
            lbl.grid(row=i // 2 + 1, column=i % 2, padx=5, pady=5)
            lbl.bind("<Button-1>", lambda e, fn=filter_name: self.apply_filter(fn))
            self.previews[filter_name] = lbl

    def generate_thumbnails(self, img=None):
        # If no image is given, create a default placeholder
        if img is None:
            placeholder = Image.new("RGB", (80, 80), color="gray")
        else:
            placeholder = img.copy()
            placeholder.thumbnail((80, 80))

        for filter_name in self.filters:
            filtered = self.apply_filter_effect(placeholder.copy(), filter_name)
            tk_img = CTkImage(light_image=filtered, size=(80,80))
            self.tk_img[filter_name] = tk_img  # store reference to avoid garbage collection
            self.previews[filter_name].configure(image=tk_img)

    def apply_filter_effect(self, img, filter_name):
        if filter_name == "Original":
            return img
        elif filter_name == "Punch":
            img = ImageEnhance.Color(img).enhance(1.5)
            img = ImageEnhance.Contrast(img).enhance(1.2)
        elif filter_name == "Golden":
            r, g, b = img.split()
            r = r.point(lambda i: min(255, int(i * 1.1)))
            g = g.point(lambda i: min(255, int(i * 1.05)))
            img = Image.merge("RGB", (r, g, b))
        elif filter_name == "Cool Light":
            r, g, b = img.split()
            b = b.point(lambda i: min(255, int(i * 1.2)))
            img = Image.merge("RGB", (r, g, b))
        elif filter_name == "B&W":
            img = img.convert("L").convert("RGB")
        elif filter_name == "B&W High Contrast":
            img = img.convert("L")
            img = ImageEnhance.Contrast(img).enhance(2.0).convert("RGB")
        return img

    def apply_filter(self, filter_name):
        if filter_name == "Original":
            if self.app.original_img is not None:
                filtered = self.app.original_img.copy()
            else:
                return
        else:
            if self.app.current_img is None:
                return
            img = self.app.current_img.copy()
            filtered = self.apply_filter_effect(img, filter_name)

        self.app.display_img(filtered)
        self.app.current_img = filtered
