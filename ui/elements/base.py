import customtkinter
from ui import app
from src import config

class Base(customtkinter.CTkFrame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master

        self.checkboxes = []
        keybinds = config.keybinds
        difficulties = config.difficulties
        versions = config.versions

        dropdown_frame = customtkinter.CTkFrame(self.root, fg_color='gray17')
        dropdown_frame.grid(row=0, column=0, padx=5, pady=5)

        controller_frame = customtkinter.CTkFrame(self.root, height=75, fg_color='gray17')
        controller_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        button_frame = customtkinter.CTkFrame(self.root)
        button_frame.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

        _width = 150

        self._controller(dropdown_frame, controller_frame, keybinds, _width)
        self._difficulty(dropdown_frame, difficulties, _width)
        self._version(dropdown_frame, versions, _width)
        self._buttons(button_frame, _width)

    def _controller(self, frame: customtkinter.CTkFrame, buttons: customtkinter.CTkFrame, keybinds, width: int):
        
        def _update_buttons(choice):

            self.checkboxes = []
            checkbox: customtkinter.CTkCheckBox
            for checkbox in buttons.winfo_children():
                checkbox.destroy()

            if choice == "None - Always On":
                customtkinter.CTkLabel(buttons, text=config.general['Default_Button']).pack()
            else:
                for i, option in enumerate(keybinds[choice]):
                    c = i // 4
                    r = i - (c*4)
                    var = customtkinter.BooleanVar()
                    checkbox = customtkinter.CTkCheckBox(buttons, text=option, variable=var)
                    checkbox.grid(row=r, column=c, pady=5)
                    self.checkboxes.append(var)

                for col in range(len(keybinds[choice]) // 4):
                    buttons.grid_columnconfigure(col, uniform="equal", weight=1)

        _update_buttons("None - Always On")

        customtkinter.CTkLabel(frame, text='Controller', fg_color="gray20", corner_radius=6).grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.controller = customtkinter.CTkOptionMenu(frame, values=list(keybinds), dynamic_resizing=False, width=width, command=_update_buttons)
        self.controller.grid(row=1, column=0, padx=5, pady=5)

    def _difficulty(self, frame: customtkinter.CTkFrame, difficulties, width: int):

        customtkinter.CTkLabel(frame, text='Difficulty', fg_color="gray20", corner_radius=6).grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        self.difficulty = customtkinter.CTkOptionMenu(frame, values=difficulties, dynamic_resizing=False, width=width)
        self.difficulty.set(difficulties[-1])
        self.difficulty.grid(row=1, column=1, padx=5, pady=5)

    def _version(self, frame: customtkinter.CTkFrame, versions, width: int):

        customtkinter.CTkLabel(frame, text='Version', fg_color="gray20", corner_radius=6).grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        self.version = customtkinter.CTkOptionMenu(frame, values=versions, dynamic_resizing=False, width=width)
        self.version.set(versions[1])
        self.version.grid(row=1, column=2, padx=5, pady=5)

    def _buttons(self, frame: customtkinter.CTkFrame, width: int):

        customtkinter.CTkButton(frame, text='Character', width=width, command=lambda: app.App._show(self.root, 'character')).grid(row=0, column=0, padx=5, pady=5)

        customtkinter.CTkButton(frame, text='Class', width=width, command=lambda: app.App._show(self.root, 'class')).grid(row=0, column=1, padx=5, pady=5)

        customtkinter.CTkButton(frame, text='Item', width=width, command=lambda: app.App._show(self.root, 'item')).grid(row=0, column=2, padx=5, pady=5)

        customtkinter.CTkButton(frame, text='Database', width=width, command=lambda: app.App._show(self.root, 'database')).grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(frame, text='Help', width=width, command=lambda: app.App._show(self.root, 'help')).grid(row=2, column=1, padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(frame, text='Discord', width=width, command=lambda: app.App.handleDiscord(self.root)).grid(row=2, column=2, padx=5, pady=5, sticky='nsew')