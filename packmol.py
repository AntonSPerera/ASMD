import subprocess
import os
import time
class Solvate:
    def __init__(self, solvent, solute, con, density, x,y,z,dir):
        self.dir = dir
        self.solvent= solvent
        self.solute =solute
        self.con= float(con)
        self.den= float(density)
        self.x = float(x)
        self.y= float(y)
        self.z = float(z)

        numberMolcues = int(self.con * (6.4e-20) * 6.02214e23 *((self.x * self.y * self.z)/(40*40*40)))
        numberSolvent = int(self.den * (6.4e-20)* 6.02214e23*((self.x * self.y * self.z)/(40*40*40)))
        subprocess.run(f"mkdir {self.dir}/{solvent}_{solute}Packmol", shell = True)


        with open(f'{self.dir}/{solvent}_{solute}Packmol/mixture.inp', 'a') as m:
            info = ["#", f"# A mixture of {self.solvent} and {self.solute}", "#", "tolerance 2.0", "filetype pdb", f"output {solvent}_{solute}Packmol/{self.solvent}_and_{self.solute}Mixture.pdb",
                    "", f"structure {self.solvent}_Solvent/{self.solvent}_Solvent.pdb", f"  number {numberSolvent}", f"  inside box 0. 0. 0. {self.x} {self.y} {self.z}", "end structure",
                    "", f"structure {self.solute}_Solute/{self.solute}_Solute.pdb", f"  number {numberMolcues}", f"  inside box 0. 0. 0. {self.x} {self.y} {self.z}", "end structure"]
            for lines in info:
                m.writelines(lines +"\n")

        while not os.path.isfile(f"{self.dir}/{solvent}_{solute}Packmol/mixture.inp"):
            time.sleep(1)
        conda_activate = f"source {self.dir}/miniconda3/bin/activate"
        packmol_cmd =f"packmol < {self.dir}/{solvent}_{solute}Packmol/mixture.inp"

        cmd = ["bash", "-c",
               f'{conda_activate} && {packmol_cmd}']
        subprocess.Popen(cmd).wait()







