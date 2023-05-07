import os
import subprocess
import time
from rdkit import Chem
from rdkit.Chem import AllChem
class lig:
    def __init__(self, sm, m):
        self.smiles = sm
        self.mol = m
        subprocess.run([f'mkdir /project/cmri235_uksr/shasanka_conda_boss/sla296/singularity/{self.mol}script'], shell=True)
        conda_activate = "source /project/cmri235_uksr/shasanka_conda_boss/sla296/singularity/miniconda3/bin/activate && conda activate ligpg"
        export_bossdir = "export BOSSdir=/project/cmri235_uksr/shasanka_conda_boss/sla296/singularity/boss"
        ligpargen_cmd = f"ligpargen -s '{self.smiles}' -n {self.mol} -p {self.mol} -r {self.mol} -c 0 -o 0 -cgen CM1A"
        singularity_container = "/project/cmri235_uksr/shasanka_conda_boss/sla296/singularity/Fast/f.sif"

        cmd = ["singularity", "exec", singularity_container, "bash", "-c",
               f'{conda_activate} && {export_bossdir} && {ligpargen_cmd}']
        subprocess.Popen(cmd).wait()

        while os.path.isfile(f'/project/cmri235_uksr/shasanka_conda_boss/sla296/singularity/{self.mol}/{self.mol}-debug.pdb') == False:
            print("still making pdb")
            time.sleep(1)
        pdb_location = Chem.MolFromPDBFile(f'/project/cmri235_uksr/shasanka_conda_boss/sla296/singularity/{self.mol}/{self.mol}-debug.pdb')
        pdb_location = Chem.AddHs(pdb_location)
        AllChem.EmbedMolecule(pdb_location)
        Chem.MolToMolFile(pdb_location, f'{self.mol}/{self.mol}.mol')
        comand2 = f'obabel -imol {self.mol}/{self.mol}.mol -ogjf -O {self.mol}script/{self.mol}.gjf --gen3D'
        subprocess.run([comand2], shell=True)

