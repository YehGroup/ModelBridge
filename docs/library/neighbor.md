# Neighbor (`Neighbor.py`)

It desrves a better name. Currently this code is to give lattice indices based on physical position of the strained $MoS_2$ simulation.

## Read LAMMPS Dumpfiles (`read_lammps_steps`)

??? info "Input"
    * `filename`: The name of the file you are reading. Ex: `position.dat`
    * `req_steps`: A list of timesteps that you want to store as a dataframe. Ex: `[0, 100, 200, 500]`

??? info "Output"
    A turple of dataframes each represent the dumpfiles of a specific steps. 
    
    Ex: `df1, df2, df3, df4 = read_lammps_steps(...)`


This assumes lammps dump files are written in the following format:

<div class="expandable-code" data-lines="7" markdown="1">
```text
ITEM: TIMESTEP
0
ITEM: NUMBER OF ATOMS
2206
ITEM: BOX BOUNDS xy xz yz pp pp pp
-5.4510441999999998e+01 5.4510441999999998e+01 0.0000000000000000e+00
-5.4972548000000003e+01 5.4972548000000003e+01 0.0000000000000000e+00
-5.2500000000000000e+01 8.6812539999999998e+01 0.0000000000000000e+00
ITEM: ATOMS id type x y z
561 13 -24.5104 -24.1401 9.85443
565 13 -24.5104 -22.4753 7.5
.
.
.
ITEM: TIMESTEP
100
ITEM: NUMBER OF ATOMS
2206
ITEM: BOX BOUNDS xy xz yz pp pp pp
-5.3965337579999911e+01 5.3965337579999911e+01 0.0000000000000000e+00
-5.4446523794540113e+01 5.4446523794540113e+01 0.0000000000000000e+00
-5.2500000000000000e+01 8.6812539999999998e+01 0.0000000000000000e+00
ITEM: ATOMS id type x y z
561 13 -24.2653 -23.9091 9.85443
.
.
.
```

</div>

Specifically, we distinguish different dumped chunck of data using `ITEM: TIMESTEP`, and then we record the data using the following procedure:

1. Read the number on next line as timestep.
2. Skip `ITEM: NUMBER OF ATOMS`, read the number on next line as number of atoms $N_{\text{atoms}}$.
3. Skip 4 lines that includes simulation box condition and dimensions.
4. Read in `ITEM: ATOMS id type x y z`, with each (excluding `ITEM:` and `ATOMS`) a column title in the resulting dataframe.
5. Record requested datas.
    1. If timestep is in `req_steps`, record all $N_{\text{atoms}}$ rows of numbers to the dataframe. 
    2. If not, skip all $N_{\text{atoms}}$ rows. 

<div class="expandable-code" data-lines="4" data-title="Source Code" markdown="1">
```python
--8<-- "Library/Neighbor.py:read-lammps"
```
</div>

??? warning "timestep no found"

    We use `missing` to record any requested timesteps that were not found in the dump files. For safety, if any requested timestep is missing, the function stops immediately and returns nothing.

## Labeling Unit Cell Lattices
The two functions below work together to give our system appropriate lattice indices. 

### Select Mo atoms (`extract_mo_cells`)
??? info "Input"
    * `ref_df`: A dataframe of a particular timestep (`ref` stands for reference).
    * `mo_types`: $Mo$ atoms' type id. Default: `mo_types=(2, 5, 8, 11)`.

??? info "Output"
    * `mo_df`: A dataframe that only contains rows of $Mo$  atoms. Where the rows are in acending order of particle id. 

<div class="expandable-code" data-lines="4" data-title="Source Code" markdown="1">
```python
--8<-- "Library/Neighbor.py:cells-types"
```
</div>

??? warning "No Mo atoms"

    This error will return if the `mo_df` contains zero rows. 

### Assign Lattice Indices to Mo atoms (`assign_cell_indices`)
Assign each Mo atom to the closest ideal lattice site.

??? info "Input"
    * `mo_df`: A dataframe with only $Mo$ atoms
    * `a`: lattice constant of $MoS_2$. Default: `3.12` Å 
    * `theta_deg`: Rotation angle in degrees of the ideal $MoS_2$ 2D lattice, relative to a default layout. Default: `0` degree.
    * `search_radius`: Radius centered on each node of the ideal $MoS_2$ 2D lattice that define the search region for the corresponding $Mo$  atom. Default: `1` Å

??? info "Output"
    * `cells`: A dataFrame with columns `mo_id, x, y, z, cell_x, cell_y, cell`

