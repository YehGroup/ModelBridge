# ModelBridge

ModelBridge is a collection of tools for constructing and running theoretical and computational model for Professor Nai-Chang Yeh's group in Caltech. The project is currently under active development, still in the process of cleanning and shipping previous scripts. Documentation will be added alongside the code as new components are implemented.

> Ok ModelBridge is a pretty lame name, but it is trying to capture the idea that this package contains toolkits for our lab's attempt to bridge our experimental observation with our computational/theoretical model. In hopes to obtain suggestions on what could be attempted for future experiments or suggestions on how we could tailor our model to reflect significant observations. 

## Quick Start

Download the `Library/` folder from the ModelBridge GitHub repository and copy it into your working project.

```text
your_project/
├── Library/
└── your_script.py
```

You can then import the modules you need from `Library`. For example
```python
from Library.Hamiltonian import build_full_H
```
See a standalone working example in [`Example_Eigen.py`](https://github.com/YehGroup/ModelBridge/blob/main/Example_Eigen.py). 

??? info "Install Dependences"

    The easiest way is to create an virtual environment on `your_project` folder by copying the [`setup_env.sh`](https://github.com/YehGroup/ModelBridge/blob/main/setup_env.sh) to `your_project` folder and run it in your terminal:

    ```terminal
    chmod +x setup_env.sh
    ./setup_env.sh
    ```

## Shipping Progress

- [x] Documentation framework with Zensical
- [x] Automatic GitHub Pages deployment
- [x] Synced some code snippets from source files into documentation
- [x] Parameter definitions for the current model (`Library/Param.py`)
- [x] Create and maintain dependences
- [x] Codes for Reading and interacting with LAMMPS
- [ ] Lattice labeling functions
- [ ] Strain-related functions
- [ ] Hamiltonian construction
- [ ] MPO construction
- [ ] KPM / LDOS utilities
- [ ] Examples and tutorials

## Documentation

The main code documentation is organized under the **Library** section. Source code shown in the documentation is pulled directly from the corresponding Python files, so the examples stay synchronized with the implementation.