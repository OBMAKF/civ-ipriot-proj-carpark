import tkinter as tk


class CarBayDisplay(tk.Button):
    def __init__(self, window, bay: int, isle: int) -> None:
        super(CarBayDisplay, self).__init__(
            window, background='green', foreground='yellow',
            activebackground='grey', activeforeground='green',
            text=f"{bay}-{isle}", command=self.activate)
        self.location = (bay, isle)
        self.is_available = True

    def update(self) -> None:
        super().update()
        if self.is_available:
            self.configure(state='normal')
            return
        self.configure(state='disabled')

    def activate(self):
        if self.is_available:
            self.is_available = False
            self.master.activate(self.location)
            self.update()
