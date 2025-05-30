# Individual platform process flow

- Step 1: Create folders 
    components
    cross-sections
    floorplan
    materials
- Step 2: Create/copy metadata files 
    CHANGELOG
    layers.lyp
    drc_rules.lydrc
    layerstack.png
    process_overview.yaml
- Step 3: Copy components into "components"
- Step 4: Populate cross-sections from previous MPWs
    cross_sections.yaml
        Only cross sections that ports are attached to are needed
        Check the dimensions from the cell library for Heater and Waveguides (maybe more?)
        Example // Dummy example, not an actual one.
            - name: rib_1310nm_TE           // Name of cross section.
                xs_type: rib                // Cross section type. <Check allowed cross sections in Type_CrossSections>
                width: 10.8                 // Total width of the cross section, encompassing all the shapes
                minimum_bend_radius: 10     // Min bend radius
                layers:                     // List of involved layers
                - layer:                        // Layer entry 1
                    - 3                             // Rib layer
                    - 0                             // Layer datatype
                    offset: 0                       // Offset from centre
                    width: 0.8                      // Width of the rib layer
                - layer:                        // Layer entry 2
                    - 5                             // Slab layer
                    - 0                             // Slab layer datatype
                    offset: 0                       // Slab offset from centre
                    width: 10.8                     // Slab width
                modes:                      // List of supported modes
                - mode_numbers:                 // First supported mode
                    - 0                             // Index for TE
                    - 0                             // Index for TM
                    polarisation: TE                // Polarisation
                    wavelength: 1310                // Wavelength
                - mode_numbers:                 // Second supported mode
                    - 0                             //..
                    - 0
                    polarisation: TM
                    wavelength: 1310                //..
        DC contact pads have 80 um width (cross-section named dc)
    Include GDS files of the cross sections, with named consistent with yaml entries.
        Basically make 50um-long strips out of the cross sections
- Step 5: Populate "floorplan"
    Check the allowed floorplans in MPW call.
    The floorplan GDS is in the template. 
    Usually has this format:
        - name: Cell0_SOI_Full_Institution_Name // Large area floorplan
            design_area:
            - 11.47
            - 4.9
            final_chip_size:
            - 12.5
            - 5.5
        - name: Cell0_SOI_Half_Institution_Name // Small area floorplan
            design_area:
            - 5.5
            - 4.9
            final_chip_size:
            - 12.5
            - 5.5
    Floorplan names in GDS filename and floorplans.yaml has to be consistent.
- Step 6: Populate "materials"
    Include the material refractive index data
    Has wavelength (nm) vs real refractive index
        Q: Any reason to include imaginary refractive index?
    Only one material data in one csv file
    Stick to the material names allowed (these names will be cross-referenced by other yamls) <See allowed material names in Type_Materials>
- Step 7: Either create or import layerstack.png - as an explanation to the end user.
    I usually download standard components pdf, rip the image using Inkscape for the available stacks, then combine.
- Step 8: Create/modify process_overview.yaml
    Example format:
        process_name: Si_220nm_passive  <See allowed process names in Type_Processes>
        foundry: CORNERSTONE
        description: SOI 220nm passive process with heaters
        material: SOI                   // Should be consistent with material file names
        includes_heaters: true
        gds_layers:
        - name: Si_Etch1_EBL_DF_94nm
            layer: [60, 0]
            description: EBL-defined grating couplers. Layer will be etched. For gaps > 0.35, there is no max feature size.
            drc: { min_feature_size: 0.2, min_gap: 0.25, max_feature_length: 20.0 }  
        - name: Floorplan
            layer: [99, 0]
            is_info_only: true          // if info only, drc:{} is not required.
            description: Cell outline   
        layer_stack: <I haven't understood the layer_stack entry, where it's used, etc. It is not cross-referenced elsewhere.>
        - name: BOX
            description: BOX - buried oxide
            material: SiO2   // Can add details to here
            thickness: { value: 3.0 }
            gds_layer: null     // Has to correspond to an existing layer (on null) in gds_layers
        - name: Waveguide
            description: Full thickness SiN layer
            material: SOI
            thickness: { value: 0.22, tol: 0.02 }
            gds_layer: Si_Etch4_LF_100nm_to_BOX, not Si_Etch2_DF_70nm
        - name: Contact_pads
            description: Metal layer for contact pads and electrical routing
            material: metal1
            is_metal_layer: true
            thickness: { value: 0.22, tol: 0.01}
            gds_layer: Heat_CP_LF
- Step 9: Modify layers.lyp
    This file is the markup file for the layer display in KLayout
    These layers should be named consistently with process_overview.yaml and layers in the component gds'es.
    Since it is cosmetics, it does not necessarily break anything.
        Make sure to remove the GDSFactory-specific entries, if they exist.
    Can modify and export from KLayout
        Check the lyp file afterwards - it has a tendency to combine layer name and datatype together. Check with references.
- Step 10: Populate components - modify yamls and such
    Example:
        name: Cell0_SOI220_Full_1550nm_Packaging_Template
        component_type: PackagingTemplate
        ports:
        - name: e_o1
          port_type: optical
          center:
          - 4922.173
          - 1650.0
          orientation: 180
          cross_section: strip_1550nm_TE
        - name: e_vertical_te1
          port_type: vertical_te
          center:
          - 5290.0
          - 1650.0
          orientation: 0
          width: 10     <Cross section is absent, instead use width>
          fibre_modes:
          - fibre_type: SMF-28
            wavelength: 1550
        - name: n_e10
          port_type: electrical_dc
          center:
          - -1915.0
          - 2200.0
          orientation: 270
          cross_section: dc
    Cell names defined here must have corrresponding GDSes.
    Remove PHIX packages if they are there.
- Step 11: Import DRC rules from the call website.
    Make sure to remove inactive layers from the DRC rule, as the validator throws an error.
- Step 12: Modify CHANGELOG based on the updates in the new MPW call.
    Probably worth to append to Changelog instead of rewriting.
