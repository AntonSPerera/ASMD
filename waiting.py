import time
class waiting:
    def __init__(self, name):
        self.name=name
        made = False
        while made==False:
            with open (f'/project/cmri235_uksr/shasanka_conda_boss/sla296/singularity/{self.name}script/{self.name}-final.log','r') as outputF:
                a =outputF.readlines()
                if len(a)==0:
                    print("log file is courpted")
                line=a[-1].strip()
                if line[0:33]=="Normal termination of Gaussian 16":
                    made = True
                    print("Now trasfering charges")
                else:
                    print("DFT not done, wating for 10 sec befroe rechecking")
                    time.sleep(10)