import tkinter as tk
from tkinter import Frame

BUTTON_FONT = ('Arial', 12, 'bold')

def button(frame: Frame, text, **kwargs):
    return tk.Button(frame, text=text, width=25, font=BUTTON_FONT,
                     bg='#5dff5d', fg='black', borderwidth=5, anchor=tk.CENTER, **kwargs)

def back_button(frame: Frame, **kwargs):
    return tk.Button(frame, text="Back", font=BUTTON_FONT, anchor=tk.CENTER, **kwargs)

def activate_button(frame: Frame, text:str, **kwargs):
    return tk.Button(frame, text=text, width=25, font=BUTTON_FONT,
                     bg='#EA3A0D', fg='white', anchor=tk.CENTER, borderwidth=2, **kwargs)

def show_frame(frame: Frame):
    print(frame)
    frame.tkraise()
