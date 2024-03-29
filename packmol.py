import subprocess
import os
import time
import topology as top
class Solvate:
    def __init__(self, solvent, solute, con, density, solvent2, den2, x,y,z,di, ratio):
        self.dir = di
        self.solvent= solvent
        self.solvent2 = solvent2
        self.solutes = solute
        self.con= con
        self.den= float(density)
        try:
            self.den2=float(den2)
        except:
            self.den2=''
        try:
            self.ratio=float(ratio)
        except:
            self.ratio = 1
        self.x = 10*float(x)
        self.y= 10*float(y)
        self.z = 10*float(z)

        self.numberSolvent = int(self.den * (6.4e-20)* 6.02214e23*(((self.x/10) * (self.y/10) * (self.z/10))/(40*40*40)))
        try:
            self.numberSolvent2 = int(self.den2 * (6.4e-20)* 6.02214e23*(((self.x/10) * (self.y/10) * (self.z/10))/(40*40*40))* self.ratio)
        except:
            self.numberSolvent2 = 0

        subprocess.run(f"mkdir {self.dir}/Packmol", shell = True)


        with open(f'{self.dir}/Packmol/mixture.inp', 'a') as m:
            info_all = ["#", f"# A mixture of {solvent},{solvent2} and solutes", "#", "","tolerance 2.0", "filetype pdb", f"output Packmol/Mixture.pdb",
                    "", f"structure {self.solvent}_Solvent/{self.solvent}_Solvent.pdb", f"  number {self.numberSolvent}", f"  inside box 0. 0. 0. {self.x} {self.y} {self.z}", "end structure","",
                    f"structure {self.solvent2}_Solvent2/{self.solvent2}_Solvent2.pdb", f"  number {self.numberSolvent2}",
                    f"  inside box 0. 0. 0. {self.x} {self.y} {self.z}", "end structure",
                  ]
            for i in range( len(con)):
                self.mol = int(
                    float(con[i].strip()) * (6.4e-20)* 6.02214e23*(((self.x/10) * (self.y/10) * (self.z/10))/(40*40*40)))
                info_all.append(" ")
                info_all.append(f"structure {solute[i].strip()[:3]}_Solute{i+1}/{solute[i].strip()[:3]}_Solute{i+1}.pdb")
                info_all.append( f"  number {self.mol}")
                info_all.append(f"  inside box 0. 0. 0. {self.x} {self.y} {self.z}")
                info_all.append("end structure")



            info_none=["#", f"# A mixture of {solvent},and solutes", "#", "","tolerance 2.0", "filetype pdb", f"output Packmol/Mixture.pdb",
                    "", f"structure {self.solvent}_Solvent/{self.solvent}_Solvent.pdb", f"  number {self.numberSolvent}", f"  inside box 0. 0. 0. {self.x} {self.y} {self.z}", "end structure"]

            for i in range( len(con)):
                self.molnum = int(
                    float(con[i].strip()) * (6.4e-20)* 6.02214e23*(((self.x/10) * (self.y/10) * (self.z/10))/(40*40*40)))
                info_none.append(" ")
                info_none.append(f"structure {solute[i].strip()[:3]}_Solute{i+1}/{solute[i].strip()[:3]}_Solute{i+1}.pdb")
                info_none.append( f"  number {self.molnum}")
                info_none.append(f"  inside box 0. 0. 0. {self.x} {self.y} {self.z}")
                info_none.append("end structure")


            if  len(self.solvent2)!=0:
                for lines in info_all:
                    m.writelines(lines +"\n")
            if  len(self.solvent2) == 0:
                for lines in info_none:
                    m.writelines(lines + "\n")


        while not os.path.isfile(f"{self.dir}/Packmol/mixture.inp"):
            time.sleep(1)
        conda_activate = f"source {self.dir}/miniconda3/bin/activate"
        packmol_cmd =f"packmol < {self.dir}/Packmol/mixture.inp"

        cmd = ["bash", "-c",
               f'{conda_activate} && {packmol_cmd}']
        subprocess.Popen(cmd).wait()
        self.to()
    def to(self,):
        top.toopol(self.solvent, self.numberSolvent, self.solvent2, self.numberSolvent2, self.solutes, self.con, self.dir, self.x/10, self.y/10, self.z/10)









