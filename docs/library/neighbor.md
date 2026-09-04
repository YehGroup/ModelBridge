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

Note that we also use `missing` to record any request timesteps that was not found in the dumpfiles. For safety this will stop the function immediately and doesn't return anything. 