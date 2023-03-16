import tkinter as tk
from tkinter import Frame

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
