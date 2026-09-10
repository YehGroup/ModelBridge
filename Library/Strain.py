import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from scipy.interpolate import griddata
from pathlib import Path
from .Neighbor import read_lammps_steps

def compute_strain_tensor_from_frames(ref_df, def_df, atom_types, cutoff_radius=8.0):
    """
    Compute local 2D strain tensor using the same idea as the attached code.

    For each atom i:
        1. Find neighbors around i in the reference configuration.
        2. Compute relative neighbor vectors before and after deformation.
        3. Compute relative displacement differences.
        4. Fit local displacement gradient by least squares.
        5. Extract exx, eyy, exy with out-of-plane correction.
    """

    ref_layer = ref_df[ref_df["type"].isin(atom_types)].copy()
    def_layer = def_df[def_df["type"].isin(atom_types)].copy()

    # Match atoms by id
    merged = ref_layer.merge(
        def_layer,
        on="id",
        suffixes=("_ref", "_def")
    ).sort_values("id").reset_index(drop=True)

    # Reference and deformed positions
    R0 = merged[["x_ref", "y_ref", "z_ref"]].to_numpy()
    R1 = merged[["x_def", "y_def", "z_def"]].to_numpy()

    # Remove rigid center-of-mass translation of this layer
    R1 = R1 - (R1.mean(axis=0) - R0.mean(axis=0))

    tree = cKDTree(R0)

    strain_data = []

    for i in range(len(merged)):
        atom_id = merged.loc[i, "id"]
        atom_type = merged.loc[i, "type_ref"]

        # neighbors in reference configuration
        neighbors = tree.query_ball_point(R0[i], cutoff_radius) #define neighbors based on a cut off
        neighbors = [j for j in neighbors if j != i]

        if len(neighbors) < 3:
            strain_data.append([atom_id, atom_type, R0[i,0], R0[i,1], R0[i,2],
                                np.nan, np.nan, np.nan, np.nan, np.nan])
            continue

        # Relative neighbor vectors before deformation
        dR0 = R0[neighbors] - R0[i]

        # Relative neighbor vectors after deformation
        dR1 = R1[neighbors] - R1[i]

        # Relative displacement changes
        dU = dR1 - dR0

        # Same structure as attached code:
        # A = in-plane reference neighbor vectors, shape (N, 2)
        # B = relative displacement vectors, including z, shape (N, 3)
        A = dR0[:, 0:2]
        B = dU[:, 0:3]

        # Solve A @ G = B
        # G[0,0] = du_x/dx
        # G[1,1] = du_y/dy
        # G[0,1] = du_y/dx
        # G[1,0] = du_x/dy
        # G[0,2] = du_z/dx
        # G[1,2] = du_z/dy
        G, _, _, _ = np.linalg.lstsq(A, B, rcond=None)

        dux_dx = G[0, 0]
        duy_dy = G[1, 1]
        duy_dx = G[0, 1]
        dux_dy = G[1, 0]
        duz_dx = G[0, 2]
        duz_dy = G[1, 2]

        # Strain components, following the attached code
        exx = dux_dx + 0.5 * duz_dx**2
        eyy = duy_dy + 0.5 * duz_dy**2
        exy = 0.5 * (duy_dx + dux_dy) + 0.5 * duz_dx * duz_dy

        dilation = exx + eyy
        vonmises = np.sqrt(exx**2 - exx*eyy + eyy**2 + 3.0*exy**2)

        strain_data.append([
            atom_id, atom_type, R0[i,0], R0[i,1], R0[i,2],
            exx, eyy, exy, dilation, vonmises
        ])

    strain_df = pd.DataFrame(
        strain_data,
        columns=[
            "id", "type", "x_ref", "y_ref", "z_ref",
            "exx", "eyy", "exy", "dilation", "vonmises"
        ]
    )

    return strain_df


