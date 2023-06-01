import os
import subprocess
import tempfile
#from pmda.rdf import InterRDF




# Directories and files
current_dir = os.getcwd()
input_dir = os.path.join(current_dir, 'InputGrofiles')
output_dir = os.path.join(current_dir, 'Output')
mdp_dir = os.path.join(current_dir, 'Fast/MDP')
topology_file = os.path.join(input_dir, "topol.top")
initial_coordinates = os.path.join(input_dir, "solvated.gro")
xtc_file = os.path.join(output_dir, "production.xtc")
tpr_file = os.path.join(output_dir, "production.tpr")
eqtpr_file= os.path.join(output_dir,"equilibration.tpr")
trr_file = os.path.join(output_dir, "production.trr")
nmol_itp = os.path.join(input_dir, "nmol.itp")
gro_file = os.path.join(output_dir, "production.gro")
edr_file = os.path.join(output_dir, "equilibration.edr")

# Copy MDP files to output directory
subprocess.run(["cp", "-r", f"{mdp_dir}/.", output_dir])
# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Run simulations
import subprocess
import re
import os


def count_warnings(filename):
    # Read the simulation output log file and count the number of warnings
    if os.path.isfile(output_dir +"/em.log")==True:
        with open(filename, 'r') as file:
            log_data = file.read()

        warning_pattern = r'WARNING'
        warning_count = len(re.findall(warning_pattern, log_data))
    else:
        warning_count =100

    return warning_count


def update_maxwarn(max_warn, threshold):
    # Check the warning count and update the max_warn value if needed
    warning_count = count_warnings(os.path.join(output_dir, "em.log"))
    if warning_count > threshold:
        max_warn *= 2  # Double the max_warn value
        print(f"Warning count ({warning_count}) exceeded threshold. Updating max_warn to: {max_warn}")
    else:
        print(f"Simulation completed successfully with {warning_count} warnings.")

    return max_warn


def get_available_cpu_threads():
    # Get the number of available CPU threads
    cpu_info = os.popen('lscpu').read()
    threads_pattern = r'Thread\(s\) per core:\s+(\d+)'
    result = re.search(threads_pattern, cpu_info)
    if result:
        threads_per_core = int(result.group(1))
        available_threads = os.cpu_count() * threads_per_core
        return available_threads
    else:
        return None


def get_available_gpus():
    # Get the number of available GPUs
    gpu_info = os.popen('nvidia-smi --list-gpus').read()
    gpu_count = len(re.findall(r'GPU\s\d:', gpu_info))
    return gpu_count


def run_gromacs_simulation(command, max_warn, threshold):
    # Execute the GROMACS simulation command
    subprocess.run(command + ["-maxwarn", str(max_warn)])

    # Check the warning count and update max_warn if needed
    while True:
        max_warn = update_maxwarn(max_warn, threshold)
        if count_warnings(os.path.join(output_dir, "em.log")) <= threshold:
            break

    return max_warn


# Set initial values
max_warn = 10
threshold = 100

# Energy minimization
command = ["gmx_mpi", "grompp", "-f", os.path.join(mdp_dir, "em.mdp"), "-c", initial_coordinates, "-p", topology_file,
           "-o", os.path.join(output_dir, "em.tpr")]
max_warn = run_gromacs_simulation(command, max_warn, threshold)

available_threads = get_available_cpu_threads()
available_gpus = get_available_gpus()

command = ["gmx_mpi", "mdrun", "-deffnm", "em", "-v"]
if available_threads is not None:
    command += ["-ntomp", str(available_threads)]
subprocess.run(command, cwd=output_dir)

# NVT equilibration
command = ["gmx_mpi", "grompp", "-f", os.path.join(mdp_dir, "nvt.mdp"), "-c", os.path.join(output_dir, "em.gro"), "-p",
           topology_file, "-o", os.path.join(output_dir, "nvt.tpr")]
max_warn = run_gromacs_simulation(command, max_warn, threshold)

command = ["gmx_mpi", "mdrun", "-deffnm", "nvt", "-v"]
if available_threads is not None:
    command += ["-ntomp", str(available_threads)]
subprocess.run(command, cwd=output_dir)

# NPT equilibration
command = ["gmx_mpi", "grompp", "-f", os.path.join(mdp_dir, "equilibration.mdp"), "-c",
           os.path.join(output_dir, "nvt.gro"), "-t", os.path.join(output_dir, "nvt.cpt"), "-p", topology_file, "-o",
           os.path.join(output_dir, "equilibration.tpr")]
