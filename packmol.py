import subprocess
import os
import time
import topology as top
class Solvate:
    def __init__(self, solvent, solute, con, density,solute2, solvent2, con2, den2, x,y,z,dir):
        self.dir = dir
        self.solvent= solvent
        self.solute =solute
        self.solvent2 = solvent2
        self.solute2 = solute2
        self.con= float(con)
        self.den= float(density)
        self.con2= float(con2)
        self.den2= float(den2)
        self.x = float(x)
        self.y= float(y)
        self.z = float(z)

        self.numberMolcues = int(self.con * (6.4e-20) * 6.02214e23 *((self.x * self.y * self.z)/(40*40*40)))
        self.numberSolvent = int(self.den * (6.4e-20)* 6.02214e23*((self.x * self.y * self.z)/(40*40*40)))
        self.numberMolcues2 = int(self.con2 * (6.4e-20) * 6.02214e23 * ((self.x * self.y * self.z) / (40 * 40 * 40)))
        self.numberSolvent2 = int(self.den2 * (6.4e-20) * 6.02214e23 * ((self.x * self.y * self.z) / (40 * 40 * 40)))

        subprocess.run(f"mkdir {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Packmol", shell = True)


        with open(f'{self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Packmol/mixture.inp', 'a') as m:
            info = ["#", f"# A mixture of {solvent},{solute},{solute2},{solvent2}", "#", "","tolerance 2.0", "filetype pdb", f"output {solvent}_{solute}_{solute2}_{solvent2}Packmol/{solvent}_{solute}_{solute2}_{solvent2}Mixture.pdb",
                    "", f"structure {self.solvent}_Solvent/{self.solvent}_Solvent.pdb", f"  number {self.numberSolvent}", f"  inside box 0. 0. 0. {self.x} {self.y} {self.z}", "end structure",
                    "", f"structure {self.solute}_Solute/{self.solute}_Solute.pdb", f"  number {self.numberMolcues}", f"  inside box 0. 0. 0. {self.x} {self.y} {self.z}", "end structure", ""                                                                                                                                                "",
                    f"structure {self.solvent2}_Solvent2/{self.solvent2}_Solvent2.pdb", f"  number {self.numberSolvent2}",
                    f"  inside box 0. 0. 0. {self.x} {self.y} {self.z}", "end structure",
                    "", f"structure {self.solute2}_Solute2/{self.solute2}_Solute2.pdb", f"  number {self.numberMolcues2}",
                    f"  inside box 0. 0. 0. {self.x} {self.y} {self.z}", "end structure"]
            for lines in info:
                m.writelines(lines +"\n")

        while not os.path.isfile(f"{self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Packmol/mixture.inp"):
            time.sleep(1)
        conda_activate = f"source {self.dir}/miniconda3/bin/activate"
        packmol_cmd =f"packmol < {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Packmol/mixture.inp"

        cmd = ["bash", "-c",
               f'{conda_activate} && {packmol_cmd}']
        subprocess.Popen(cmd).wait()
        self.to()
    def to(self):
        top.toopol(self.solvent, self.numberSolvent, self.solvent2, self.numberSolvent2, self.solute, self.numberMolcues, self.solute2, self.numberMolcues2, self.dir)