1. Use `argmin` to find the $Mo$ atom $j$ that is closest to $(0, 0)$ and chose it as the lattice origin. i.e. $\mathbf{r}_j \equiv \mathbf{r}_0$.
2. Given the lattice constant $a$ and the rotation angle `theta_deg`, written as $\theta$, we can compute 

    $$
    \begin{align*}
    \mathbf{a}_1 = \hat{R}(\theta) \begin{bmatrix}a \\ 0\end{bmatrix}
    \quad , \quad
    \mathbf{a}_2 = \hat{R}(\theta) \begin{bmatrix}-a/2 \\ \sqrt{3}a/2 \end{bmatrix}
    \end{align*}
    $$

    where $\hat{R}(\theta)$ is the rotation matrix of angle $\theta$. At this point, the ideal position of any $Mo$ atom can be written as 

    $$
    \begin{align*}
    \mathbf{r}_{(n_1, n_2)} = \mathbf{r}_0 + n_1 \mathbf{a}_1 + n_2 \mathbf{a}_2 = \mathbf{r}_0 + B \begin{bmatrix} n_1 \\ n_2  \end{bmatrix}
    \end{align*}
    $$

    where $n_1, n_2$ are integers. $B$ is the `basis` matrix defined as 

    $$
    \begin{align*}
    B \equiv \begin{bmatrix} \mathbf{a}_1 & \mathbf{a}_2  \end{bmatrix}
    \end{align*}
    $$

3. For any actual, possibly distorted $Mo$ atom in position $\mathbf{r}_i$, we have the corresponding lattice coordinates $f_1, f_2$ by multiplying $B^{-1}$

    $$
    \begin{align*}
        \mathbf{f}_i \equiv \begin{bmatrix} f_1 \\ f_2  \end{bmatrix} = B^{-1}(\mathbf{r}_i - \mathbf{r}_0)
    \end{align*}
    $$

    These lattice coordinates are stored in `frac` because they can be fractions. And we write the lattice coordinate for $\mathbf{r}_i$ as $\mathbf{f}_i$.

4. Finally, for each $\mathbf{r}_i$, we find the ideal (integer) lattice site whose Cartesian position is closest to it using the following method. 

    Find a candidate lattice by rounding $\mathbf{f}_i$ to the nearest integer coordinate

    $$
    \begin{align*}
    \begin{bmatrix} \text{round}(f_1) \\ \text{round}(f_2)  \end{bmatrix} \equiv (p, q)
    \end{align*}
    $$

    Then define the search size $N_s$ by

    $$
        N_s = \left\lceil \frac{R_s}{a} \right\rceil + 1
    $$

    where $R_s$ is the `search_radius` from our input. Then, around the rough guess $(p, q)$, we form an square neighborhood in lattice-coordinate space to search over

    $$
        C = \{(p + \Delta p , q + \Delta q) : |\Delta p| \leq N_s \ , \  |\Delta q| \leq N_s \}
    $$

    The coordinate in $C$ that is the closest to $\mathbf{r}_i$ will be assigned as the lattice coordinate `(cell_x, cell_y)` of atom $i$.

5. Lastly, we give those cells a seperate index: `cell` that is different from their particle id, for conceptual clarity.  

<div class="expandable-code" data-lines="4" data-title="Source Code" markdown="1">
```python
--8<-- "Library/Neighbor.py:cells-indices"
```
</div>

??? Warning "Could be Very Off"

    This will not be a accurate function if the lattice constant of the system is either varying strongly or very different from the input `a`. So preferably use this for a relaxed system and you have checked using other methods what the histogram of the lattice distance $Mo - Mo$.

### A Subset of All Unit Cells (`select_matrix_cells`)
This is just a particular helpful function when we only want to construct Hamiltonian for a subset of all the $MoS_2$ that we simulated. It selects a `supercell_side` x `supercell_side` block in lattice coordinates.

??? info "Input"
    * `cells`: A dataframe with `cell_x, cell_y, cell`. 
    * `chosen_cell_x`: x lattice coordinate of your region's center
    * `chosen_cell_y`: y lattice coordinate of your region's center
    * `supercell_side`: A side of the sqaure region you specify to define the size

??? info "Output"
    * `selected`: A sub-dataframe of selected rows in `cells` dataframe

??? note "Definition of center"
    For odd supercell_side:
        The block is centered on (chosen_cell_x, chosen_cell_y).

    For even supercell_side:
        (chosen_cell_x, chosen_cell_y) is the bottom-left cell
        of the central 2x2 block.

<div class="expandable-code" data-lines="4" data-title="Source Code" markdown="1">
```python
--8<-- "Library/Neighbor.py:sub-cells"
```
</div> 

## Neighbors of a $MoS_2$ unit cell



<div class="expandable-code" data-lines="4" data-title="Source Code" markdown="1">
```python
--8<-- "Library/Neighbor.py:neighbors"
```
</div> 