max_warn = run_gromacs_simulation(command, max_warn, threshold)
command = [ "gmx_mpi", "mdrun", "-deffnm", "equilibration", "-v"]
#if available_gpus > 0:
    #command = ["mpirun", "-np", str(available_gpus), "gmx_mpi", "mdrun", "-deffnm", "equilibration", "-v", "-nb", "gpu"]
if available_threads is not None:
    command += ["-ntomp", str(available_threads)]
subprocess.run(command, cwd=output_dir)

# Calculate density for validation
import gromacs



def calculate_density(tpr_file, edr_file):
    
    # Ensure GROMACS commands are available.
    gromacs.config.setup()

    # Run gmx_mpi energy to extract density.
    density_xvg_file = f"{output_dir}/density.xvg"
    #command = f'gmx_mpi energy -s {os.path.abspath(eqtpr_file)} -f {os.path.abspath(edr_file)} -o {output_dir}/{density_xvg_file}'
    energy_mpi = gromacs.tools.Energy_mpi(s=os.path.abspath(eqtpr_file),
                                          f=os.path.abspath(edr_file),
                                          o=f'{density_xvg_file}')

    energy_mpi.run(input="Density")
    #subprocess.run(command)
    return density_xvg_file


def extract_density(density_xvg_file):
    # Read density values from the xvg file.
    densities = []
    with open(density_xvg_file, "r") as f:
        for line in f.readlines():
            if line.startswith("#") or line.startswith("@"):
                continue
            densities.append(float(line.split()[1]))

    return densities


density_xvg_file = calculate_density(tpr_file, edr_file)
densities = extract_density(density_xvg_file)

print("Density values:", densities)


# Run production if density is within accuracy
def production_run(topology_file, output_dir):
    max_warn = 10
    threshold = 100
    command = ["gmx_mpi", "grompp", "-f", os.path.join(mdp_dir, "production.mdp"), "-c",
               os.path.join(output_dir, "equilibration.gro"), "-t", os.path.join(output_dir, "equilibration.cpt"), "-p", topology_file, "-o",
               os.path.join(output_dir, "production.tpr")]
    max_warn = run_gromacs_simulation(command, max_warn, threshold)
    command = [ "gmx_mpi", "mdrun", "-deffnm", "production", "-v"]
    #if available_gpus > 0:
        #command = ["mpirun", "-np", str(available_gpus), "gmx_mpi", "mdrun", "-deffnm", "production", "-v", "-nb", "gpu"]
    if available_threads is not None:
        command += ["-ntomp", str(available_threads)]
    subprocess.run(command, cwd=output_dir)
    print("Simulation completed.")

def check_density_accuracy(x, densities):
    mean_density = sum(densities) / len(densities)
    lower_limit = 0.9 * mean_density
    upper_limit = 1.1 * mean_density

    if lower_limit <= x <= upper_limit:
        print(f"The given value x = {x} is within 10% accuracy of the mean density y = {mean_density:.2f}.")
        return True
    else:
        print(f"The given value x = {x} is not within 10% accuracy of the mean density y = {mean_density:.2f}.")
        return False


x = 0.34  # Replace with your given density value
is_within_accuracy = check_density_accuracy(x, densities)

if is_within_accuracy:
    production_run(topology_file, output_dir)
else:
    print("The density does not satisfy the 10% accuracy condition. The production run will not continue.")

# Perform PBC correction
trjconv = gromacs.tools.Trjconv(s=tpr_file, f=trr_file, o=xtc_file, pbc="mol", ur="compact")
trjconv.run(input="System")

# Analysis

# MSD
import subprocess

# Create an index file for the ions
subprocess.run(["gmx_mpi", "make_ndx", "-f", gro_file, "-o", f"{output_dir}/index.ndx"], input=b"q\n")

# Calculate the MSD for the ions
subprocess.run(["gmx_mpi", "msd", "-f", xtc_file, "-s", tpr_file, "-n", "index.ndx", "-o", f"{output_dir}/msd.xvg"], input=b"0\n")

import os
import MDAnalysis as mda


