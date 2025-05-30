# PDK Repo Todo list

Remaining components:
- SiN_300nm
    Created and populated from Wavephotonics files. Requires repopulating

- Si_220nm_active
    Not started

- Si_220nm_passive
    Created and populated from Wavephotonics files. Requires repopulating

- Si_340nm
    Step 1 done
    Step 2 done
    Step 3 skipped - redundant with Step 8/9/10
    Step 4 done
    Step 5 done
    Step 6 done
    Step 7 done
    Step 8/9/10:
        Components are missing
        Issue with components: layer names are not descriptive or missing
        Process_overview and layers.lyp depends on layer names
        Our components have layers like 1/0,2/0 etc, there are no layer names. The YAML files look for layer names.
        This might cause an issue - in discussion with Shengqi
    Step 11 done
    Step 12 done

- Si_500nm
    Step 1 done
    Step 2 done
    Step 3 skipped
    Step 4: Done, suspicions with defining "rib" geometry. 
        SOI500 does not have strips, everything is rib, hence there is actually no extra layer for rib protection.
        This makes the cross section effectively a strip, but we will still define it as rib because everything on this 
            is going to be rib anyways, who cares.
    Step 5 done    
    Step 6 done
    Step 7 done
    Step 8/9/10 is not done.
    Step 11 done
    Step 12 done

- Si_sus_bias
    Not started

- Si_sus_nobias
    Not started

- Ge_on_Si
    Folder created but empty

- SiN_200nm
    Not online, future work