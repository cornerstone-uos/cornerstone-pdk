# cornerstone-pdk
To keep track of the CORNERSTONE PDK and allow Wave Photonics to create PDK packages from this for various layout tools.

Please use the following structure in the repo (unless otherwise specified all length values should be given in um):

1. Add a new folder for every separate process you offer. E.g. one for SOI 220nm, one from SiN 850nm, one for SiN on SOI, etc.
2. For every process we would like the following information (for details on what to include in these files and folders see the sub-sections below):
    1.  A process overview yaml, that gives the general information on the process, such as the name and layers.
    2.  A .lyp file: layer file used by KLayout
    3.  A .lydrc file: a DRC file for automated DRC checking using KLayout
    4.  A "materials" folder: to contain refractive index data on the materials used in your process layer-stack.
    4.  An layerstack cross-section image to show the order of layers.
    4.  A "floorplans" folder to give information on standard die sizes for your process
    5.  A waveguide "cross-sections" folder: To make routing between components in the layout tools easier we would like to know about the standard cross-sections you use with the components in your PDK.
    6. The PDK components themselves and their metadata should be placed in the "components" folder.

*__Note: For some example files, please have a look in the "example_process" folder.__*

## Process Overview
Please create a file called "process_overview.yaml". This file should contain general information about the process. Please include the following entries:

- `process_name`: the name to be used for the process. This name will appear in the PDK packages and on our PDK access portal. Please make it distinctive, but not too long. The process name must be unique at the foundry.
- `foundry`: the name of the foundry. Ensure you use the correct capitalisation, as you usually spell it.
- `description`: a short text description of the process to be used on the PDK website. You can include for example the main materials and special features, such as whether heaters or other modulators are included and if this is an MPW process. Description must be <=500 characters length.
- `material`: the kind of process this is, for example `SOI`, `SiN`, `AlOx`, `AlN`, `GaAs`, `GaN`, `Ge-on-Si`, `InP`, `InP-on-SOI`, `TFLN`, `BTO`, etc.
- `includes_heaters`: notes down whether heaters are an option on this process, either `true` or `false`
- `gds_layers`: for every GDS layer, please include:

  - `name`: a descriptive, but short name without spaces. Every name must be unique in the process.
  - `layer`: the GDS layer and datatype (in a list)
  - `description`: a short description of what the layer does. For etches you should include the etch depth and variation of the etch depth. If the layer relates to another layer (e.g. two layers together indicate full etch, or one layer is the negative of another layer), this would be good to include as well. Finally, it would be helpful if you could indicate if this is a positive layer (e.g. a waveguide layer of a certain thickness) or a negative layer (e.g. where a part is etched away).
  - `is_info_only`: (Optional) a boolean (`true` or `false`) indicating whether this layer is purely for information and does not affect the final chip. If not set, we will assume this layer is a physical chip layer, i.e. `is_info_only = false`.
  - `drc`: the relevant DRC rules, in the following shape `{ min_feature_size: 0.06, min_gap: 0.06, max_feature_length: 20.0 }`, where the maximum feature length is optional. The latter is for example relevant for extra thin grating features. You only need to specify this, if `is_info_only` is set to `false`.
  - `alias`: another name for this layer. E.g. when you want to use a particular layer also for on-chip labels. If the alias use of the layer comes with different DRC rules, please list alias layer separately too and specify the relevant DRC rules there. If you want more than one alias, you can put them into a list.

  If you can, please also include which layers should be used to indicate the floorplan (design area outline), final chip size (if larger than the design area), components (device recognition), optical ports (pin recognition), electrical ports (pin recognition M), fibre ports on grating couplers (fibre target), on-chip labels (Label), gds-only text (Text). Except for the on-chip labels, all of these layers should be information-only layers and not correspond to a physical layer on the chip. If not specified here we use the following for these, so in that case please ensure the following layers do not overlap with any internally used layers:

  - Floorplan: 99/0
  - FinalChipSize: 99/1
  - Text: 66/0
  - DevRec: 68/0
  - PinRec: 1/10
  - PinRecM: 1/11
  - FbrTgt: 81/0

  If you have not specified an on-chip label layer we generally use an etch or waveguide layer in the process for this. A metal layer is also possible to use for on-chip labels, however these often have larger minimum feature sizes, which makes the labels more restricted. If you have a layer you would recommend, please indicate this with the "alias" option above.