def extract_residues_from_itp(itp_file):
    residues = []

    with open(itp_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith(";"):
                continue
            if line.strip() == "[ molecules ]":
                break

        for line in lines[lines.index("[ molecules ]\n") + 1:]:
            if line.strip() == "" or line.startswith(";"):
                continue
            residues.append(line.split()[0])

    return residues


residue_names = extract_residues_from_itp(nmol_itp)
print("Residue names:", residue_names)

universes = {}

for residue_name in residue_names:
    universe = mda.Universe(gro_file)
    residue_universe = universe.select_atoms(f"resname {residue_name}")
    universes[residue_name] = residue_universe

# Usage example:
#residue_name = "ACN"
#print(f"Number of '{residue_name}' atoms: {len(universes[residue_name].atoms)}")

import MDAnalysis as mda
import MDAnalysis.analysis.rdf as rdf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

universe = mda.Universe(gro_file, xtc_file)


# Function to count the number of atoms in a residue
def count_atoms_in_residue(universe, resname):
    residue = universe.select_atoms(f"resname {resname}")[0].residue
    return len(residue.atoms)


# Calculate the number of atoms in each residue type
atoms_in_residues = {resname: count_atoms_in_residue(universe, resname) for resname in residue_names}

# Set up PDF file to save plots
with PdfPages(f'{output_dir}/RDF_plots.pdf') as pdf:
    # Calculate RDF for each residue type as reference
    for reference_residue in residue_names:
        plt.figure(figsize=(8, 6))
        for target_residue in residue_names:
            reference_group = universe.select_atoms(f"resname {reference_residue}")
            target_group = universe.select_atoms(f"resname {target_residue}")

            # Use exclusion_block based on the number of atoms in the residues
            exclusion_block = (atoms_in_residues[reference_residue],
                               atoms_in_residues[target_residue]) if reference_residue == target_residue else None

            rdf_analysis = rdf.InterRDF(reference_group, target_group, nbins=75, range=(0.0, 15.0),
                                        exclusion_block=exclusion_block)
            rdf_analysis.run()

            # Plot RDF
            plt.plot(rdf_analysis.bins, rdf_analysis.rdf, label=f"{reference_residue}-{target_residue}")

        plt.xlabel("Distance (angstroms)")
        plt.ylabel("RDF")
        plt.title(f"RDF for reference residue: {reference_residue}")
        plt.legend()

        # Display the plot in the Jupyter notebook
        plt.show()

        # Save the plot to the PDF file
        pdf.savefig(plt.gcf())
        plt.close()

import numpy as np

# Function to calculate coordination number from RDF
def calculate_coordination_number(rdf_analysis, rcut):
    # Integrate the RDF up to the cutoff radius
    cn = np.trapz(rdf_analysis.rdf[rdf_analysis.bins <= rcut], x=rdf_analysis.bins[rdf_analysis.bins <= rcut])
    return cn

# Set up PDF file to save plots and a dictionary to store coordination numbers
with PdfPages(f'{output_dir}/RDF_plots.pdf') as pdf:
    coordination_numbers = {}
    # Calculate RDF for each residue type as reference
    for reference_residue in residue_names:
        plt.figure(figsize=(8, 6))
        coordination_numbers[reference_residue] = {}
        for target_residue in residue_names:
            reference_group = universe.select_atoms(f"resname {reference_residue}")
            target_group = universe.select_atoms(f"resname {target_residue}")

            # Use exclusion_block based on the number of atoms in the residues
            exclusion_block = (atoms_in_residues[reference_residue],
                               atoms_in_residues[target_residue]) if reference_residue == target_residue else None

            rdf_analysis = rdf.InterRDF(reference_group, target_group, nbins=75, range=(0.0, 15.0),
                                        exclusion_block=exclusion_block)
            rdf_analysis.run()

            # Calculate coordination number and store it
            cn = calculate_coordination_number(rdf_analysis, rcut=5)  # Adjust rcut value as needed
            coordination_numbers[reference_residue][target_residue] = cn

            # Plot RDF
            plt.plot(rdf_analysis.bins, rdf_analysis.rdf, label=f"{reference_residue}-{target_residue} (CN={cn:.2f})")

        plt.xlabel("Distance (angstroms)")
        plt.ylabel("RDF")
        plt.title(f"RDF for reference residue: {reference_residue}")
        plt.legend()

        # Display the plot in the Jupyter notebook
        plt.show()

        # Save the plot to the PDF file
        pdf.savefig(plt.gcf())
        plt.close()

# Print coordination numbers
for ref_residue, target_residues in coordination_numbers.items():
    for target_residue, cn in target_residues.items():
        print(f"Coordination number of {ref_residue} to {target_residue}: {cn:.2f}")

import pandas as pd

# Create an empty list to store the data
coordination_numbers_list = []

for ref_residue, target_residues in coordination_numbers.items():
    for target_residue, cn in target_residues.items():
        # Append the data to the list instead of printing
        coordination_numbers_list.append([ref_residue, target_residue, cn])

# Convert the list to a DataFrame
coordination_numbers_df = pd.DataFrame(coordination_numbers_list, columns=['Reference_Residue', 'Target_Residue', 'Coordination_Number'])

# Print the DataFrame
print(coordination_numbers_df)
