import subprocess
import reorg as g


class gro:
    def __init__(self, solvent, solute, solvent2, di, x, y, z):
        self.dir = di
        self.x = x
        self.y = y
        self.z = z
        self.solvent = solvent
        self.solute = solute
        self.solvent2 = solvent2
        command = f'gmx_mpi editconf -f {self.dir}/Packmol/Mixture.pdb -box {self.x} {self.y} {self.z} -o Packmol/solvated.gro'
        subprocess.run(command, shell=True, check=True)
        print("gro file made")

        
        command4 = f'mv {self.dir}/{solvent}_Solvent/{solvent}_Solvent.pdb {self.dir}/InputGrofiles && mv {self.dir}/{solvent}_Solvent/{solvent}_Solvent.gmx.itp {self.dir}/InputGrofiles && mv {self.dir}/{solvent}_Solventscript {self.dir}/InputGrofiles'

        command5 = f'mv {self.dir}/Packmol/solvated.gro {self.dir}/InputGrofiles'
        command6 = f'rm -r {self.dir}/{solvent}_Solvent && rm -r {self.dir}/Packmol'

        command8 = f'mv {self.dir}/{solvent2}_Solvent2/{solvent2}_Solvent2.pdb {self.dir}/InputGrofiles && mv {self.dir}/{solvent2}_Solvent2/{solvent2}_Solvent2.gmx.itp {self.dir}/InputGrofiles && mv {self.dir}/{solvent2}_Solvent2script {self.dir}/InputGrofiles'
        command10 = f'rm -r {self.dir}/{solvent2}_Solvent2'
        command12 = f'cp -r {self.dir}/Fast/MDP {self.dir}/InputGrofiles'
        print("cleaning up")

        

        subprocess.run(command4, shell=True, check=True)
        subprocess.run(command5, shell=True, check=True)
        subprocess.run(command6, shell=True, check=True)
        if  len(self.solvent2) != 0:
            subprocess.run(command8, shell=True, check=True)
            subprocess.run(command10, shell=True, check=True)



        for i in range(len(self.solute)):
            com1 = f'mv {self.dir}/{self.solute[i].strip()[:3]}_Solute{i+1}/{self.solute[i].strip()[:3]}_Solute{i+1}.pdb {self.dir}/InputGrofiles && mv {self.dir}/{self.solute[i].strip()[:3]}_Solute{i+1}/{self.solute[i].strip()[:3]}_Solute{i+1}.gmx.itp {self.dir}/InputGrofiles && mv {self.dir}/{self.solute[i].strip()[:3]}_Solute{i+1}script {self.dir}/InputGrofiles'
            com2 = f'rm -r {self.dir}/{self.solute[i].strip()[:3]}_Solute{i+1}'
            subprocess.run(com1, shell=True, check=True)
            subprocess.run(com2, shell=True, check=True)


        g.reorg(self.solvent + "_Solvent", self.dir + "/InputGrofiles")


        if len(self.solvent2) != 0:
            g.reorg(self.solvent2 + "_Solvent2", self.dir + "/InputGrofiles")

        for j in range(len(self.solute)):
            g.reorg(self.solute[j].strip()[:3] + f"_Solute{j+1}", self.dir + "/InputGrofiles")

        subprocess.run(command12, shell=True, check=True)


        print("Starting the simulation")
