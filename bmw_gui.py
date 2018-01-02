from tkinter import *

root = Tk()

img1 = PhotoImage(file="D:/bmw.png")

lab1 = Label(root, image=img1)
butt1 = Button(root, text="wybierz")
lb = Listbox(root, height=5)
lb.insert(0, "abc")
lb.insert(0, "address-book")
lb.insert(0, "Seria 1", "Seria 3", "Seria 5", "Seria 7", "X3", "X5", "X6", "Z3", "Z4")

lab1.grid(row=0, column=0, sticky="wn")
butt1.grid(row=1, column=0)
lb.grid(row=0, column=1, rowspan=2)

root.mainloop()