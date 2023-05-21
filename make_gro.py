import subprocess

class gro:
    def __init__(self,solvent, solute,di,x,y,z):
        self.dir = di
        self.x = x
        self.y = y
        self.z = z
        self.solvent = solvent
        self.solute = solute
        command= f'source {self.dir}/Fast/gromacs_load.sh && gmx_mpi editconf -f {self.dir}/{solvent}_{solute}Packmol/{self.solvent}_and_{self.solute}Mixture.pdb -box {self.x} {self.y} {self.z} -o {solvent}_{solute}Packmol/solvated.gro'
        subprocess.run(command, shell = True, check = True)
        print("gro file made")
        command2= f'mkdir {self.dir}/{solvent}_{solute}Grofiles'

        command3 =f'mv {self.dir}/{solute}_Solute/{solute}_Solute.pdb {self.dir}/{solvent}_{solute}Grofiles && mv {self.dir}/{solute}_Solute/{solute}_Solute.gmx.itp {self.dir}/{solvent}_{solute}Grofiles && mv {self.dir}/{solute}_Solutescript {self.dir}/{solvent}_{solute}Grofiles'
        command4 = f'mv {self.dir}/{solvent}_Solvent/{solvent}_Solvent.pdb {self.dir}/{solvent}_{solute}Grofiles && mv {self.dir}/{solvent}_Solvent/{solvent}_Solvent.gmx.itp {self.dir}/{solvent}_{solute}Grofiles && mv {self.dir}/{solvent}_Solventscript {self.dir}/{solvent}_{solute}Grofiles'
        command5= f'mv {self.dir}/{solvent}_{solute}Packmol/solvated.gro {self.dir}/{solvent}_{solute}Grofiles'
        command6= f'rm -r {self.dir}/{solute}_Solute && rm -r {self.dir}/{solvent}_Solvent && rm -r {self.dir}/{solvent}_{solute}Packmol'
        print("cleaning up")
        subprocess.run(command2, shell=True, check=True)
        subprocess.run(command3, shell =True, check = True)
        subprocess.run(command4, shell=True, check=True)
        subprocess.run(command5, shell=True, check=True)
        subprocess.run(command6, shell=True, check=True)
        print("Starting the simulation")
