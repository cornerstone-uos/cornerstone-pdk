# cornerstone-pdk

Repository for official PDK releases of CORNERSTONE. 

The structure of this repository is arranged for the convenience of the export toolset. The platform material (component GDS, material data, DRC rules) can be found as a whole in Wavephotonics PDK Management Platform ([PDK Portal](https://cornerstone.wavephotonics.com/)), as well as on our website : [Live MPW Calls](https://cornerstone.sotonfab.co.uk/mpw/live-calls/)

We currently offer these platforms as part of our MPW service:

- SOI 220nm Active
- SOI 220nm Passive
- SOI 340nm
- SOI 500nm
- Ge-on-Si
- Suspended Si 
- SiN 300nm
- SiN 200nm Visible

We currently have two versions of Suspended Si (biased/unbiased), please communicate with us the version you chose during submission.

For custom materials and topologies, please contact us at [cornerstone@soton.ac.uk](mailto:cornerstone@soton.ac.uk)

## Overview of the repository structure

- `SiN_300nm/`, `Si_220nm_active/`, &c: Folders for platforms that CORNERSTONE offers.
- `<PlatformFolder>/components/`: Contains components for the said platform.
- `<PlatformFolder>/cross-sections/`: Contains cross-sections defined within the platform.
- `<PlatformFolder>/floorplans/`: Contains the floorplans/design areas for the offered tiers of service, specific to the platform.
- `<PlatformFolder>/materials/`: Contains refractive index information regarding the materials involved in the said platform.
- `<PlatformFolder>/docs/`: Contains documentation-related files for the platform.
- `<PlatformFolder>/experimental/`: Contains experimental data (mostly post-processed) for the platform.
- `<PlatformFolder>/sparams/`: Contains generated s-parameters for the components within the platform.
- `<PlatformFolder>/process_overview.yaml/`: Process overview for the platform - contains information such as layer definitions and corresponding process parameters.
- `<PlatformFolder>/drc_rules.lydrc`: DRC script for the platform.
- `<PlatformFolder>/layerstack.png/`: Diagram of offered topologies within the platform.
- `<PlatformFolder>/layers.lyp`: Cosmetics for KLayout Layer Toolbox
- `<PlatformFolder>/CHANGELOG.md`: Version information for the platform.
- `README.md`: This document
- `pyproject.toml`: Dependency list for installation using `uv pip install .[docs, validator]`

# Validation

Wavephotonics YAML format is a convenient standard to use for PDK export across a variety of platforms. The validator for this format is listed in the dependencies of the repository. To use, simply sync the dependencies, activate the environment and run validation command. 

Using `uv`, these can be done as:
- `uv sync`
- `source .venv/bin/activate` (Linux) or `./venv/Scripts/activate` (Windows)
- `pdk-data-verifier validate .`

You can also use the verifier through the testing panel in VSCode. To access this, select the Python interpreter for the virtual environment (`Ctrl + Shift + P` -> `Python: Select Interpreter` -> `.venv/Scripts/python.exe` or `.venv/bin/python`); then go to the `Testing` panel and run the `test_data.py` test.


<!-- Adding some CSS
<style type="text/css">
    ol {list-style-type: decimal;}
    ol ol {list-style-type: lower-alpha;}
    ul {list-style-type: disc;}
    ul ul {list-style-type: circle;}
</style> -->
