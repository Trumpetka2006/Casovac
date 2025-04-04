#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
import datetime

# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if "textvariable" not in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Foo"

    totalTimeLeft = 20 * 60
    partTimeLeft = 6 * 60 + 40
    parts = [partTimeLeft, partTimeLeft, partTimeLeft]
    progress = 2
    colors = ("red", "green", "blue")
    running = False

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.clock = tk.Label(self, text="1984")
        self.clock.grid(row=0, column=1, rowspan=1)
        self.totatlTimer = tk.Label(self, text="Cas zkouzky")
        self.partTimer = tk.Label(self, text="Cas casti")

        self.graph_total = tk.Canvas(self, width=100, height=100)
        self.graph_total.grid(row=1, column=0)
        self.graph_part = tk.Canvas(self, width=300, height=30)
        self.graph_part.grid(row=1, column=1)

        self.graph_total.create_arc(0, 0, 100, 100, extent=120, start=90)
        self.graph_total.create_arc(0, 0, 100, 100, extent=120, start=210)
        self.graph_total.create_arc(0, 0, 100, 100, extent=120, start=330)
        self.graph_part.create_rectangle(0, 0, 300, 29, fill="red")

        self.totatlTimer = tk.Label(self, text="Cas zkouzky")
        self.partTimer = tk.Label(self, text="Cas casti")

        self.totatlTimer.grid(row=1, column=0)
        self.partTimer.grid(row=1, column=1)

        self.control = tk.LabelFrame(self, text="Ovládací panel")
        self.control.grid(row=2, column=1)

        self.start_pause = tk.Button(
            self.control, text="Spustit", command=self.pause_run
        )
        self.new_part = tk.Button(self.control, text="Nová část", command=self.n_part)
        self.repeat_part = tk.Button(
            self.control, text="Opakovat část", command=self.r_part, state="disabled"
        )
        self.new_exeam = tk.Button(
            self.control, text="Nová zkoužka", command=self.n_exeam
        )

        self.start_pause.grid(row=0, column=0, sticky="WE")
        self.new_part.grid(row=1, column=0, sticky="WE")
        self.repeat_part.grid(row=1, column=1, sticky="WE")
        self.new_exeam.grid(row=2, column=0, sticky="WE")

    def pause_run(self, event=None):
        self.running = not self.running
        if self.running:
            self.start_pause.configure(text="Pozastavit")
            self.repeat_part.configure(state="disabled")
            self.new_exeam.configure(state="disabled")
            self.new_part.configure(state="disabled")
        else:
            self.start_pause.configure(text="Spustit")
            self.repeat_part.configure(state="active")
            self.new_exeam.configure(state="active")
            if self.progress != 0:
                self.new_part.configure(state="active")

    def n_part(self, event=None):
        self.parts[self.progress] = 0
        self.progress -= 1
        self.update_timer()

        if self.progress == 0:
            self.new_part.configure(state="disabled")
        self.repeat_part.configure(state="disabled")

    def r_part(self, event=None):
        self.parts[self.progress] = 6 * 60 + 40
        self.update_timer()
        self.repeat_part.configure(state="disabled")

    def n_exeam(self, event=None):
        for i in range(3):
            self.parts[i] = 6 * 60 + 40
        self.progress = 2
        self.new_part.configure(state="active")
        self.start_pause.configure(state="active")
        self.repeat_part.configure(state="active")

    def update_timer(self):
        self.totalTimeLeft = 0
        for part in self.parts:
            self.totalTimeLeft += part

    def tick(self):
        self.clock.configure(text=str(datetime.datetime.now())[:19])

        if self.running:
            self.parts[self.progress] -= 1
            if self.parts[self.progress] == 0:
                self.pause_run()
                self.repeat_part.configure(state="disabled")
                if self.progress == 0:
                    self.start_pause.configure(state="disabled")
                    self.new_part.configure(state="disabled")
                    self.repeat_part.configure(state="disabled")
                self.n_part()
            self.update_timer()

        self.graph_total.delete("all")
        for i in range(3):
            self.graph_total.create_arc(
                0,
                0,
                100,
                100,
                extent=self.parts[i] / (6 * 60 + 40) * 120,
                start=90 + 120 * i,
                fill=self.colors[i],
            )

        self.graph_part.delete("all")
        self.graph_part.create_rectangle(
            0,
            0,
            self.parts[self.progress] / (6 * 60 + 40) * 300,
            29,
            fill=self.colors[self.progress],
        )
        self.partTimer.configure(
            text=f"{int(self.parts[self.progress] / 60)}:{self.parts[self.progress] % 60}"
        )

        self.totatlTimer.configure(
            text=f"{int(self.totalTimeLeft / 60)}:{self.totalTimeLeft % 60}"
        )

        self.after(10, self.tick)


app = Application()
app.tick()
app.mainloop()
