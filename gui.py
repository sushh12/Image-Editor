# gui.py
import customtkinter as ctk

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Image Editing Application")
        self.root.geometry("800x600")
        
        # self.editor = Editor()
        self.image = None
        
        # btn_frame Frame
        self.btn_frame = ctk.CTkFrame(self.root)
        self.btn_frame.pack(side="top", fill="x")
        
        # Open Button
        self.open_btn = ctk.CTkButton(self.btn_frame, text="Open", width=10).grid(row=0, column=0)
        # edit Button
        self.edit_btn = ctk.CTkButton(self.btn_frame, text="Edit", width=10, command=self.toggle_edit_panel).grid(row=0, column=1)
        # Save Button
        self.save_btn = ctk.CTkButton(self.btn_frame, text="Save", width=10).grid(row=0, column=2)
        
        
        # Image Display Frame
        self.image_frame = ctk.CTkFrame(self.root, fg_color="white")
        self.image_frame.pack(side="left", fill="both", expand=True)
        
        self.image_label = ctk.CTkLabel(self.image_frame, text="No Image Loaded")
        self.image_label.pack(expand=True)
        
        # Edit Panel Frame
        self.edit_panel = ctk.CTkFrame(self.root, width=200, fg_color="gray")
        self.edit_panel.pack(side="right", fill="y")
        # self.edit_panel.pack_forget()
		
    def toggle_edit_panel(self):
        if self.edit_panel.winfo_ismapped():
            self.edit_panel.pack_forget()
        else:
            self.edit_panel.pack(side='right', fill='y')
            
    def run(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    app = App()
    app.run()

