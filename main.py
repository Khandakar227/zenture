import tkinter as tk
from PIL import Image, ImageTk
from libs import button, back_button, activate_button
import vrconsole as vr
import threading
import vr_sharing as vshare
from GAME_MODE import DUAL_HAND_MODE,FLIGHT_CONTROL_MODE,FULLBODY_MODE,RACING_MODE,SINGLE_HAND_MODE

LARGEFONT = ("Verdana", 20)
BG_COLOR = '#171A21'
game_mode = 0
game_ctrl_state = 0


def console_active():
    global game_mode
    global game_ctrl_state
    global console_active_thread
    vr.activate(game_mode, game_ctrl_state)
    console_active_thread = threading.Thread(target=console_active)


def exit_change_call():
    global exit_active_thread
    vr.exit_stat_change()
    exit_active_thread = threading.Thread(target=exit_change_call)


def vr_active_call():
    global vr_active_thread
    vshare.vr_mode_run()
    vr_active_thread = threading.Thread(target=vr_active_call)


def vr_deactive_call():
    global vr_deactive_thread
    vshare.vr_mode_exit()
    vr_deactive_thread = threading.Thread(target=vr_deactive_call)


console_active_thread = threading.Thread(target=console_active)
exit_active_thread = threading.Thread(target=exit_change_call)
vr_active_thread = threading.Thread(target=vr_active_call)
vr_deactive_thread = threading.Thread(target=vr_active_call)


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

        self.logo = tk.PhotoImage(file='assets/XENTURE_logo.png')
        self.iconphoto(False, self.logo)

        self.mode = tk.IntVar()
        self.configure(bg=BG_COLOR)
        self.geometry("1100x800")
        self.title('Xenture')
        # App bar at the top
        appbar = tk.Label(self, text="Xenture", font=('Arial', 16, 'bold'), bg='#4DAA57', padx=70, pady=15, borderwidth=5, anchor='w',)
        appbar.place( relwidth=1, x=0, y=0)
        # App logo in app bar
        app_icon_img = Image.open('assets/XENTURE_icon.png').resize((50, 50))
        img = ImageTk.PhotoImage(app_icon_img)
        app_icon = tk.Label(self, image = img, bg='#4DAA57')
        app_icon.image = img
        app_icon.place(x = 10, y = 6)

        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(anchor="c", fill="none", expand=True)

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
            frame.grid(sticky="nsew", row=0, column=0)

        self.show_frame(MainPage)

        # Status bar
        self.statusbar = tk.Label(self, text="No mode is active", fg="red", bg='black', font=(
            'Verdana', 11), relief=tk.SUNKEN, anchor="w")
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def on_change_mode(self, *args):
        global game_mode
        global console_active_thread
        if self.mode.get() == DUAL_HAND_MODE:
            self.statusbar.configure(
                text='Dual hand gesture is active', fg='lightgreen')
            print(self.mode.get())
            game_mode = self.mode.get()
            console_active_thread.start()

            # Dual hand gesture code

            pass

        elif self.mode.get() == FULLBODY_MODE:
            self.statusbar.configure(
                text='Full body gesture is active', fg='lightgreen')
            print(self.mode.get())
            game_mode = self.mode.get()
            console_active_thread.start()
            # Full body gesture code

            pass

        elif self.mode.get() == FLIGHT_CONTROL_MODE:
            self.statusbar.configure(
                text='Aircraft steering gesture is active', fg='lightgreen')
            print(self.mode.get())
            game_mode = self.mode.get()
            console_active_thread.start()
            # Aircraft steering code
            # vr.activate()
            pass
        elif self.mode.get() == SINGLE_HAND_MODE:
            self.statusbar.configure(
                text='Single hand gesture is active', fg='lightgreen')
            print(self.mode.get())
            game_mode = self.mode.get()
            console_active_thread.start()
            # Single Hand code
            pass
        elif self.mode.get() == RACING_MODE:
            self.statusbar.configure(
                text='Racing gesture is active', fg='lightgreen')
            print(self.mode.get())
            game_mode = self.mode.get()
            # console_active_thread.start()
            # Racing gesture code
            vr_active_thread.start()
            pass
        else:
            self.statusbar.configure(text='No mode is active', fg='red')
            print(self.mode.get())
            exit_active_thread.start()
            # No gesture code / deactivate


class MainPage(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: App):
        tk.Frame.__init__(self, parent, bg=BG_COLOR, pady=50)

        dual_hand_btn = button(self, text='Dual hand gesture',
                               command=lambda: controller.show_frame(DualHandPage))
        full_body_btn = button(self, text='Full body gesture',
                               command=lambda: controller.show_frame(FullBodyPage))
        steering = button(self, text='Flight control gesture',
                          command=lambda: controller.show_frame(AircraftSteeringPage))
        single_hand_btn = button(self, text='Single hand gesture',
                                 command=lambda: controller.show_frame(SingleHandPage))
        racing_btn = button(self, text='Racing',
                            command=lambda: controller.show_frame(RacingPage))

        tk.Label(self, text="", width=50, bg=BG_COLOR).grid(column=0)
        dual_hand_btn.grid(column=3, row=1, pady=15, padx=15)
        full_body_btn.grid(column=3, row=2, pady=15, padx=15)
        steering.grid(column=3, row=3, pady=15, padx=15)
        single_hand_btn.grid(column=3, row=4, pady=15, padx=15)
        racing_btn.grid(column=3, row=5, pady=15, padx=15)


