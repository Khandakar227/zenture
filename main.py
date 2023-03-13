import tkinter as tk
from tkinter import ttk
from libs import button, show_frame, back_button, activate_button

LARGEFONT =("Arial", 35)  
BG_COLOR = '#171A21'
# Which gesture control to use
mode = 0

def toggle_mode(new_mode, frame:tk.Frame):
    global mode
    
    mode = new_mode if mode != new_mode else 0

    print(mode)
    if mode == new_mode:
        frame.toggle_activate.config(text=f"Deactivate", bg='#5dff5d', fg='black')
    else: frame.toggle_activate.config(text=f"Activate", bg='#EA3A0D', fg='white')
    

class App(tk.Tk):     
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs): 
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.configure(bg=BG_COLOR)
        self.geometry('600x600')
        self.title('Zenture') 

        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(fill = "none", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (MainPage, DualHandPage, FullBodyPage, AircraftSteeringPage, SingleHandPage, RacingPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(MainPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent:tk.Frame, controller:App):
        tk.Frame.__init__(self, parent, bg=BG_COLOR, pady=50)

        dual_hand_btn = button(self, text='Dual hand gesture', command=lambda: controller.show_frame(DualHandPage))
        full_body_btn = button(self, text='Full body gesture', command=lambda: controller.show_frame(FullBodyPage))
        steering = button(self, text='Aircraft steering', command=lambda: controller.show_frame(AircraftSteeringPage))
        single_hand_btn = button(self, text='Single hand gesture', command=lambda: controller.show_frame(SingleHandPage))
        racing_btn = button(self, text='Racing', command=lambda: controller.show_frame(RacingPage))

        dual_hand_btn.pack(pady=15, padx=15)
        full_body_btn.pack(pady=15, padx=15)
        steering.pack(pady=15, padx=15)
        single_hand_btn.pack(pady=15, padx=15)
        racing_btn.pack(pady=15, padx=15)

class SubPage(tk.Frame):
    def __init__(self, parent:tk.Frame, controller:App):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        back = back_button(self, bg=BG_COLOR, fg='white', command=lambda:controller.show_frame(MainPage))
        back.pack(pady=15, padx=15, fill="both")

class DualHandPage(SubPage):
    def __init__(self, parent:tk.Frame, controller:App):
        super().__init__(parent, controller)
        self.toggle_activate = activate_button(self, "Activate", command=self.on_toggle_activate)
        self.toggle_activate.pack(pady=15, padx=15, fill="both")
    
    def on_toggle_activate(self):
        toggle_mode(1, self)        
        
        # Dual hand gesture code


class FullBodyPage(SubPage):     
    def __init__(self, parent:tk.Frame, controller:App):
        super().__init__(parent, controller)

        self.toggle_activate = activate_button(self, "Activate", command=self.on_toggle_activate)
        self.toggle_activate.pack(pady=15, padx=15, fill="both")
    
    def on_toggle_activate(self):
        toggle_mode(2, self)
        
        # Full body gesture code        


class AircraftSteeringPage(SubPage):     
    def __init__(self, parent:tk.Frame, controller:App):
        super().__init__(parent, controller)

        self.toggle_activate = activate_button(self, "Activate", command=self.on_toggle_activate)
        self.toggle_activate.pack(pady=15, padx=15, fill="both")
    
    def on_toggle_activate(self):
        toggle_mode(3, self)
        # aircraft hand gesture code
        


class SingleHandPage(SubPage):     
    def __init__(self, parent:tk.Frame, controller:App):
        super().__init__(parent, controller)

        self.toggle_activate = activate_button(self, "Activate", command=self.on_toggle_activate)
        self.toggle_activate.pack(pady=15, padx=15, fill="both")
    
    def on_toggle_activate(self):
        toggle_mode(4, self)
        # Single hand gesture code
        
        

class RacingPage(SubPage):     
    def __init__(self, parent:tk.Frame, controller:App):
        super().__init__(parent, controller)

        self.toggle_activate = activate_button(self, "Activate", command=self.on_toggle_activate)
        self.toggle_activate.pack(pady=15, padx=15, fill="both")
    
    def on_toggle_activate(self):
        toggle_mode(5, self)
        # Racing hand gesture code
        
        
        
app = App()
app.mainloop()