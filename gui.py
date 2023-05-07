import tkinter as tk
import scriptMaker as m
import lig as l
import dft as dft
import waiting as wait
import chargeTrasnfer as transfer


class GUI:
    def __init__(self):
        self.window = tk.Tk()

        self.window.title('FastAtom')

        self.window.geometry('600x750')

        self.button = tk.Button(self.window,
                                text="Submit",
                                width=5,
                                height=1,
                                bg="gray",
                                fg="black", command=self.run)

        self.entry = tk.Entry(self.window, fg="black", bg="white", width=50)

        self.Mname = tk.Entry(self.window, fg="black", bg="white", width=50)

        self.label = tk.Label(self.window, text="Molecule name: ")

        self.lable2 = tk.Label(self.window, text="SMILES code:")

        self.user = tk.Entry(self.window, fg="black", bg="white", width=50)

        self.user_label = tk.Label(self.window, text="user id")

        self.chargeV = tk.IntVar()

        self.charge = tk.Checkbutton(self.window, text="Charge", variable=self.chargeV)

        self.cha = tk.Entry(self.window, fg="black", bg="white", width=50)

        self.dft = tk.IntVar()

        self.DFT = tk.Checkbutton(self.window, text="DFT", variable=self.dft)

        self.DFT.grid(row=6, column=0)

        self.entry.grid(row=0, column=1)

        self.lable2.grid(row=0, column=0)

        self.label.grid(row=2, column=0)

        self.Mname.grid(row=2, column=1)

        self.button.grid(row=7, column=0)

        self.user.grid(row=4, column=1)

        self.user_label.grid(row=4, column=0)

        self.charge.grid(row=5, column=0)

        self.cha.grid(row=5, column=1)

        self.window.mainloop()

    def run(self):
        l.lig(self.entry.get(), self.Mname.get())
        if self.dft.get()==1:
            print("dft was selcted")
            self.script()
        else:
            print("dft not selcted")
    def script(self):
        m.FIdel(self.Mname.get())
        dft.sumbit(self.Mname.get(), self.user.get(), self.cha.get() )
        wait.waiting(self.Mname.get())
        transfer.trans(self.Mname.get())

GUI()
