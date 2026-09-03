import numpy as np
import pandas as pd
from .Param import GROUP_SIZE

# --8<-- [start:read-lammps]
def read_lammps_steps(filename, req_steps):
    req_steps = list(req_steps)
    req_set = set(req_steps)
    frames = {}

    with open(filename) as f:
        while True:
            line = f.readline()

            if not line:
                break

            if not line.startswith("ITEM: TIMESTEP"):
                continue

            step = int(f.readline())

            f.readline()                  # ITEM: NUMBER OF ATOMS
            n_atoms = int(f.readline())

            for _ in range(4):
                f.readline()              # BOX header + x/y/z bounds

            columns = f.readline().split()[2:]      # remove ITEM: and ATOMS:

            if step in req_set:
                data = [f.readline().split() for _ in range(n_atoms)]

                df = pd.DataFrame(data, columns=columns).astype(float)
                df["id"] = df["id"].astype(int)
                df["type"] = df["type"].astype(int)

                frames[step] = df

                if req_set.issubset(frames):
                    break
            else:
                for _ in range(n_atoms):
                    f.readline()

    missing = req_set - frames.keys()
    if missing:
        raise ValueError(f"Timesteps {sorted(missing)} not found in {filename}")

    return tuple(frames[step] for step in req_steps)
# --8<-- [end:read-lammps]

def extract_mo_cells(ref_df, mo_types=(2, 5, 8, 11)):
    mo_df = ref_df[ref_df["type"].isin(mo_types)].copy()
    mo_df = mo_df.sort_values("id").reset_index(drop=True)

    if len(mo_df) == 0:
        raise ValueError("No Mo atoms found.")

    return mo_df


def assign_cell_indices(mo_df, a=3.12, theta_deg=0.0, search_radius=1.0):
    """
    Assign each Mo atom to the closest ideal lattice site.

    Origin = Mo atom with lowest x, then lowest y.

    Returns
    -------
    cells : DataFrame with columns
        cell, mo_id, x, y, z, cell_x, cell_y
    """

    xy = mo_df[["x", "y"]].to_numpy(float)

    # Mo atom closest to x = 0, y = 0
    origin_index = np.argmin(xy[:, 0]**2 + xy[:, 1]**2)
    origin = xy[origin_index]

    theta = np.deg2rad(theta_deg)

    R = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)],
    ])

    a1 = R @ np.array([a, 0.0])
    a2 = R @ np.array([-0.5 * a, np.sqrt(3) * a / 2])

    basis = np.column_stack([a1, a2])
    inv_basis = np.linalg.inv(basis)

    # rough fractional coordinate, only used to know where to search
    frac = (xy - origin) @ inv_basis.T

    # how many nearby integer lattice labels to test
    n_search = int(np.ceil(search_radius / a)) + 1

    cell_x = []
    cell_y = []

    for p, f in zip(xy, frac):
        i0, j0 = np.rint(f).astype(int)

        candidates = []
        candidate_xy = []

        for di in range(-n_search, n_search + 1):
            for dj in range(-n_search, n_search + 1):
                i = i0 + di
                j = j0 + dj

                candidates.append((i, j))
                candidate_xy.append(origin + i * a1 + j * a2)

        candidates = np.array(candidates, dtype=int)
        candidate_xy = np.array(candidate_xy, dtype=float)

        distances = np.linalg.norm(candidate_xy - p, axis=1)

        # among nearby ideal sites, pick Euclidean closest
        best = np.argmin(distances)

        cell_x.append(candidates[best, 0])
        cell_y.append(candidates[best, 1])

    cells = pd.DataFrame({
        "mo_id": mo_df["id"].to_numpy(dtype=int),
        "x": mo_df["x"].to_numpy(float),
        "y": mo_df["y"].to_numpy(float),
        "z": mo_df["z"].to_numpy(float),
        "cell_x": np.array(cell_x, dtype=int),
        "cell_y": np.array(cell_y, dtype=int),
        "cell": np.arange(len(mo_df), dtype=int),
    })

    return cells


def select_matrix_cells(cells, chosen_cell_x=0, chosen_cell_y=0, supercell_side=1):
    """
    Select a supercell_side x supercell_side block in lattice coordinates.

    For odd supercell_side:
        The block is centered on (chosen_cell_x, chosen_cell_y).

    For even supercell_side:
        (chosen_cell_x, chosen_cell_y) is the bottom-left cell
        of the central 2x2 block.
    """

    if supercell_side <= 0:
        raise ValueError("supercell_side must be positive.")

    center_exists = ((cells["cell_x"] == chosen_cell_x) & (cells["cell_y"] == chosen_cell_y)).any()

    if not center_exists:
        raise ValueError(
            f"Chosen cell ({chosen_cell_x}, {chosen_cell_y}) not found."
        )

    half_size = supercell_side // 2

    if supercell_side % 2 == 1:
        # Odd size: chosen cell is the unique center.
        x_min = chosen_cell_x - half_size
        x_max = chosen_cell_x + half_size
        y_min = chosen_cell_y - half_size
        y_max = chosen_cell_y + half_size
    else:
        # Even size: chosen cell is the bottom-left cell
        # of the central 2x2 block.
        x_min = chosen_cell_x - half_size + 1
        x_max = chosen_cell_x + half_size
        y_min = chosen_cell_y - half_size + 1
        y_max = chosen_cell_y + half_size

    selected = cells[
        cells["cell_x"].between(x_min, x_max)
        & cells["cell_y"].between(y_min, y_max)
    ].copy()

    expected_cells = supercell_side**2

    if len(selected) != expected_cells:
        raise ValueError(
            f"Expected {expected_cells} cells for a "
            f"{supercell_side}x{supercell_side} block, "
            f"but found {len(selected)}. "
            "The requested block may extend beyond the available cells "
            "or contain missing lattice coordinates."
        )

    # Give the cells a deterministic ordering.
    selected = (
        selected
        .sort_values(["cell_x", "cell_y"])
        .reset_index(drop=True)
    )

    selected["original_cell"] = selected["cell"].to_numpy(dtype=int)
    selected["cell"] = np.arange(len(selected), dtype=int)

    return selected


'''
This is the list of hopping cell sites that A or C source will hop to. H2 only contains half of such hopping list bc looping over all cells will double count same type hopping. 
'''
def C3_half_neighbor_list(nx, ny):
    H1 = [
        ((nx - 1, ny - 1), 0),
        ((nx,     ny),     1),
        ((nx - 1, ny),     2),
    ]

    H2 = [
        ((nx + 1, ny),     0),
        ((nx,     ny + 1), 1),
        ((nx - 1, ny - 1), 2),
    ]

    H3 = [
        ((nx,     ny + 1), 0),
        ((nx - 2, ny - 1), 1),
        ((nx,     ny - 1), 2),
    ]

    return H1, H2, H3



def orb_i(cell_lookup, nx, ny, alpha):
    alpha = alpha.upper()

    orbital_offset = {
        "A": 0,
        "B": 2,
        "C": 5,
        "D": 8,
    }

    n_orbitals_per_cell = 11

    if alpha not in GROUP_SIZE:
        raise ValueError(f"Unknown orbital group alpha = {alpha}. Expected A/B/C/D.")

    key = (int(nx), int(ny))

    cell_number = cell_lookup[key]

    start = cell_number * n_orbitals_per_cell + orbital_offset[alpha]
    stop = start + GROUP_SIZE[alpha]

    return np.arange(start, stop, dtype=int)