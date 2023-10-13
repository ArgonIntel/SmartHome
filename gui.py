import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

class SmartHomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Home")
        self.geometry("700x620")
        self.resizable(False, False)
        
        self.create_widgets()
    
    def create_widgets(self):
        putanja = "photos/SmartHomePhoto.png"
        fotografija = Image.open(putanja)
        photo = ImageTk.PhotoImage(fotografija)
        self.background_label = tk.Label(self, image=photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.photo = photo
        
        smart_home_app_label = tk.Label(self, text='SMART HOME APP', background="white", fg="black", font=("Arial", 22))
        smart_home_app_label.place(relx=.5, rely=.96, width=420, height=30, anchor="center")

if __name__ == "__main__":
    app = SmartHomeApp()
    app.mainloop()
