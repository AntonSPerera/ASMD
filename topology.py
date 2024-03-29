import subprocess
import os


class toopol:
    def __init__(self, solvent1, solvent1N, solvent2, solvent2N, solute, con, currentdir, x,y,z):
        self.solvent = solvent1
        self.solvent2 = solvent2
        self.solute1 = solute
        self.con = con
        self.dir = currentdir
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        command2 = f'mkdir {self.dir}/InputGrofiles'
        if os.path.isdir(f'{self.dir}/InputGrofiles') == True:
            folder_number=0
            if os.path.isdir(f'{self.dir}/Old_InputGrofiles_Output')==False:
                make_old= f'mkdir {self.dir}/Old_InputGrofiles_Output'
                subprocess.run(make_old, shell=True, check=True)
            while True:
                if os.path.isdir(f'{self.dir}/Old_InputGrofiles_Output/InputGrofiles{folder_number+1}'):
                    folder_number +=1
                else:
                    move = f'mv {self.dir}/InputGrofiles {self.dir}/Old_InputGrofiles_Output/InputGrofiles{folder_number+1}'
                    subprocess.run(move, shell=True, check=True)
                    break
        if os.path.isdir(f'{self.dir}/Output') == True:
            folder_number = 0
            while True:
                if os.path.isdir(f'{self.dir}/Old_InputGrofiles_Output/Output{folder_number + 1}'):
                    folder_number += 1
                else:
                    move = f'mv {self.dir}/Output {self.dir}/Old_InputGrofiles_Output/Output{folder_number + 1}'
                    subprocess.run(move, shell=True, check=True)
                    break
        subprocess.run(command2, shell=True, check=True)
        cmd = f"touch {self.dir}/InputGrofiles/topol.top && touch InputGrofiles/nmol.itp"
        subprocess.run(cmd, shell=True, check=True)
        with open(f"{self.dir}/InputGrofiles/topol.top", 'a') as top, open(
                f"{self.dir}/InputGrofiles/nmol.itp", 'a') as nmol:

            lines_atomtypes = ['#include "oplsaa.ff/forcefield.itp"', f'#include "{self.solvent}_Solvent_atomtype.itp"'
                          ]
            lines_itp=[f'#include "{self.solvent}_Solvent.itp"']

            last_lines=["", '[system]',
                          f'{solvent1}', "", '#include "nmol.itp"']

            if len(self.solvent2) !=0:
                lines_atomtypes.append(f'#include "{self.solvent2}_Solvent2_atomtype.itp"')
                lines_itp.append(f'#include "{self.solvent2}_Solvent2.itp"')
            for i in range(len(self.solute1)):
                lines_atomtypes.append(f'#include "{self.solute1[i].strip()[:3]}_Solute{i+1}_atomtype.itp"')
                lines_itp.append(f'#include "{self.solute1[i].strip()[:3]}_Solute{i+1}.itp"')




            for l in lines_atomtypes:
                top.write(l + "\n")
            for sha in lines_itp:
                top.write(sha + "\n")
            for lami in last_lines:
                top.write(lami + "\n")


            linesNmol = ['[ molecules ]', ';molecules #molecules', "", f'{self.solvent}   {solvent1N}'
                            ]
            if len(self.solvent2) != 0:
                linesNmol.append(f'{self.solvent2}   {solvent2N}')

            for i in range(len(self.solute1)):
                self.mol = int(
                    float(self.con[i].strip()) * (6.4e-20) * 6.02214e23 * ((self.x * self.y * self.z) / (40 * 40 * 40)))
                linesNmol.append(f'{self.solute1[i].strip()[:3]}   {self.mol}')


            for li in linesNmol:
                nmol.write(li + "\n")




