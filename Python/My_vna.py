import tkinter as tk

window = tk.Tk()

label = tk.Label(
    text="Привет, Tkinter!",
    fg="white",
    bg="black",
    width=2000,
    height=2000
)

label.pack()
window.mainloop()