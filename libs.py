import tkinter as tk
from tkinter import Frame
from PIL import Image, ImageTk

BUTTON_FONT = ('Arial', 12, 'bold')
BUTTON_COLOR_PR = '#41cd52'

def button(frame: Frame, text, **kwargs)->tk.Button:
    return tk.Button(frame, text=text, width=25, font=BUTTON_FONT,
                     bg=BUTTON_COLOR_PR, fg='black', borderwidth=5, anchor=tk.CENTER, **kwargs)


def back_button(frame: Frame, **kwargs)->tk.Button:
    return tk.Button(frame, text="Back", font=BUTTON_FONT, anchor=tk.CENTER, width=12, **kwargs)


def activate_button(frame: Frame, text: str, **kwargs)->tk.Button:
    return tk.Button(frame, text=text, width=12, font=BUTTON_FONT,
                     bg=BUTTON_COLOR_PR, fg='black', anchor=tk.CENTER, borderwidth=2, **kwargs)

class BkgrndFrame(tk.Frame):
    def __init__(self, parent, width, height):
        file_path= "assets/bg.webp"
        super(BkgrndFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()

        pil_img = Image.open(file_path)
        self.img = ImageTk.PhotoImage(pil_img.resize((width, height), Image.ANTIALIAS))
        self.bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def add(self, widget:tk.Widget, x: float, y: float):
        canvas_window = self.canvas.create_window(x, y, anchor=tk.NW, window=widget)
        return widget
