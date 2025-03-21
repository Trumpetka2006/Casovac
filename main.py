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
    progress = 0

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
        self.graph_part = tk.Canvas(self, width=300, height=20)
        self.graph_part.grid(row=1, column=1)

        self.graph_total.create_arc(0, 0, 100, 100, extent=120, start=90)
        self.graph_total.create_arc(0, 0, 100, 100, extent=120, start=210)
        self.graph_total.create_arc(0, 0, 100, 100, extent=20, start=330)
        self.graph_part.create_rectangle(0, 0, 300, 120, fill="red")

        self.totatlTimer = tk.Label(self, text="Cas zkouzky")
        self.partTimer = tk.Label(self, text="Cas casti", bg="white")

        self.totatlTimer.grid(row=1, column=0)
        self.partTimer.grid(row=1, column=1)

        self.control = tk.LabelFrame(self, text="Ovládací panel")
        self.control.grid(row=2, column=1)

        self.start_pause = tk.Button(self.control, text="> / ||")
        self.start_pause.grid(row=0, column=0)

    def tick(self):
        self.clock.configure(text=str(datetime.datetime.now())[:19])

        self.graph_total.delete("all")
        self.graph_total.create_arc(0, 0, 100, 100, extent=self.progress, start=90)
        self.progress += 1

        self.after(1000, self.tick)


app = Application()
app.tick()
app.mainloop()
