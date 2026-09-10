import numpy as np
from Neighbor import orb_i, C3_half_neighbor_list
from Param import PARAMS, GROUP_SIZE, GROUPS, VALID

def H0(params, uxx, uyy, uxy):
    t, a, b = params[0,:,:], params[1,:,:], params[2,:,:]

    H = np.array([
        [t[0,1],      0,      0],
        [     0, t[0,1],      0],
        [     0,      0, t[0,0]]
    ])
    H += (uxx + uyy) * np.array([
        [a[0,1],      0,      0],
        [     0, a[0,1],      0],
        [     0,      0, a[0,0]]
    ])
    H += (uxx - uyy) * np.array([
        [b[0,0],       0,        0],
        [     0, -b[0,0],   b[0,1]],
        [     0,  b[0,1],        0]
    ])
    H += 2 * uxy * np.array([
        [     0,   b[0,0],   b[0,1]],
        [b[0,0],        0,        0],
        [b[0,1],        0,        0]
    ])
    return H


def H1(params, uxx, uyy, uxy):
    t, a, b = params[0,:,:], params[1,:,:], params[2,:,:]
    
    H = np.array([
        [t[1,0],      0,      0],
        [     0, t[1,1], t[1,2]],
        [     0, t[1,3], t[1,4]]
    ])
    
    H += (uxx + uyy) * np.array([
        [a[1,0],      0,      0],
        [     0, a[1,1], a[1,2]],
        [     0, a[1,3], a[1,4]]
    ])
    
    H += (uxx - uyy) * np.array([
        [b[1,0],      0,      0],
        [     0, b[1,1], b[1,2]],
        [     0, b[1,3], b[1,4]]
    ])
    
    H += 2 * uxy * np.array([
        [     0, b[1,5], b[1,6]],
        [b[1,7],      0,      0],
        [b[1,8],      0,      0]
    ])
    
    return H


def H2(params, uxx, uyy, uxy):
    t, a, b = params[0,:,:], params[1,:,:], params[2,:,:]
    H = np.array([
        [ t[2,0], t[2,3], t[2,4]],
        [-t[2,3], t[2,1], t[2,5]],
        [-t[2,4], t[2,5], t[2,2]]
    ])
    
    H += (uxx + uyy) * np.array([
        [ a[2,0], a[2,3], a[2,4]],
        [-a[2,3], a[2,1], a[2,5]],
        [-a[2,4], a[2,5], a[2,2]]
    ])
    
    H += (uxx - uyy) * np.array([
        [ b[2,0], b[2,3], b[2,4]],
        [-b[2,3], b[2,1], b[2,5]],
        [-b[2,4], b[2,5], b[2,2]]
    ])
    
    H += 2 * uxy * np.array([
        [     0, b[2,6], b[2,7]],
        [b[2,6],      0, b[2,8]],
        [b[2,7],-b[2,8],      0]
    ])
    
    return H


def H3(params, uxx, uyy, uxy):
    t, a, b = params[0,:,:], params[1,:,:], params[2,:,:]
    H = np.array([
        [t[3,0],      0,      0],
        [     0, t[3,1], t[3,2]],
        [     0, t[3,3], t[3,4]]
    ])
    
    H += (uxx + uyy) * np.array([
        [a[3,0],      0,      0],
        [     0, a[3,1], a[3,2]],
        [     0, a[3,3], a[3,4]]
    ])
    
    H += (uxx - uyy) * np.array([
        [b[3,0],      0,      0],
        [     0, b[3,1], b[3,2]],
        [     0, b[3,3], b[3,4]]
    ])
    
    H += 2 * uxy * np.array([
        [     0, b[3,5], b[3,6]],
        [b[3,7],      0,      0],
        [b[3,8],      0,      0]
    ])
    
    return H


def rotate_strain(uxx, uyy, uxy, times=1):

    uxx_rot, uyy_rot, uxy_rot = uxx, uyy, uxy
    for _ in range(times):
        uxx_rot, uyy_rot, uxy_rot = (
            0.25 * uxx_rot + 0.75 * uyy_rot - 0.5 * np.sqrt(3) * uxy_rot,
            0.75 * uxx_rot + 0.25 * uyy_rot + 0.5 * np.sqrt(3) * uxy_rot,
            0.5*(0.50 * np.sqrt(3) * uxx_rot - 0.50 * np.sqrt(3) * uyy_rot - uxy_rot)
        )
    return uxx_rot, uyy_rot, uxy_rot


