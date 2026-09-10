import numpy as np
from scipy.linalg import svd

p0 = np.array([[1, 0],
               [0, 0]], dtype=complex)   # |0><0|

p1 = np.array([[0, 0],
               [0, 1]], dtype=complex)   # |1><1|

tp = np.array([[0, 0],
               [1, 0]], dtype=complex)   # |1><0|

tm = np.array([[0, 1],
               [0, 0]], dtype=complex)   # |0><1|

#initialize the size of the system
def init(INPUT_UNIT_CELLS):
    global N_UNIT_CELLS, BIT_WIDTH
    N_UNIT_CELLS = INPUT_UNIT_CELLS
    BIT_WIDTH = max(1, (N_UNIT_CELLS - 1).bit_length())



def bits(n):
    return [int(bit) for bit in format(n, f"0{BIT_WIDTH}b")]

def add_direct_bond(ni, nf, t):
    mpo = []
    for bi, bf in zip(bits(ni), bits(nf)):
        if bi == bf:
            op = p0 if bi == 0 else p1
        elif bi > bf:
            op = tm
        else:
            op = tp
        
        core = np.asarray(op, dtype=complex)[None, None, :, :] # op -> [op] so in general mpo can have [op_00 op_01 ... // op_10 op_11 ... // op_20 ...]
        mpo.append(core)

    mpo[0] = t * mpo[0]
    return mpo

def add_bond(ni, nf, t): #here we assume t adjoint is t (t is real)
    bi_list = bits(ni)
    bf_list = bits(nf)

    diff = [i for i, (bi, bf) in enumerate(zip(bi_list, bf_list)) if bi != bf]

    if len(diff) == 0:
        return add_direct_bond(ni, nf, 2*t)
    else:
        first, last = diff[0], diff[-1]
        
    mpo = []

    for i, (bi, bf) in enumerate(zip(bi_list, bf_list)):
        if bi == bf:
            forward = backward = p0 if bi == 0 else p1
        elif bi > bf:
            forward, backward = tm, tp
        else:
            forward, backward = tp, tm

        if first == last == i:
            core = (forward + backward)[None, None]

        elif i < first or i > last:
            core = forward[None, None] #p0 or p1 when not in diff

        elif i == first:
            core = np.stack((forward, backward))[None, :]

        elif i == last:
            core = np.stack((forward, backward))[:, None]

        else:
            core = np.zeros((2, 2, 2, 2), dtype=complex)
            core[0, 0] = forward
            core[1, 1] = backward

        mpo.append(core)

    mpo[0] = t * mpo[0]
    return mpo

def merge_mpo(mpo1, mpo2):
    merged = []
    n = len(mpo1)

    for i, (A, B) in enumerate(zip(mpo1, mpo2)):
        A = np.asarray(A)
        B = np.asarray(B)

        if A.ndim == 2:
            A = A[None, None, :, :]
        if B.ndim == 2:
            B = B[None, None, :, :]

        if i == 0:
            C = np.concatenate((A, B), axis=1)
        elif i == n - 1:
            C = np.concatenate((A, B), axis=0)
        else:
            Dl1, Dr1, d1, d2 = A.shape
            Dl2, Dr2, _, _ = B.shape
            C = np.zeros((Dl1 + Dl2, Dr1 + Dr2, d1, d2), dtype=np.result_type(A, B))
            C[:Dl1, :Dr1] = A
            C[Dl1:, Dr1:] = B

        merged.append(C)

    return merged

def QR_mpo(mpo):
    cores = [np.asarray(core) for core in mpo]

    for i in range(len(cores) - 1):
        Dl, Dr, d_out, d_in = cores[i].shape
        matrix = cores[i].transpose(0, 2, 3, 1).reshape(Dl * d_out * d_in, Dr) #transpose: (left bond, right bond, physical out, physical in) -> (left bond, physical out, physical in, right bond)

        Q, R = np.linalg.qr(matrix, mode="reduced")
        rank = Q.shape[1]

        cores[i] = Q.reshape(Dl, d_out, d_in, rank).transpose(0, 3, 1, 2)
        #cores[i + 1] = np.einsum("ra,abij->rbij", R, cores[i + 1])
        next_core = cores[i + 1]
        Da, Db, d_out2, d_in2 = next_core.shape

        cores[i + 1] = (R @ next_core.reshape(Da, -1)).reshape(R.shape[0], Db, d_out2, d_in2)

    return cores