- `layer_stack`: Please indicate the physical layers (including metal routing and via layers) in the layer stack with the following details:

  - `name`: The unique name of the part of the layer stack. E.g. `BOX` (bottom oxide), `Waveguide` (for e.g. the full height waveguide core layer), `TOX` (top oxide cladding), `SLAB` (for e.g. the base part of a rib waveguide), `Heater_Filament` or `Top_Metal`, etc.
  - `description`: Short description of the layer and it's use.
  - `material`: The name for the material in the layer. This can be simple such as SiN, but also more detailed such as Thermal_SiO2 or PECVD_SiO2. Different physical layers can use the same material.
  - `thickness`: Thickness of material in the form `{ value: 0.22, tol: 0.02 }`, where the tolerance is optional if you do not have this information.
  - `gds_layer`: if relevant, specify how the layer relates to the GDS layers specified under `gds_layers`. E.g. just put the GDS layer here if it's a one-to-one correspondence, but you can also add instructions like "layer1, except for overlapping with layer2" or "overlap of layer1 and layer2" or "not layer3, layer4 or layer6".
  - `is_metal_layer`: (optional) Can be used to indicate that a layer is a metal layer and therefore doesn't require refractive index data in the materials folder.

## LYP File
Optional, but very welcome: a layer file for KLayout. Please include all layers you listed in `gds_layers` in the "process_overview.yaml" file. For more information, please have a look at the [KLayout docs on layer files](https://www.klayout.de/lyp_format.html).

## LYDRC File
Optional, but very welcome: a DRC ruleset file for KLayout. Please include all layer rules you also listed in `gds_layers` in the "process_overview.yaml" file. This file is also a chance to add more complex DRC rules, such as rules that check for minimum overlap between specific layers. For more information on how to generate this kind of file, please see here: [KLayout docs on DRC files](https://klayout.de/0.23/doc/manual/drc_basic.html)

## Materials
For every material in your layer stack, except for maybe electrical layers, we need the relevant material refractive indices. For every material listed under `layer_stack` in the process overview, please include a .csv file with the name of the file corresponding to the material name, with `wavelength (nm), refractive index` as the header. In this csv file please include data for the refractive index at as many wavelength values (in nm) as you can find. If you are using literature values from <https://refractiveindex.info>, you can easily download the data from there into .csv file format. Please ensure you update the header to `wavelength (nm), refractive index` and adapt the wavelengths from um to nm, though.

## Layerstack
Optional, but very welcome: one or more images showing the layerstack options. For example for a strip and a rib waveguide or for passive vs. active layer stack variations.

## Floorplans
This folder should contain a "floorplans.yaml" file that gives a list of floorplans, detailing the design area/final chip sizes for the standard chip sizes you use for this process. You can (optionally) also include gds files with the floorplans here (one gds file per floorplan). In this case, please ensure that the gds file name corresponds to a floorplan name in the yaml as well, giving the corresponding design area and final chip sizes.

## Cross-Sections
Please list all standard waveguide cross-sections in the "cross_sections.yaml" yaml file in the "cross-sections" folder and add an example GDS file for this cross-section into the folder, too. For the GDS examples please create a waveguide using this cross-section going from west to east with a length of 50 um. The GDS filename should correspond to the `name` listed in the cross-sections yaml. In the yaml you should  include the following information for every cross-section:

- `name`: a short, but descriptive name for the cross-section, e.g. `strip_1550nm_TE`
- `xs_type`: e.g `strip`, `rib`, `strip-loaded`, `deep`, `shallow`, `dc`, etc.
- `width`: the port width for any optical ports using this cross-section. Usually the width of the main waveguide section.
- `minimum_bend_radius`: the minimum recommended bend radius
- `layers`: somewhat a duplicate from the example GDS file. For every element of the cross-section, include the GDS `layer`, the `width` on this layer and the `offset` from the waveguide centre.
- `modes`: please also include which light modes the cross-section supports. For every mode include the `mode_numbers` in x and y (respectively, as a list of two integers), `polarisation` (e.g. `TE`, `TM`, `quasi-TE`, `quasi-TM` or `mixed`) and the central `wavelength` in nm as an integer or floating point value (e.g. 1550).
- `is_suspended`: (optional) For suspended platforms, e.g. a suspended silicon platform, please indicate this on the relevant cross-sections with `is_suspended: true`: This is needed, since these kind of waveguides do not have a consistent cross-section geometry to extrude. Please do still include the cross-sections, so we can obtain the mode information at the ports and match ports. If not set, we will assume `is_suspended: false` for this cross-section.

If you want you can also include electrical routing cross-sections. In this case, please use the types `dc` for DC routing or `gsg` (ground-signal-ground) or `gs` (ground-signal) for RF routing. For DC routing you can set the minimum bend radius to 0. You do not need to specify the `modes` in this case, you still have to specify the `layers`, though!

## PDK Components
For every component, please add a gds file and a yaml file with the same filename. The yaml file is used to capture the metadata of the component, such as port information and must be given for every component. Please add the following information to the component yamls:

- `name`: the name of the component, should be as short as possible, but should be unique for any (wavelength, polarisation) tuple relevant to the component. E.g. for a crossing component that allows the crossing of a 1550nm TE and a 1310nm TM waveguide, the name must be unique for all components in the PDK that work with 1550nm TE light and all components in the PDK that work with 1310nm TM light. For a 1x2 MMI that was optimised for only 1550nm TM light, the name only needs to be unique for all components in the PDK that use 1550nm TM light.
- `component_type`: Please choose one of the following "MMI1x2", "MMI2x2", "MMI1x4", "OpticalHybrid90deg2x4", "OpticalHybrid90deg4x4", "DirectionalCoupler", "GratingCoupler1D" (a regular grating coupler), "GratingCoupler2D", "EdgeCoupler"  (e.g. a spot size converter), "Crossing", "Taper", "Bend", "Terminator", "WaveguideConverter" (e.g. for a component that converts between strip and rib waveguides), "ModeConverter", "RingResonator", "PolarisationFilter", "PolarisationSplitter1x2" (a 1x2 polarising beam splitter), "PolarisationSplitter2x2" (a 2x2 polarising beam splitter), "PolarisationRotator", "BraggFilter" (for fully passive Bragg filters), "BraggReflector", "AWG", "WavelengthMUX", "ModeMUX", "AlignmentMarker", "ContactPadDC", "ContactPadRF", "PackagingTemplate", "AmplitudeModulator", "PolarisationModulator", "EOPM" (Electro-Optic Phase Modulator), "TOPM" (Thermo-Optic Phase Modulator, also known as a heater), "Photodiode", "SOA" (Semiconductor Optical Amplifier), "BraggReflectorHeater" (for Bragg filters with a heating element for tuning), "DFBLaser" (Distributed Feedback Laser) or "DBRLaser" (Distributed Bragg Reflector Laser). If you are unsure which component type is the correct one, or you are missing a component type, please let us know and we will either point you to the right component type or add a new one.
- `designers`: (optional) if the designer is different from the organisation that designed the PDK, you can add a list of designer names here. This is relevant for e.g. open-source PDKs, where external designers can contribute to a PDK.
- `publications`: (optional) if the component has been featured in any publications, you can add a link to this publication here if you want.
- `ports`: for every optical or electrical port of the component, please give the following information:
  - `name`: for in-plane optical ports, we usually use `o1`, `o2`, etc. For electrical ports we generally use `e1`, `e2` etc. for  For (out-of-plane) fibre ports we use `vertical_te1`, `vertical_te2`, etc (or `_tm` for TM grating couplers) and for edge couplers we use `edge1`, `edge2`, etc.
  - `port_type`: please choose between `optical` (in-plane optical port), `electrical_dc` or `electrical_rf` (DC and RF ports), `vertical_te` or `vertical_tm` for grating coupler fibre ports and `edge` for edge coupler ports.
  - `center`: please give the x and y coordinate of the center of the port.
  - `width`: (optional) For electrical ports, if you do not specify a cross-section, please specify a width of the port here.
  - `orientation`: the orientation of the port (outward of the component) in degrees. For example 0 is east, 90 is north, 180 is west and 270 is south pointing.
  - `cross_section`: refers to the unique name of one of the cross-sections specified in "cross-sections/cross_sections.yaml", e.g. `strip_1550nm_TE`. Is optional for electrical ports, in this case please specify the width instead.
  - `modes`: (optional) if the optical modes at this port are different from the modes specified for the cross-section referenced above, please add the modes relevant to the component port here, including the `mode_numbers`, `polarisation` and `wavelength` (in nm) for each mode at this port. For examples, please see the modes given in the cross-sections yaml.
  - `fibre_modes`: (only needed for fibre ports) if you're adding a fibre port, please specify the `fibre_type` and `wavelength` for this port. For the fibre type, please choose from the following: 'SM300', 'S405-XP', 'SM400', 'SM450', '460HP', 'SM600', 'S630-HP', '630HP', '780HP', 'HI780', 'SM800-5.6-125', 'SM800G80', 'SM980-5.8-125', 'SM980G80','1060XP', '980HP', 'HI1060', 'SMF-28', 'CCC1310', '1310BHP', 'SM1550P', 'SM1250G80', '1550BHP', 'SM1500G80', 'DCF4' or 'SM1950'. If your fibre type is not represented here, please contact us and we'll add it to the list.


## Changelog
For every PDK, please maintain a changelog in CHANGELOG.md. This file should get an entry for every version of the PDK, so when you create a new PDK, there will be one entry in this file. However, if you make changes and start a pull request to main, you should add a new entry for this update. For every entry, we need

- a version: an entry in the form `## 1.0`
- a short description of what changed underneath that (at least 5 characters long, at most a few lines)

Note: new version entries should always be added above the older versions.

# Validation

We have written some code to automatically check the PDK data for completeness and consistency. You have two options to run this code, via a unit test or via the terminal.
For both approaches you will need to install the relevant python environment first. We recommend using uv, where the environment gets created as specified in the pyproject.toml file. To get the environment up and running, run the following command (ensure you are in the base folder of the repo in your terminal):

`uv sync`

## Running the validation via the terminal

First you will need to activate the environment you installed above (ensure you are in the base folder of the repo in your terminal):

`source .venv/bin/activate`

Next, you can run the following command:

`pdk-data-verifier validate .`

## Running the validation via the unit testing panel

First ensure you are using the correct environment. Please use the shortcut `Ctrl + Shift + P` to open up the menu right at the top centre of the VS Code window and start typing "Python: Select Interpreter" and then select the environment ".venv".

Then go into the test panel of the menu on the left and select run tests. If the tests go through without trouble, the test will turn green. If there is something to fix, the test will turn red and you will be given a message in the "TEST RESULTS" panel.

Please read through the messages in the table to see what you need to fix, do the fixes and then run the validation again.

<!-- Adding some CSS
<style type="text/css">
    ol ol { list-style-type: lower-alpha; }
</style> -->