def rotate_matrix(H, times=1):
    U_R = np.array([
        [         -1/2, np.sqrt(3)/2, 0],
        [-np.sqrt(3)/2,         -1/2, 0],
        [            0,            0, 1]
    ])
    
    result = H
    for _ in range(times):
        result = U_R.T @ result @ U_R
    
    return result


def build_H(instr, strain):
    order = instr["order"]
    alpha = instr["alpha"]
    beta = instr["beta"]
    c3 = instr.get("c3", 0)

    params = PARAMS[(order, alpha, beta)]

    uxx = strain["exx"]
    uyy = strain["eyy"]
    uxy = strain["exy"]

    uxx_r, uyy_r, uxy_r = rotate_strain(uxx, uyy, uxy, times=c3)

    if order == 0:
        H_ref = H0(params, uxx_r, uyy_r, uxy_r)
    elif order == 1:
        H_ref = H1(params, uxx_r, uyy_r, uxy_r)
    elif order == 2:
        H_ref = H2(params, uxx_r, uyy_r, uxy_r)
    elif order == 3:
        H_ref = H3(params, uxx_r, uyy_r, uxy_r)
    else:
        raise ValueError(f"Unknown neighbor order: {order}")

    H_rot = rotate_matrix(H_ref, times=c3)

    n_alpha = GROUP_SIZE[alpha]
    n_beta = GROUP_SIZE[beta]

    return H_rot[:n_alpha, :n_beta]


'''
================================================
Below is for periodic neighbors
================================================
'''

def wrap(cells):
    """
    Make a periodic cell wrapper for a rectangular selected cell block.

    Requires selected cells to form a full rectangular grid in cell_x, cell_y.
    For N_sites = 1, this always works.
    """

    xs = np.sort(cells["cell_x"].astype(int).unique())
    ys = np.sort(cells["cell_y"].astype(int).unique())

    # Require consecutive integer cell coordinates.
    if len(xs) > 1 and not np.all(np.diff(xs) == 1):
        raise ValueError("cell_x values are not consecutive; periodic wrapping is ambiguous.")

    if len(ys) > 1 and not np.all(np.diff(ys) == 1):
        raise ValueError("cell_y values are not consecutive; periodic wrapping is ambiguous.")

    present = set(
        (int(row.cell_x), int(row.cell_y))
        for row in cells.itertuples(index=False)
    )

    expected = set(
        (int(x), int(y))
        for x in xs
        for y in ys
    )

    missing = expected - present
    if missing:
        raise ValueError(
            "Periodic wrapping needs a full rectangular selected block. "
            f"Missing cells: {sorted(missing)[:10]}"
        )

    x0 = int(xs.min())
    y0 = int(ys.min())
    nx_period = len(xs)
    ny_period = len(ys)

    def wrap_cell(cell):
        x, y = cell
        x = int(x)
        y = int(y)

        wx = x0 + ((x - x0) % nx_period)
        wy = y0 + ((y - y0) % ny_period)

        return (wx, wy)

    return wrap_cell