def svd_mpo(mpo):
    cores = list(mpo)

    #diagnosis, comment out the line below if no needed.    
    #previous_info = None

    for i in range(len(cores) - 1, 0, -1):
        Dl, Dr, d_out, d_in = cores[i].shape #l is left bond index, r is the right bond index, out and in is the physical index
        matrix = cores[i].reshape(Dl, Dr * d_out * d_in)

        #diagnosis, comment out the line below if no needed.
        #current_info = (i, matrix.shape, np.max(np.abs(matrix)), np.isfinite(matrix).all())


        scale = np.max(np.abs(matrix))
        if not np.isfinite(scale):
            raise FloatingPointError(f"NaN/Inf reached core {i}")
        if scale == 0:
            scale = 1.0
        try:
            U, s, Vh = np.linalg.svd(matrix / scale, full_matrices=False)
            s *= scale
        except Exception as e:
            #print("Previous:", previous_info) #diagnosis, comment out the line if no needed.
            #print("Failed:  ", current_info) #diagnosis, comment out the line if no needed.
            absM = np.abs(matrix)
            nonzero = absM[absM > 0]
            max_idx = np.unravel_index(np.argmax(absM), matrix.shape)
            min_idx = np.unravel_index(
                np.argmin(np.where(absM > 0, absM, np.inf)),
                matrix.shape
            )

            print("Using gesvd instead because:", type(e).__name__, e)
            print("core:", i, "shape:", matrix.shape)
            print("largest entry:", matrix[max_idx], "at", max_idx)
            print("smallest nonzero entry:", matrix[min_idx], "at", min_idx)
            print("dynamic range:", np.max(absM) / np.min(nonzero))
            
            U, s, Vh = svd(
                matrix / scale,
                full_matrices=False,
                lapack_driver="gesvd",
                check_finite=False,
            )
            s *= scale

        #diagnosis, comment out the line below if no needed.
        #previous_info = current_info

        tol = np.finfo(s.dtype).eps * max(matrix.shape) * s[0] #for debug I set to constant
        rank = max(1, np.count_nonzero(s > tol)) #the max function is used to take care of the case where rank is 0

        U = U[:, :rank]
        s = s[:rank]
        Vh = Vh[:rank, :]

        cores[i] = Vh.reshape(rank, Dr, d_out, d_in)

        transfer = U * s
        #cores[i - 1] = np.einsum("abij,bc->acij", cores[i - 1], transfer)
        prev = cores[i - 1]
        Da, Db, d_out2, d_in2 = prev.shape

        matrix_prev = (prev.transpose(0, 2, 3, 1).reshape(Da * d_out2 * d_in2, Db)) @ transfer

        cores[i - 1] = (matrix_prev.reshape(Da, d_out2, d_in2, transfer.shape[1]).transpose(0, 3, 1, 2))

    return cores

def truncate(mpo):
    return svd_mpo(QR_mpo(mpo))



#=================
# no essential
#=================

def mpo_to_matrix(mpo):
    partial = np.asarray(mpo[0])[0]   # shape (Dr, d_out, d_in)

    for core in mpo[1:]:
        core = np.asarray(core)

        Dr = core.shape[1]
        old_out, old_in = partial.shape[1:]
        d_out, d_in = core.shape[2:]

        partial = np.einsum(
            "aIJ,abij->bIiJj",
            partial,
            core,
        ).reshape(
            Dr,
            old_out * d_out,
            old_in * d_in,
        )

    return partial[0]

def mpo_mem(mpo):
    bytes_used = sum(np.asarray(core).nbytes for core in mpo)

    return {
        "bytes": bytes_used,
        "KiB": bytes_used / 1024,
        "MiB": bytes_used / 1024**2,
        "GiB": bytes_used / 1024**3,
    }

def mat_mem(matrix):
    bytes_used = np.asarray(matrix).nbytes

    return {
        "bytes": bytes_used,
        "KiB": bytes_used / 1024,
        "MiB": bytes_used / 1024**2,
        "GiB": bytes_used / 1024**3,
    }

def smat_mem(sparse_matrix):
    """Exact memory used by a SciPy CSR, CSC, or COO matrix."""
    bytes_used = sparse_matrix.data.nbytes

    if hasattr(sparse_matrix, "indices"):  # CSR or CSC
        bytes_used += (
            sparse_matrix.indices.nbytes
            + sparse_matrix.indptr.nbytes
        )
    else:  # COO
        bytes_used += (
            sparse_matrix.row.nbytes
            + sparse_matrix.col.nbytes
        )

    return {
        "bytes": bytes_used,
        "KiB": bytes_used / 1024,
        "MiB": bytes_used / 1024**2,
        "GiB": bytes_used / 1024**3,
    }


#=================
# save mpo as:
# 
# core_0000
# core_0001
# core_0002
# ...
# n_bits
#=================
def save_mpo(filename, mpo):
    data = {
        f"core_{i:03d}": np.asarray(core, dtype=np.complex128)
        for i, core in enumerate(mpo)
    }

    data["ncores"] = np.array(len(mpo))
    np.savez(filename, **data)