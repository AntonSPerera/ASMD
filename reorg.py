import subprocess
class reorg:
    def __init__(self, molecule, dir):
        self.moleclue=molecule
        self.dir = dir
        subprocess.run(f"touch {self.dir}/{self.moleclue}.itp", shell=True)
        subprocess.run(f'touch {self.dir}/{self.moleclue}_atomtype.itp', shell=True)
        with open (f"{self.dir}/{self.moleclue}.gmx.itp", 'r') as org, open(f"{self.dir}/{self.moleclue}.itp", 'a') as itp, open(f'{self.dir}/{self.moleclue}_atomtype.itp', 'a') as type:
            lines=org.readlines()
            atomtype=10
            atomtype_lastline=0
            orginal=[]
            for iteams in lines:
                orginal.append(iteams)
            orginal[6]=";[ defaults ]"+ "\n"
            orginal[7]="; nbfunc        comb-rule       gen-pairs       fudgeLJ fudgeQQ" + "\n"
            orginal[8]=";    1               3              yes            0.5     0.5" +"\n"
            for iteams in orginal:
                if iteams.strip()=="[ moleculetype ]":
                    atomtype_lastline =orginal.index(iteams) - 2
            for i in range(atomtype):
                itp.writelines(orginal[i])
            for j in range(atomtype_lastline +2, len(orginal)):
                itp.writelines(orginal[j])
            type.writelines('\n')
            for k in range(atomtype_lastline-atomtype+1):
                type.writelines(orginal[atomtype+k])

       
       

