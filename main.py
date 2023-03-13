import tkinter as tk
# from tkinter import ttk
from libs import button, back_button, activate_button

LARGEFONT = ("Arial", 35)
BG_COLOR = '#171A21'


def toggle_mode(new_mode, frame: tk.Frame):
    global mod
    app.mode.set(new_mode if app.mode.get() != new_mode else 0)
    print(app.mode.get())
    if app.mode.get() == new_mode:
        frame.toggle_activate.config(
            text=f"Deactivate", bg='#EA3A0D', fg='white')
    else:
        frame.toggle_activate.config(
            text=f"Activate", bg='#5dff5d', fg='black')


class App(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.mode = tk.IntVar()
        self.configure(bg=BG_COLOR)
        self.geometry('600x600')
        self.title('Zenture')

        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(fill="none", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # An auto update variable for gesture mode
        # Which gesture control to use
        self.mode.initialize(0)
        self.mode.trace('w', self.on_change_mode)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (MainPage, DualHandPage, FullBodyPage, AircraftSteeringPage, SingleHandPage, RacingPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage)

        # Status bar
        self.statusbar = tk.Label(self, text="No mode is active", fg="red", bg='black', font=('Verdana', 11), relief=tk.SUNKEN, anchor="w")
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def on_change_mode(self, *args):
        if self.mode.get() == 1:
            self.statusbar.configure(text='Dual hand gesture is active', fg='lightgreen')
            print(self.mode.get())
            
            # Dual hand gesture code
            
            pass
        
        elif self.mode.get() == 2:
            self.statusbar.configure(text='Full body gesture is active', fg='lightgreen')
            print(self.mode.get())
        
            # Full body gesture code
        
            pass
        
        elif self.mode.get() == 3:
            self.statusbar.configure(text='Aircraft steering gesture is active', fg='lightgreen')
            print(self.mode.get())
            # Aircraft steering code
            pass
        elif self.mode.get() == 4:
            self.statusbar.configure(text='Single hand gesture is active', fg='lightgreen')
            print(self.mode.get())
            # Single Hand code
            pass
        elif self.mode.get() == 5:
            self.statusbar.configure(text='Racing gesture is active', fg='lightgreen')
            print(self.mode.get())
            # Racing gesture code
            pass
        else:
            self.statusbar.configure(text='No mode is active', fg='red')
            print(self.mode.get())
            # No gesture code / deactivate


class MainPage(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: App):
        tk.Frame.__init__(self, parent, bg=BG_COLOR, pady=50)

        dual_hand_btn = button(self, text='Dual hand gesture',
                               command=lambda: controller.show_frame(DualHandPage))
        full_body_btn = button(self, text='Full body gesture',
                               command=lambda: controller.show_frame(FullBodyPage))
        steering = button(self, text='Aircraft steering',
                          command=lambda: controller.show_frame(AircraftSteeringPage))
        single_hand_btn = button(self, text='Single hand gesture',
                                 command=lambda: controller.show_frame(SingleHandPage))
        racing_btn = button(self, text='Racing',
                            command=lambda: controller.show_frame(RacingPage))

        dual_hand_btn.grid(column=0, row=1, pady=15, padx=15)
        full_body_btn.grid(column=0, row=2, pady=15, padx=15)
        steering.grid(column=0, row=3, pady=15, padx=15)
        single_hand_btn.grid(column=0, row=4, pady=15, padx=15)
        racing_btn.grid(column=0, row=5, pady=15, padx=15)


class SubPage(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: App):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        back = back_button(self, bg=BG_COLOR, fg='white',
                           command=lambda: controller.show_frame(MainPage))
        back.pack(pady=15, padx=15, fill="both")


class DualHandPage(SubPage):
    def __init__(self, parent: tk.Frame, controller: App):
        super().__init__(parent, controller)
        self.toggle_activate = activate_button(
            self, "Activate", command=self.on_toggle_activate)
        self.toggle_activate.pack(pady=15, padx=15, fill="both")

    def on_toggle_activate(self):
        toggle_mode(1, self)


class FullBodyPage(SubPage):
    def __init__(self, parent: tk.Frame, controller: App):
        super().__init__(parent, controller)

        self.toggle_activate = activate_button(
            self, "Activate", command=self.on_toggle_activate)
        self.toggle_activate.pack(pady=15, padx=15, fill="both")

    def on_toggle_activate(self):
        toggle_mode(2, self)


class AircraftSteeringPage(SubPage):
    def __init__(self, parent: tk.Frame, controller: App):
        super().__init__(parent, controller)

        self.toggle_activate = activate_button(
            self, "Activate", command=self.on_toggle_activate)
        self.toggle_activate.pack(pady=15, padx=15, fill="both")

    def on_toggle_activate(self):
        toggle_mode(3, self)


class SingleHandPage(SubPage):
    def __init__(self, parent: tk.Frame, controller: App):
        super().__init__(parent, controller)

        self.toggle_activate = activate_button(
            self, "Activate", command=self.on_toggle_activate)
        self.toggle_activate.pack(pady=15, padx=15, fill="both")

    def on_toggle_activate(self):
        toggle_mode(4, self)


class RacingPage(SubPage):
    def __init__(self, parent: tk.Frame, controller: App):
        super().__init__(parent, controller)

        self.toggle_activate = activate_button(
            self, "Activate", command=self.on_toggle_activate)
        self.toggle_activate.pack(pady=15, padx=15, fill="both")

    def on_toggle_activate(self):
        toggle_mode(5, self)


def on_change_mode(*args):
    global mode
    if mode.get() == 1:
        print(mode.get())
        # Dual hand gesture code
        pass
    elif mode.get() == 2:
        print(mode.get())
        # Full body gesture code
        pass
    elif mode.get() == 3:
        print(mode.get())
        # Aircraft steering code
        pass
    elif mode.get() == 4:
        print(mode.get())
        # Single Hand code
        pass
    elif mode.get() == 5:
        print(mode.get())
        # Racing gesture code
        pass
    else:
        print(mode.get())
        # No gesture code / deactivate


app = App()
app.mainloop()
