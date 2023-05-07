import subprocess
class FIdel:
    def __init__(self, name):
        self.name = name
        sumbit_name = self.name + 'Sumbit.sh'
        self.idel = subprocess.run(['sinfo' ], shell=True, capture_output=True)
        self.nodes = self.idel.stdout.decode().splitlines()
        self.cacL_nodes = []                        #runs the sifo coamdn
        file = [
            "#!/bin/bash",
            "",
            "",
            "",
            "#SBATCH -t 5-00:00:00                                   #Time for the job to run",
            "#SBATCH --job-name=EPT_P1_s          #Name of the job",
            "",
            "#SBATCH -N 1                                    #Number of nodes required",
            "#SBATCH -n 40                           #Number of cores needed for the job",
            "#SBATCH --partition=CAC48M192_L         #Name of the queue",
            "",
            "#SBATCH --mail-type ALL                         #Send email on start/end",
            "#SBATCH --mail-user sla296@uky.edu              #Where to send email",
            "",
            "#SBATCH --account=col_cmri235_uksr              #Name of account to run under",
            "",
            "#SBATCH --error=SLURM_JOB_%j.err                #Name of error file",
            "#SBATCH --output=SLURM_JOB_%j.out               #Name of output file",
            "",
            "#Module needed for this Gaussian job",
            f"#SBATCH --chdir=/project/cmri235_uksr/shasanka_conda_boss/sla296/singularity/{self.name}script",
            "module load ccs/gaussian/g16-A.03/g16-haswell",
            "",
            "echo \"Job $SLURM_JOB_ID running on SLURM NODELIST: $SLURM_NODELIST\"",
            "",
            "#Gaussian Program execution command",
            "sleep 5",
            "g16 ept_p1_lpg.gjf > ept_p1_lpg.log"
        ]

        for lines in self.nodes:
            if 'CAC48M192_L' in lines or 'CAL48M192_L' in lines:
                word= lines.split()
                if 'idel' in word:                  
                    self.cacL_nodes.append(lines)
        try:
            self.idel_node= self.cacL_nodes[0][0]
        except:
            print("No idel node, making sumbit file using CAC48M192_L")
            self.idel_node= "CAC48M192_L"
            with open(f'{self.name}script/{sumbit_name}', 'a') as a:
                file[9] = '#SBATCH --partition=' + self.idel_node + '			#Name of the queue'
                file[27] = f'g16 /project/cmri235_uksr/shasanka_conda_boss/sla296/singularity/{self.name}script/{self.name}-final.gjf > /project/cmri235_uksr/shasanka_conda_boss/sla296/singularity/{self.name}script/{self.name}-final.log'
                for iteams in file:
                    a.write(iteams + '\n')

            print("Submit file is made, now submititng")
        else:
            self.idel_node= self.cacL_nodes[0][0]
            with open (f'{self.name}script/{sumbit_name}', 'a') as a:
                file[9] = '#SBATCH --partition=' + self.idel_node + '			#Name of the queue'
                file[26] = f'g16 {self.name}.gjf > {self.name}.log'
                for iteams in file:
                    a.write(iteams + '\n')

            print("Submit file made, now submititng")

