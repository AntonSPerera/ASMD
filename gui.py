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

        self.SoluteSmiles = tk.Entry(self.window, fg="black", bg="white", width=50)

        self.SoluteName = tk.Entry(self.window, fg="black", bg="white", width=50)

        self.SolventSmiles = tk.Entry(self.window, fg="black", bg="white", width=50)

        self.Solname= tk.Entry(self.window, fg= "black", bg="white", width=50)

        self.concentration = tk.Entry(self.window, fg= "black", bg="white", width=50)

        self.labelSolute = tk.Label(self.window, text="Solute name: ".ljust(20))

        self.labelSolvent= tk.Label(self.window, text="Solvent name: ".ljust(20))

        self.labelConcentration= tk.Label(self.window, text ="Concentration: ".ljust(20))

        self.lableSolventSmiles = tk.Label(self.window, text="Solvent SMILES code:".ljust(20))

        self.labelSoluteSmiles = tk.Label(self.window, text= "Solute SMILES code: ".ljust(20))

        self.user = tk.Entry(self.window, fg="black", bg="white", width=50)

        self.user_label = tk.Label(self.window, text="User ID")

        self.chargeV = tk.IntVar()

        self.chargeCheck = tk.Checkbutton(self.window, text="Charge on the Solute", variable=self.chargeV)

        self.chargeEntry = tk.Entry(self.window, fg="black", bg="white", width=50)

        self.dftV = tk.IntVar()

        self.DFTCheck = tk.Checkbutton(self.window, text="DFT", variable=self.dftV)

        self.labelSolute.grid(row=0, column=0)
        self.labelSoluteSmiles.grid(row=1, column=0)
        self.labelSolvent.grid(row=2, column=0)
        self.lableSolventSmiles.grid(row=3, column=0)
        self.labelConcentration.grid(row=4, column=0)
        self.user_label.grid(row=5, column=0)
        self.chargeCheck.grid(row=6, column=0)
        self.DFTCheck.grid(row=7, column=0)

        self.user.grid(row=5, column=1)
        self.chargeEntry.grid(row=6, column=1)
        self.concentration.grid(row=4, column=1)
        self.Solname.grid(row=2, column=1)
        self.SoluteSmiles.grid(row=1, column=1)
        self.SolventSmiles.grid(row=3, column=1)
        self.SoluteName.grid(row=0, column=1)

        self.button.grid(row=10, column=0)

        self.window.mainloop()

    def run(self):
        l.lig(self.SoluteSmiles.get(), "Solute_" +self.SoluteName.get())
        l.lig(self.SolventSmiles.get(), "Solvent_" +self.Solname.get())
        if self.dftV.get()==1:
            print("dft was selcted")
            self.script()
        else:
            print("dft not selcted")
    def script(self):
        m.FIdel("Solute_" +self.SoluteName.get())
        dft.sumbit("Solute_" +self.SoluteName.get(), self.user.get(), self.chargeEntry.get() )
        wait.waiting("Solute_" +self.SoluteName.get())
        transfer.trans("Solute_" +self.SoluteName.get())

        m.FIdel("Solvent_" +self.Solname.get())
        dft.sumbit("Solvent_" + self.Solname.get(), self.user.get(), "0" )
        wait.waiting("Solvent_" +self.Solname.get())
        transfer.trans("Solvent_" +self.Solname.get())

GUI()
