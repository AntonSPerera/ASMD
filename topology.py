import subprocess
class toopol:
    def __init__(self,solvent1,solvent1N, solvent2,solvent2N, solute1,solute1N, solute2,solute2N, currentdir,):
        self.solvent= solvent1
        self.solvent2= solvent2
        self.solute1 = solute1
        self.solute2= solute2
        self.dir= currentdir
        command2= f'mkdir {self.dir}/{solvent1}_{solute1}_{solute2}_{solvent2}Grofiles'
        subprocess.run(command2, shell=True, check=True)
        cmd= f"touch {self.dir}/{solvent1}_{solute1}_{solute2}_{solvent2}Grofiles/topology.top && touch {self.dir}/{solvent1}_{solute1}_{solute2}_{solvent2}Grofiles/nmol.itp"
        subprocess.run(cmd, shell=True, check=True)
        with open (f"{self.dir}/{solvent1}_{solute1}_{solute2}_{solvent2}Grofiles/topology.top", 'a') as top, open(f"{self.dir}/{solvent1}_{solute1}_{solute2}_{solvent2}Grofiles/nmol.itp", 'a') as nmol:
            lines=['#include "oplsaa.ff/forcefield.itp"', f'#include "{self.solute1}_Solute1.gmx.itp"', f'#include "{self.solute2}_Solute2.gmx.itp"',f'#include "{self.solute1}_Solute.gmx.itp"', f'#include "{self.solvent}_Solvent1.gmx.itp"', f'#include "{self.solvent2}_Solvent2.gmx.itp"',"", '[system]', f'{solvent1}_{solvent2}_{solute1}_{solute1}',"",'#include "nmol.itp"' ]
            for l in lines:
                top.write(l +"\n")
            linesNmol=['[ molecules ]', ';molecules #molecules',"", f'{self.solvent}   {solvent1N}',f'{self.solvent2}   {solvent2N}', f'{self.solute1}   {solute1N}', f'{self.solute2}   {solute2N}']
            for li in linesNmol:
                nmol.write(li +"\n")


