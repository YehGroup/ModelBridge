import numpy as np

def fmt(z, precision=2, tol=1e-12):
    z = complex(z)
    real = 0 if abs(z.real) < tol else z.real
    imag = 0 if abs(z.imag) < tol else z.imag

    if imag == 0:
        return f"{real:.{precision}g}"
    if real == 0:
        return f"{imag:.{precision}g}j"
    return f"{real:.{precision}g}{imag:+.{precision}g}j"


def matrix_lines(matrix, precision=2, tol=1e-12, width=None):
    matrix = np.asarray(matrix)

    if width is None:
        width = max(len(fmt(x, precision, tol)) for x in matrix.flat)

    lines = []
    n_rows = matrix.shape[0]

    for i, row in enumerate(matrix):
        if n_rows == 1:
            left, right = "[", "]"
        elif i == 0:
            left, right = "⎡", "⎤"
        elif i == n_rows - 1:
            left, right = "⎣", "⎦"
        else:
            left, right = "⎢", "⎥"

        values = " ".join(
            f"{fmt(x, precision, tol):^{width}}" for x in row
        )
        lines.append(f"{left} {values} {right}")

    return lines


def print_mat(matrix, precision=2, tol=1e-12):
    for line in matrix_lines(matrix, precision, tol):
        print(line)


def print_mpo(mpo, precision=2, tol=1e-12, spacing=4):
    rendered_cores = []

    for core in mpo:
        core = np.asarray(core)

        if core.ndim == 2:
            core = core[None, None, :, :]

        Dl, Dr, _, _ = core.shape
        number_width = max(
            len(fmt(x, precision, tol)) for x in core.flat
        )

        lines = []

        for a in range(Dl):
            operator_blocks = [
                matrix_lines(core[a, b], precision, tol, number_width)
                for b in range(Dr)
            ]

            for operator_rows in zip(*operator_blocks):
                lines.append("  ".join(operator_rows))

        inside_width = max(len(line) for line in lines)

        lines = [
            (
                "⎡" if i == 0
                else "⎣" if i == len(lines) - 1
                else "⎢"
            )
            + " " + line.ljust(inside_width) + " "
            + (
                "⎤" if i == 0
                else "⎦" if i == len(lines) - 1
                else "⎥"
            )
            for i, line in enumerate(lines)
        ]

        rendered_cores.append(lines)

    widths = [max(map(len, core)) for core in rendered_cores]
    height = max(map(len, rendered_cores))

    for row in range(height):
        print((" " * spacing).join(
            rendered_cores[i][row].ljust(widths[i])
            if row < len(rendered_cores[i])
            else " " * widths[i]
            for i in range(len(rendered_cores))
        ))

