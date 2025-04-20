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

        dropdown_frame = customtkinter.CTkFrame(self.root, fg_color='transparent', bg_color='transparent')
        dropdown_frame.grid_columnconfigure([0,1,2], weight=1, uniform="equal")
        dropdown_frame.pack(padx=5, pady=5, fill='x')

        controller_frame = customtkinter.CTkFrame(self.root, height=75, fg_color='gray20', bg_color='transparent')
        controller_frame.pack(padx=5, pady=0, fill='x')

        button_frame = customtkinter.CTkFrame(self.root, fg_color='transparent', bg_color='transparent')
        button_frame.pack(padx=5, pady=5, fill='x')

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

        customtkinter.CTkLabel(frame, text='Controller', fg_color="gray20", corner_radius=6).grid(row=0, column=0, sticky='ew')

        self.controller = customtkinter.CTkOptionMenu(frame, values=list(keybinds), dynamic_resizing=False, width=width, command=_update_buttons)
        self.controller.grid(row=1, column=0, sticky='ew', pady=(5,0))

    def _difficulty(self, frame: customtkinter.CTkFrame, difficulties, width: int):

        customtkinter.CTkLabel(frame, text='Difficulty', fg_color="gray20", corner_radius=6).grid(row=0, column=1, sticky='ew', padx=5)

        self.difficulty = customtkinter.CTkOptionMenu(frame, values=difficulties, dynamic_resizing=False, width=width)
        self.difficulty.set(difficulties[-1])
        self.difficulty.grid(row=1, column=1, sticky='ew', padx=5, pady=(5,0))

    def _version(self, frame: customtkinter.CTkFrame, versions, width: int):

        customtkinter.CTkLabel(frame, text='Version', fg_color="gray20", corner_radius=6).grid(row=0, column=2, sticky='ew')

        self.version = customtkinter.CTkOptionMenu(frame, values=versions, dynamic_resizing=False, width=width)
        self.version.set(versions[1])
        self.version.grid(row=1, column=2, sticky='ew', pady=(5,0))

    def _buttons(self, frame: customtkinter.CTkFrame, width: int):

        row1 = customtkinter.CTkFrame(frame, fg_color='transparent', bg_color='transparent')
        row1.grid_columnconfigure([0,1,2], weight=1, uniform="equal")

        customtkinter.CTkButton(row1, text='Character', width=width, command=lambda: app.App._show(self.root, 'character')).grid(row=0, column=0, sticky='ew')

        customtkinter.CTkButton(row1, text='Class', width=width, command=lambda: app.App._show(self.root, 'class')).grid(row=0, column=1, sticky='ew', padx=5)

        customtkinter.CTkButton(row1, text='Item', width=width, command=lambda: app.App._show(self.root, 'item')).grid(row=0, column=2, sticky='ew')

        row2 = customtkinter.CTkFrame(frame, fg_color='transparent', bg_color='transparent')
        row2.grid_columnconfigure([0,1], weight=1, uniform="equal")

        customtkinter.CTkButton(row2, text='Selected', width=width, command=lambda: app.App._show(self.root, 'selected')).grid(row=0, column=0, sticky='ew')

        customtkinter.CTkButton(row2, text='Database', width=width, command=lambda: app.App._show(self.root, 'database')).grid(row=0, column=1, sticky='ew', padx=(5,0))

        row3 = customtkinter.CTkFrame(frame, fg_color='transparent', bg_color='transparent')
        row3.grid_columnconfigure([0,1], weight=1, uniform="equal")

        customtkinter.CTkButton(row3, text='Help', width=width, command=lambda: app.App._show(self.root, 'help')).grid(row=0, column=0, sticky='ew')

        customtkinter.CTkButton(row3, text='Discord', width=width, command=lambda: app.App.handleDiscord(self.root)).grid(row=0, column=1, sticky='ew', padx=(5,0))

        row1.pack(fill='x')
        row2.pack(fill='x', pady=5)
        row3.pack(fill='x')