def save_strain_scatter(strain_df, component, output_file):
    plt.figure(figsize=(7, 6))

    sc = plt.scatter(
        strain_df["x_ref"],
        strain_df["y_ref"],
        c=strain_df[component],
        s=MARKSIZE,              
        marker=".",
        cmap="bwr",
        vmin=-vlim,
        vmax=vlim,
        linewidths=0,
        edgecolors="none",
        rasterized=True
    )

    plt.colorbar(sc, label=component)
    plt.xlabel("x reference position (Å)")
    plt.ylabel("y reference position (Å)")
    plt.axis("equal")
    plt.tight_layout()

    plt.savefig(output_file, dpi=800, bbox_inches="tight")  # higher resolution; was 300
    plt.close()


def save_strain_interpolated(strain_df, component, output_file):
    coords = strain_df[["x_ref", "y_ref"]].to_numpy()
    values = strain_df[component].to_numpy()

    mask = np.isfinite(values)
    coords = coords[mask]
    values = values[mask]

    x_min, x_max = coords[:, 0].min(), coords[:, 0].max()
    y_min, y_max = coords[:, 1].min(), coords[:, 1].max()

    grid_x, grid_y = np.mgrid[
        x_min:x_max:grid_size*1j,
        y_min:y_max:grid_size*1j
    ]

    grid_z = griddata(coords, values, (grid_x, grid_y), method="linear")

    plt.figure(figsize=(7, 6))

    im = plt.imshow(
        grid_z.T,
        extent=(x_min, x_max, y_min, y_max),
        origin="lower",
        cmap="bwr",
        interpolation="bilinear",
        vmin=-vlim,
        vmax=vlim
    )

    plt.colorbar(im, label=component)
    plt.xlabel("x reference position (Å)")
    plt.ylabel("y reference position (Å)")
    plt.axis("equal")
    plt.tight_layout()

    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()


def print_plotted_data_range(strain_df, component):
    values = strain_df[component].to_numpy()
    values = values[np.isfinite(values)]

    if len(values) == 0:
        print(f"No finite values found for {component}.")
        return

    print(f"{component} data range:")
    print(f"  min = {values.min():.8g}")
    print(f"  max = {values.max():.8g}")





if __name__ == "__main__":

    ref_step = 12712      # no Au-MoS2 interaction
    def_step = 18300      # with Au-MoS2 interaction


    filename = '../../../Adjust15_nxn_Hamiltonian/2layer_55x55/positions.dat'

    # Choose strain component to plot:
    # options: "exx", "eyy", "exy", "dilation", "vonmises"
    component_to_plot = "dilation"

    # Choose which atoms define the strain field.
    # For MoS2, I recommend Mo atoms only for a clean triangular lattice.
    layer_types = [2, 5, 8, 11]      # Mo atoms
    # layer_types = [1, 4, 7, 10]    # bottom S
    # layer_types = [3, 6, 9, 12]    # top S
    #layer_types = list(range(1,13)) # all MoS2 atoms, less clean

    cutoff_radius = 4.0   # Å; attached code used 8 for strain field
    grid_size = 256
    vlim = 0.01           # color scale limit for strain plots
    MARKSIZE = 60 #size of the marker in scatter plot

    strain_csv = f"strain_ref{ref_step}_def{def_step}_data.csv"

    if Path(strain_csv).exists():
        print(f"Reading existing strain data: {strain_csv}")
        strain_df = pd.read_csv(strain_csv)

    else:
        ref, deformed = read_lammps_steps(filename, [ref_step, def_step])

        strain_df = compute_strain_tensor_from_frames(
            ref,
            deformed,
            atom_types=layer_types,
            cutoff_radius=cutoff_radius
        )

        strain_df.to_csv(strain_csv, index=False)
        print(f"Saved strain data: {strain_csv}")

    # Print min/max of the data being plotted
    print_plotted_data_range(strain_df, component_to_plot)

    # Save atom-by-atom scatter plot
    save_strain_scatter(
        strain_df,
        component_to_plot,
        f"strain_{component_to_plot}_scatter.png"
    )

    # Save interpolated heatmap
    save_strain_interpolated(
        strain_df,
        component_to_plot,
        f"strain_{component_to_plot}_map.png"
    )

    print(f"Saved strain_{component_to_plot}_scatter.png")
    print(f"Saved strain_{component_to_plot}_map.png")