class SubPage(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: App):

        self.page_mode = 0
        self.frame: tk.Frame
        # = tk.Label(self, text=self.title, bg=BG_COLOR, fg='white', font=LARGEFONT)
        self.titleLabel: tk.Label

        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        back = back_button(self, bg=BG_COLOR, fg='white',
                           command=lambda: controller.show_frame(MainPage))
        back.grid(row=0, column=0, pady=15, padx=15)

        self.toggle_activate = activate_button(
            self, "Activate", command=self.on_toggle_activate)
        self.toggle_activate.grid(
            row=0, column=5, pady=15, padx=15, sticky='nsew')

        self.reset_default_btn = activate_button(
            self, "Reset to default", command=self.on_toggle_activate)
        self.reset_default_btn.configure(bg="#cdb0ff", fg="#27138b")
        self.reset_default_btn.grid(
            row=2, column=5, pady=15, padx=15, sticky='nsew')
        
        self.vr_btn = button(self, text="ADD VR", command=lambda: self.on_vr_btn_clicked())
        self.vr_btn.configure(bg="#228CDB", fg="#27138b", width=15)
        self.vr_btn.grid(row=2, column=0, pady=15, padx=15, sticky='nsew')

    def on_toggle_activate(self):
        toggle_mode(self.page_mode, self.frame)

    def on_vr_btn_clicked(self):
        print("VR button clicked")
        # Run vr console code. pass any parameters if necessary
        # Use lambda for passing parameters
        pass

class DualHandPage(SubPage):
    def __init__(self, parent: tk.Frame, controller: App):
        super().__init__(parent, controller)
        self.page_mode = 1
        self.title = "Dual hand gesture control"
        self.frame = self
        self.titleLabel = tk.Label(
            self, text=self.title, bg=BG_COLOR, fg='white', font=LARGEFONT)
        self.titleLabel.grid(row=1, column=2, columnspan=2,
                             padx=15, pady=15, sticky='nsew')

        self.key_data = [
            {'name': 'up', 'key': 'W', 'label': 'UP'},
            {'name': 'down', 'key': 'S', 'label': 'DOWN'},
            {'name': 'left', 'key': 'A', 'label': 'LEFT'},
            {'name': 'right', 'key': 'S', 'label': 'RIGHT'},
            {'name': 'gun fire', 'key': 'left', 'label': 'GUN FIRE'},
            {'name': 'booster', 'key': 'right', 'label': 'BOOSTER'},
            {'name': 'missiles', 'key': 'up', 'label': 'FIRE MISSILES'},
            {'name': 'flares', 'key': 'down', 'label': 'DEPLOY FLARES'},
        ]
        self.keys = []
        for i, key in enumerate(self.key_data):
            btn = button(self, f"{key['label']}\n{key['key']}")
            btn.grid(row=4+i//4, column=1 + i %
                     4, pady=15, padx=15, sticky='nsew')
            btn.config(width=12, font=('Arial', 12))
            self.keys.append(btn)


class FullBodyPage(SubPage):
    def __init__(self, parent: tk.Frame, controller: App):
        super().__init__(parent, controller)
        self.page_mode = 2
        self.title = "Full body gesture control"
        self.frame = self
        self.titleLabel = tk.Label(
            self, text=self.title, bg=BG_COLOR, fg='white', font=LARGEFONT)
        self.titleLabel.grid(row=1, column=2, columnspan=2,
                             padx=15, pady=15, sticky='nsew')

        self.key_data = [
            {'name': 'up', 'key': 'W', 'label': 'UP'},
            {'name': 'down', 'key': 'S', 'label': 'DOWN'},
            {'name': 'left', 'key': 'A', 'label': 'LEFT'},
            {'name': 'right', 'key': 'S', 'label': 'RIGHT'},
            {'name': 'gun fire', 'key': 'left', 'label': 'GUN FIRE'},
            {'name': 'booster', 'key': 'right', 'label': 'BOOSTER'},
            {'name': 'missiles', 'key': 'up', 'label': 'FIRE MISSILES'},
            {'name': 'flares', 'key': 'down', 'label': 'DEPLOY FLARES'},
        ]

        self.keys = []
        for i, key in enumerate(self.key_data):
            btn = button(self, f"{key['label']}\n{key['key']}")
            btn.grid(row=4+i//4, column=1 + i %
                     4, pady=15, padx=15, sticky='nsew')
            btn.config(width=12, font=('Arial', 12))
            self.keys.append(btn)


