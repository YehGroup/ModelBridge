import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.linalg import eigvalsh

from Library.Neighbor import read_lammps_steps, extract_mo_cells, assign_cell_indices, select_matrix_cells
from Library.Hamiltonian import build_full_H, build_full_H_open
from Library.Strain import compute_strain_tensor_from_frames


'''
# Building strained Hamiltonian
'''
filename = "/media/yehlab/C/Xiang/Adjust15_nxn_Hamiltonian/0layer_55x55/positions.dat"
ref_step, def_step = 20454, 71167
Mo_types = [2, 5, 8, 11]
nei_radius = 8.0
a = 3.117

ref_df, def_df = read_lammps_steps(filename, [ref_step, def_step])
print(f"Reference and Deformed Frames loaded")
strain_df = compute_strain_tensor_from_frames(ref_df, def_df, atom_types=Mo_types, cutoff_radius=nei_radius)
print(f"Strain tensor constructed")

mo_df = extract_mo_cells(ref_df, mo_types=(2, 5, 8, 11))
cells = assign_cell_indices(mo_df, a=a, theta_deg=0, search_radius=1.5)
selected = select_matrix_cells(cells, chosen_cell_x=0, chosen_cell_y=0, supercell_side=9)
print(f"Cell constructed")

H = build_full_H(selected, strain_df)
#H = build_full_H_open(selected, strain_df)
print(f"H constructed")
print("H shape:", H.shape)
print("H dtype:", H.dtype)
print(f"H memory: {H.nbytes / 1024**3:.3f} GB")


'''
# Calculating Eigen Values
'''
evals = eigvalsh(H) #return evals in ascending order
print(f"Eigenvalue constructed")


'''
# Plot Histogram
'''
bin_width = 0.05   # eV; try 0.01, 0.02, 0.05, 0.10

E_min = np.floor(evals.min() / bin_width) * bin_width
E_max = np.ceil(evals.max() / bin_width) * bin_width

bins = np.arange(E_min, E_max + bin_width, bin_width)

counts, edges = np.histogram(evals, bins=bins)
centers = 0.5 * (edges[:-1] + edges[1:])

# Save histogram data
hist_df = pd.DataFrame({
    "E_left": edges[:-1],
    "E_right": edges[1:],
    "E_center": centers,
    "count": counts,
})

plt.figure(figsize=(10, 6))

plt.bar(
    centers,
    counts,
    width=bin_width,
    align="center",
    edgecolor="black",
    linewidth=0.5,
)

plt.xlabel("Energy (eV)")
plt.ylabel("Number of states")
plt.title("Eigenvalue Histogram")
plt.grid(True, linestyle="--", alpha=0.5)
plt.xticks(np.arange(-13,0,1))
plt.tight_layout()
plt.savefig("eigenvalue_histogram.png", dpi=300)
plt.close()
print(f"Histogram done")