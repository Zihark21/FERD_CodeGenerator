import tkinter
import customtkinter

class CustomCombobox(customtkinter.CTkComboBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dropdown = None
        self.all_values = self._values
        self.current_values = self.all_values

        self.bind("<KeyRelease>", self.update_text)
        self.set('')

    def _open_dropdown_menu(self, open=True):

        for widget in self.winfo_children():
            if isinstance(widget, tkinter.Toplevel):
                widget.destroy()
        
        self.dropdown = ListboxDropdown(self, values=self.current_values, command=self._dropdown_callback)
        
        self.dropdown.update_values(self.current_values)
        x, y = self.winfo_rootx(), self.winfo_rooty() + self.winfo_height()

        if open:
            self.dropdown.open(x, y)

    def update_text(self, event, open=True):
        current_text = self.get()
        if current_text:
            filtered_values = [val for val in self.all_values if current_text.lower() in val.lower()]
            self.current_values = filtered_values if filtered_values else self.all_values
        else:
            self.current_values = self.all_values

        self._open_dropdown_menu(open)

    def _dropdown_callback(self, value):
        self.set(value)
        if self.dropdown:
            self.dropdown.destroy()
            self.dropdown = None

class ListboxDropdown(tkinter.Toplevel):
    def __init__(self, master, values, command):
        super().__init__(master)
        self.master = master
        self.values = values
        self.command = command

        self.overrideredirect(True)
        self.lift()
        self.withdraw()

        self.listbox = tkinter.Listbox(self, height=min(15, len(values)), width=len(max(values, key=len)), activestyle="none")
        self.listbox.configure(bg="gray17", fg="white", font=customtkinter.CTkFont, selectbackground="gray", selectforeground="black")
        self.listbox.pack(fill="both", expand=True)

        self.populate_listbox()
        self.bindings()

    def populate_listbox(self):
        self.listbox.delete(0, tkinter.END)
        for value in self.values:
            self.listbox.insert(tkinter.END, value)

    def update_values(self, new_values):
        self.values = new_values
        self.listbox.delete(0, tkinter.END)
        for value in self.values:
            self.listbox.insert(tkinter.END, value)
        self.listbox.config(width=len(max(self.values, key=len)), height=min(15, len(self.values)))

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            value = self.listbox.get(selected_index[0])
            self.command(value)
        self.destroy()

    def bindings(self):
        self.listbox.bind("<ButtonRelease-1>", self.on_select)
        self.listbox.bind("<Return>", self.on_select)
        self.bind_all("<Button-1>", self.close, add="+")
        self.bind_all("<Escape>", self.close, add="+")
        self.unbind('<Button-1>')

    def open(self, x, y):
        self.geometry(f"+{x}+{y}")
        self.deiconify()

    def close(self, event):
        parent_name = str(self).split('.!')
        widget_name = str(event.widget).split('.!')
        try:
            if len(widget_name) == 2 or parent_name[2] != widget_name[2]:
                super().destroy()
                self.unbind_all("<Button-1>")
                self.unbind_all("<Escape>")
        except:
            pass