class AircraftSteeringPage(SubPage):
    def __init__(self, parent: tk.Frame, controller: App):
        super().__init__(parent, controller)
        self.page_mode = 3
        self.title = "Flight control gesture"
        self.frame = self
        self.titleLabel = tk.Label(
            self, text=self.title, bg=BG_COLOR, fg='white', font=LARGEFONT)
        self.titleLabel.grid(row=1, column=2, columnspan=2,
                             padx=15, pady=15, sticky='nsew')

        tk.Label(self, text="Configure keys", bg=BG_COLOR, fg='white', font=(
            'Verdana', 16, 'bold')).grid(row=3, column=2, pady=15, padx=15, sticky='nsew')

        self.key_data = [
            {'name': 'up', 'key': 'W', 'label': 'UP'},
            {'name': 'down', 'key': 'S', 'label': 'DOWN'},
            {'name': 'left', 'key': 'A', 'label': 'LEFT'},
            {'name': 'right', 'key': 'S', 'label': 'RIGHT'},
            {'name': 'gun fire', 'key': 'left', 'label': 'GUN FIRE'},
            {'name': 'booster', 'key': 'right', 'label': 'BOOSTER'},
            {'name': 'missiles', 'key': 'up', 'label': 'FIRE MISSILES'},
            {'name': 'flares', 'key': 'down', 'label': 'DEPLOY FLARES'},
        ]
        self.keys = []
        for i, key in enumerate(self.key_data):
            btn = button(self, f"{key['label']}\n{key['key']}")
            btn.grid(row=4+i//4, column=1 + i %
                     4, pady=15, padx=15, sticky='nsew')
            btn.config(width=12, font=('Arial', 12))
            self.keys.append(btn)


class SingleHandPage(SubPage):
    def __init__(self, parent: tk.Frame, controller: App):
        super().__init__(parent, controller)
        self.page_mode = 4
        self.title = "Single hand gesture control"
        self.frame = self
        self.titleLabel = tk.Label(
            self, text=self.title, bg=BG_COLOR, fg='white', font=LARGEFONT)
        self.titleLabel.grid(row=1, column=2, columnspan=2,
                             padx=15, pady=15, sticky='nsew')

        self.key_data = [
            {'name': 'up', 'key': 'W', 'label': 'UP'},
            {'name': 'down', 'key': 'S', 'label': 'DOWN'},
            {'name': 'left', 'key': 'A', 'label': 'LEFT'},
            {'name': 'right', 'key': 'S', 'label': 'RIGHT'},
            {'name': 'gun fire', 'key': 'left', 'label': 'GUN FIRE'},
            {'name': 'booster', 'key': 'right', 'label': 'BOOSTER'},
            {'name': 'missiles', 'key': 'up', 'label': 'FIRE MISSILES'},
            {'name': 'flares', 'key': 'down', 'label': 'DEPLOY FLARES'},
        ]
        self.keys = []
        for i, key in enumerate(self.key_data):
            btn = button(self, f"{key['label']}\n{key['key']}")
            btn.grid(row=4+i//4, column=1 + i %
                     4, pady=15, padx=15, sticky='nsew')
            btn.config(width=12, font=('Arial', 12))
            self.keys.append(btn)


class RacingPage(SubPage):
    def __init__(self, parent: tk.Frame, controller: App):
        super().__init__(parent, controller)
        self.page_mode = 5
        self.title = "Racing gesture control"
        self.frame = self
        self.titleLabel = tk.Label(
            self, text=self.title, bg=BG_COLOR, fg='white', font=LARGEFONT)
        self.titleLabel.grid(row=1, column=2, columnspan=2,
                             padx=15, pady=15, sticky='nsew')


        self.key_data = [
            {'name': 'up', 'key': 'W', 'label': 'UP'},
            {'name': 'down', 'key': 'S', 'label': 'DOWN'},
            {'name': 'left', 'key': 'A', 'label': 'LEFT'},
            {'name': 'right', 'key': 'S', 'label': 'RIGHT'},
            {'name': 'gun fire', 'key': 'left', 'label': 'GUN FIRE'},
            {'name': 'booster', 'key': 'right', 'label': 'BOOSTER'},
            {'name': 'missiles', 'key': 'up', 'label': 'FIRE MISSILES'},
            {'name': 'flares', 'key': 'down', 'label': 'DEPLOY FLARES'},
        ]
        self.keys = []
        for i, key in enumerate(self.key_data):
            btn = button(self, f"{key['label']}\n{key['key']}")
            btn.grid(row=4+i//4, column=1 + i %
                     4, pady=15, padx=15, sticky='nsew')
            btn.config(width=12, font=('Arial', 12))
            self.keys.append(btn)


def on_change_mode(*args):
    global game_mode
    global mode
    global console_active_thread
    if mode.get() == 1:
        # Dual hand gesture code
        pass
    elif mode.get() == 2:
        # Full body gesture code
        pass
    elif mode.get() == 3:

        # Aircraft steering code
        pass
    elif mode.get() == 4:
        # Single Hand code
        pass
    elif mode.get() == 5:
        # Racing gesture code
        pass
    else:
        print(mode.get())
        # No gesture code / deactivate


app = App()
app.mainloop()
