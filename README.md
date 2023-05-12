# merge_probe_sets

First, user downloads the contents of this git repo on their machine.

User opens the merge_probe_sets.yaml file and enters the name of the new project
folder they'd like to create, and lists locations of arms files they want to use
to search for probes.

User also opens the input_files/mip_ids.txt file and enters the probes they
would like in the final project folder (or optionally the probes they'd like to
exclude).

User runs program with snakemake -s merge_probe_sets.smk --cores 4

Todo: add installation instructions for installing snakemake
