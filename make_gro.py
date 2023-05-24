import subprocess

class gro:
    def __init__(self,solvent, solute,solvent2,solute2,di,x,y,z):
        self.dir = di
        self.x = x
        self.y = y
        self.z = z
        self.solvent = solvent
        self.solute = solute
        self.solvent2 = solvent2
        self.solute2 = solute2
        command= f'source {self.dir}/Fast/gromacs_load.sh && gmx_mpi editconf -f {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Packmol/{solvent}_{solute}_{solute2}_{solvent2}Mixture.pdb -box {self.x} {self.y} {self.z} -o {solvent}_{solute}_{solute2}_{solvent2}Packmol/solvated.gro'
        subprocess.run(command, shell = True, check = True)
        print("gro file made")


        command3 =f'mv {self.dir}/{solute}_Solute/{solute}_Solute.pdb {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Grofiles && mv {self.dir}/{solute}_Solute/{solute}_Solute.gmx.itp {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Grofiles && mv {self.dir}/{solute}_Solutescript {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Grofiles'
        command4 = f'mv {self.dir}/{solvent}_Solvent/{solvent}_Solvent.pdb {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Grofiles && mv {self.dir}/{solvent}_Solvent/{solvent}_Solvent.gmx.itp {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Grofiles && mv {self.dir}/{solvent}_Solventscript {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Grofiles'
        
        command5= f'mv {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Packmol/solvated.gro {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Grofiles'
        command6= f'rm -r {self.dir}/{solute}_Solute && rm -r {self.dir}/{solvent}_Solvent && rm -r {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Packmol'

        command7 = f'mv {self.dir}/{solute2}_Solute2/{solute2}_Solute2.pdb {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Grofiles && mv {self.dir}/{solute2}_Solute2/{solute2}_Solute2.gmx.itp {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Grofiles && mv {self.dir}/{solute2}_Solute2script {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Grofiles'
        command8 = f'mv {self.dir}/{solvent2}_Solvent2/{solvent2}_Solvent2.pdb {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Grofiles && mv {self.dir}/{solvent2}_Solvent2/{solvent2}_Solvent2.gmx.itp {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Grofiles && mv {self.dir}/{solvent2}_Solvent2script {self.dir}/{solvent}_{solute}_{solute2}_{solvent2}Grofiles'
        command9 = f'rm -r {self.dir}/{solute2}_Solute2 && rm -r {self.dir}/{solvent2}_Solvent2'

        print("cleaning up")
        
        subprocess.run(command3, shell =True, check = True)
        subprocess.run(command4, shell=True, check=True)
        subprocess.run(command5, shell=True, check=True)
        subprocess.run(command6, shell=True, check=True)
        subprocess.run(command7, shell=True, check=True)
        subprocess.run(command8, shell=True, check=True)
        subprocess.run(command9, shell=True, check=True)
        print("Starting the simulation")
