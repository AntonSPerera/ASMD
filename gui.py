import tkinter as tk
import scriptMaker as m
import lig as l
import dft as dft
import waiting as wait
import chargeTrasnfer as transfer
import packmol as pack
import make_gro as gro
import subprocess


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

        a= subprocess.run("echo $PWD", shell=True, capture_output=True)
        self.curentDirectory = a.stdout.decode().strip("\n")
        self.SoluteSmiles = tk.Entry(self.window, fg="black", bg="white", width=50)

        self.Density = tk.Entry(self.window,fg="black", bg="white", width=50 )
        self.xdim =tk.Entry(self.window,fg="black", bg="white", width=50 )
        self.ydim=tk.Entry(self.window,fg="black", bg="white", width=50 )
        self.zdim=tk.Entry(self.window,fg="black", bg="white", width=50 )

        self.xdimLabel= tk.Label(self.window, text="x dimensions: ".ljust(20))
        self.ydimLabel = tk.Label(self.window, text="y dimensions: ".ljust(20))
        self.zdimLabel = tk.Label(self.window, text="z dimenisons: ".ljust(20))

        self.email= tk.Entry(self.window, fg="black", bg="white", width=50)

        self.emailLable= tk.Label(self.window, text="Email: ".ljust(20))

        self.labelDensity= tk.Label(self.window, text ="Desity of solvent(M)".ljust(20))

        self.SoluteName = tk.Entry(self.window, fg="black", bg="white", width=50)

        self.SolventSmiles = tk.Entry(self.window, fg="black", bg="white", width=50)

        self.Solname= tk.Entry(self.window, fg= "black", bg="white", width=50)

        self.concentration = tk.Entry(self.window, fg= "black", bg="white", width=50)

        self.labelSolute = tk.Label(self.window, text="Solute name (3 letters): ".ljust(20))

        self.labelSolvent= tk.Label(self.window, text="Solvent name (3 letters): ".ljust(20))

        self.labelConcentration= tk.Label(self.window, text ="Concentration(M): ".ljust(20))

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
        self.chargeCheck.grid(row=12, column=0)
        self.DFTCheck.grid(row=13, column=0)
        self.labelDensity.grid(row=6, column=0)

        self.user.grid(row=5, column=1)
        self.chargeEntry.grid(row=12, column=1)
        self.concentration.grid(row=4, column=1)
        self.Solname.grid(row=2, column=1)
        self.SoluteSmiles.grid(row=1, column=1)
        self.SolventSmiles.grid(row=3, column=1)
        self.SoluteName.grid(row=0, column=1)
        self.Density.grid(row=6, column= 1)

        self.xdim.grid(row=9, column=1)
        self.ydim.grid(row=10, column=1)
        self.zdim.grid(row=11, column=1)

        self.xdimLabel.grid(row=9, column=0)
        self.ydimLabel.grid(row=10, column=0)
        self.zdimLabel.grid(row=11, column=0)
        self.button.grid(row=15, column=0)

        self.email.grid(row=14, column=1)
        self.emailLable.grid(row=14, column=0)


        self.window.mainloop()

    def run(self):
        l.lig(self.SoluteSmiles.get(), self.SoluteName.get()[:3] +"_Solute", self.curentDirectory)
        l.lig(self.SolventSmiles.get(), self.Solname.get()[:3] +"_Solvent", self.curentDirectory)
        if self.dftV.get()==1:
            print("dft was selcted")
            self.script()
        else:
            print("dft not selcted")
            self.pack()
    def script(self):
        m.FIdel(self.SoluteName.get()[:3]+"_Solute", self.email.get(), self.curentDirectory)
        dft.sumbit(self.SoluteName.get()[:3]+"_Solute", self.user.get(), self.chargeEntry.get(), self.curentDirectory )
        wait.waiting(self.SoluteName.get()[:3]+"_Solute", self.curentDirectory)
        transfer.trans(self.SoluteName.get()[:3]+"_Solute", self.curentDirectory)

        m.FIdel(self.Solname.get()[:3] +"_Solvent", self.email.get(), self.curentDirectory)
        dft.sumbit(self.Solname.get()[:3] +"_Solvent", self.user.get(), self.chargeEntry.get(), "0", self.curentDirectory )
        wait.waiting(self.Solname.get()[:3] +"_Solvent", self.curentDirectory)
        transfer.trans(self.Solname.get()[:3] +"_Solvent", self.curentDirectory)
        self.pack()
    def pack(self):
        pack.Solvate(self.Solname.get()[:3], self.SoluteName.get()[:3], self.concentration.get(), self.Density.get(), self.xdim.get(),self.ydim.get(),self.zdim.get(), self.curentDirectory )
        gro.gro(self.Solname.get()[:3], self.SoluteName.get()[:3], self.curentDirectory, self.xdim.get(),self.ydim.get(),self.zdim.get())


GUI()