def build_full_H(cells, strain_df=None):
    strain_df = strain_df.set_index("id")

    wrap_cell = wrap(cells)

    mo_id_lookup = {(row.cell_x, row.cell_y): row.mo_id for row in cells.itertuples(index=False)}
    
    cell_lookup = {(row.cell_x, row.cell_y): row.cell for row in cells.itertuples(index=False)}
    
    n_cells = len(cells)
    n_orbitals_per_cell = 11
    H = np.zeros(
        (n_cells * n_orbitals_per_cell,
         n_cells * n_orbitals_per_cell),
        dtype=complex,
    )

    for cell in cells.itertuples(index=False):
        nx = cell.cell_x
        ny = cell.cell_y
        src_id = cell.mo_id

        src_strain = {
            "exx": strain_df.loc[src_id, "exx"],
            "eyy": strain_df.loc[src_id, "eyy"],
            "exy": strain_df.loc[src_id, "exy"],
        }
        for alpha in GROUPS:
            beta = alpha
            instr = {
                    "order": 0,
                    "alpha": alpha,
                    "beta": beta,
                    "c3": 0,
                }

            H_block = build_H(instr, strain=src_strain)
            row_idx = orb_i(cell_lookup, nx, ny, alpha)
            col_idx = orb_i(cell_lookup, nx, ny, beta)
            H[np.ix_(row_idx, col_idx)] += H_block


        for order, Hn in zip([1,2,3], C3_half_neighbor_list(nx,ny)):
            for tar, c3 in Hn:
                mx, my = wrap_cell(tar)
                tar_id = mo_id_lookup[(mx, my)]
                tar_strain = {
                    "exx": strain_df.loc[tar_id, "exx"],
                    "eyy": strain_df.loc[tar_id, "eyy"],
                    "exy": strain_df.loc[tar_id, "exy"],
                }
                bond_strain = {
                    "exx": 0.5 * (src_strain["exx"] + tar_strain["exx"]),
                    "eyy": 0.5 * (src_strain["eyy"] + tar_strain["eyy"]),
                    "exy": 0.5 * (src_strain["exy"] + tar_strain["exy"]),
                }

                for alpha in GROUPS:
                    for beta in GROUPS:
                        if (alpha, beta) not in VALID[order]:
                            continue

                        instr = {
                            "order": order,
                            "alpha": alpha,
                            "beta": beta,
                            "c3": c3,
                        }

                        H_block = build_H(instr, strain=bond_strain)

                        row_idx = orb_i(cell_lookup, nx, ny, alpha)
                        col_idx = orb_i(cell_lookup, mx, my, beta)

                        H[np.ix_(row_idx, col_idx)] += H_block
                        H[np.ix_(col_idx, row_idx)] += H_block.conj().T
    return H


'''
================================================
Below is for non-periodic neighbors
================================================
'''
def build_full_H_open(cells, strain_df=None):
    strain_df = strain_df.set_index("id")

    mo_id_lookup = {(row.cell_x, row.cell_y): row.mo_id for row in cells.itertuples(index=False)}
    
    cell_lookup = {(row.cell_x, row.cell_y): row.cell for row in cells.itertuples(index=False)}
    
    n_cells = len(cells)
    n_orbitals_per_cell = 11
    H = np.zeros(
        (n_cells * n_orbitals_per_cell,
         n_cells * n_orbitals_per_cell),
        dtype=complex,
    )

    for cell in cells.itertuples(index=False):
        nx = cell.cell_x
        ny = cell.cell_y
        src_id = cell.mo_id

        src_strain = {
            "exx": strain_df.loc[src_id, "exx"],
            "eyy": strain_df.loc[src_id, "eyy"],
            "exy": strain_df.loc[src_id, "exy"],
        }
        for alpha in GROUPS:
            beta = alpha
            instr = {
                    "order": 0,
                    "alpha": alpha,
                    "beta": beta,
                    "c3": 0,
                }

            H_block = build_H(instr, strain=src_strain)
            row_idx = orb_i(cell_lookup, nx, ny, alpha)
            col_idx = orb_i(cell_lookup, nx, ny, beta)
            H[np.ix_(row_idx, col_idx)] += H_block


        for order, Hn in zip([1,2,3], C3_half_neighbor_list(nx,ny)):
            for tar, c3 in Hn:
                mx, my = tar #key difference from periodic

                if (mx, my) not in mo_id_lookup: #key difference from periodic
                    continue

                tar_id = mo_id_lookup[(mx, my)]
                tar_strain = {
                    "exx": strain_df.loc[tar_id, "exx"],
                    "eyy": strain_df.loc[tar_id, "eyy"],
                    "exy": strain_df.loc[tar_id, "exy"],
                }
                bond_strain = {
                    "exx": 0.5 * (src_strain["exx"] + tar_strain["exx"]),
                    "eyy": 0.5 * (src_strain["eyy"] + tar_strain["eyy"]),
                    "exy": 0.5 * (src_strain["exy"] + tar_strain["exy"]),
                }

                for alpha in GROUPS:
                    for beta in GROUPS:
                        if (alpha, beta) not in VALID[order]:
                            continue

                        instr = {
                            "order": order,
                            "alpha": alpha,
                            "beta": beta,
                            "c3": c3,
                        }

                        H_block = build_H(instr, strain=bond_strain)

                        row_idx = orb_i(cell_lookup, nx, ny, alpha)
                        col_idx = orb_i(cell_lookup, mx, my, beta)

                        H[np.ix_(row_idx, col_idx)] += H_block
                        H[np.ix_(col_idx, row_idx)] += H_block.conj().T
    return H